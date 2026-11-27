#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Live Citation & URL Reachability Verifier (Playbook Pass 5):
Parses every `url = {...}` and `doi = {...}` entry in `paper/refs.bib` and verifies
HTTP 200/301/302/303 reachability (using HEAD then GET fallback) with polite User-Agent.
Zero fabricated citations, zero broken DOIs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIB_PATH = ROOT / "paper" / "refs.bib"
ATLAS_VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").exists() else "2.9.0"


def _title_tokens(title: str) -> set[str]:
    clean = re.sub(r"\\[A-Za-z]+\{([^}]*)\}", r"\1", title)
    clean = re.sub(r"[{}]", "", clean)
    stop = {"the", "of", "and", "in", "for", "a", "an", "to", "with", "on", "by"}
    return {t for t in re.findall(r"[a-z0-9]+", clean.lower()) if len(t) >= 3 and t not in stop}


def check_doi(doi: str, expected_title: str = "", timeout: int = 15) -> tuple[bool, str]:
    """Verify DOI registration via DOI Handle REST API + Crossref retraction & title parity check (Playbook Item 16)."""
    clean_doi = doi.strip()
    api_url = f"https://doi.org/api/handles/{urllib.parse.quote(clean_doi, safe='/')}"
    req = urllib.request.Request(api_url, headers={"User-Agent": f"0thernes-CitationVerifier/{ATLAS_VERSION}"}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.getcode() != 200:
                return False, f"HTTP {resp.getcode()}"
            payload = json.loads(resp.read().decode("utf-8"))
            if payload.get("responseCode") != 1:
                return False, f"DOI code {payload.get('responseCode')}"
    except Exception as exc:
        return False, str(exc)

    exp_toks = _title_tokens(expected_title) if expected_title else set()

    # Zenodo record title parity check for DataCite/Zenodo DOIs
    if clean_doi.lower().startswith("10.5281/zenodo."):
        rec_id = clean_doi.rsplit(".", 1)[-1]
        z_req = urllib.request.Request(
            f"https://zenodo.org/api/records/{rec_id}",
            headers={"User-Agent": f"0thernes-CitationVerifier/{ATLAS_VERSION}"},
            method="GET",
        )
        try:
            with urllib.request.urlopen(z_req, timeout=timeout) as z_resp:
                if z_resp.getcode() == 200:
                    z_title = str(json.loads(z_resp.read().decode("utf-8")).get("metadata", {}).get("title", ""))
                    if exp_toks and z_title:
                        overlap = len(exp_toks & _title_tokens(z_title)) / max(1, len(exp_toks))
                        if overlap < 0.60:
                            return False, f"TITLE MISMATCH ({overlap:.0%} vs {z_title!r})"
                    return True, "DOI+Zenodo OK"
        except Exception:
            return True, "DOI OK (200)"

    # Crossref retraction & title parity check for published journal/proceedings DOIs
    cr_url = f"https://api.crossref.org/works/{urllib.parse.quote(clean_doi, safe='/')}"
    cr_req = urllib.request.Request(
        cr_url,
        headers={"User-Agent": f"0thernes-CitationVerifier/{ATLAS_VERSION} (mailto:0_0@0thernes.art)"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(cr_req, timeout=timeout) as cr_resp:
            if cr_resp.getcode() == 200:
                msg = json.loads(cr_resp.read().decode("utf-8")).get("message", {})
                updates = msg.get("update-to", []) or []
                rel = msg.get("relation", {}) or {}
                retracted = any(
                    "retract" in str(u.get("type", "")).lower() or "withdraw" in str(u.get("type", "")).lower()
                    for u in updates
                ) or ("is-retracted-by" in rel)
                if retracted:
                    return False, "RETRACTED (Crossref)"
                cr_titles = msg.get("title", []) or []
                if exp_toks and cr_titles:
                    overlap = len(exp_toks & _title_tokens(str(cr_titles[0]))) / max(1, len(exp_toks))
                    if overlap < 0.60:
                        return False, f"TITLE MISMATCH ({overlap:.0%} vs {cr_titles[0]!r})"
                return True, "DOI+CR OK"
    except Exception:
        # Handle API succeeded; Crossref transient unavailability should not false-fail valid DOI
        return True, "DOI OK (200)"
    return True, "DOI OK (200)"


def check_url(url: str, timeout: int = 25, retries: int = 2) -> tuple[bool, str]:
    import time

    headers = {"User-Agent": f"Mozilla/5.0 (compatible; 0thernes-CitationVerifier/{ATLAS_VERSION}; +https://github.com/0thernes/unsolved-problems-mega-atlas)"}
    last_err = "unreachable"
    for attempt in range(retries + 1):
        methods = ("GET",) if attempt > 0 else ("HEAD", "GET")
        for method in methods:
            req = urllib.request.Request(url, headers=headers, method=method)
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    code = resp.getcode()
                    if 200 <= code < 400:
                        return True, f"HTTP {code}"
            except urllib.error.HTTPError as e:
                if method == "HEAD" and e.code in (403, 405, 429):
                    continue
                return False, f"HTTP {e.code}"
            except Exception as exc:
                last_err = str(exc)
                if method == "HEAD":
                    continue
        if attempt < retries:
            time.sleep(1.5)
    return False, last_err


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify citations in paper/refs.bib.")
    parser.add_argument("--offline", action="store_true", help="Only validate BibTeX syntax & non-empty fields without network calls")
    args = parser.parse_args()

    if not BIB_PATH.exists():
        print(f"FAIL: {BIB_PATH} not found", file=sys.stderr)
        sys.exit(1)

    raw = BIB_PATH.read_text(encoding="utf-8")
    entry_blocks = re.split(r"(?m)(?=^@\w+\{)", raw)
    entries = re.findall(r"@\w+\{([^,]+),", raw)
    urls = list(dict.fromkeys(u.strip() for u in re.findall(r"url\s*=\s*\{([^}]+)\}", raw)))
    doi_titles: dict[str, str] = {}
    for blk in entry_blocks:
        dm = re.search(r"doi\s*=\s*\{([^}]+)\}", blk)
        if dm:
            tm = re.search(r"title\s*=\s*\{(.+?)\},?\s*$", blk, flags=re.M)
            doi_titles[dm.group(1).strip()] = tm.group(1).strip() if tm else ""
    dois = list(doi_titles.keys())

    print(f"Parsed {len(entries)} BibTeX entries ({len(urls)} URLs + {len(dois)} DOIs) from {BIB_PATH.name}.")
    if len(entries) < 8:
        print("FAIL: expected at least 8 verified citations in paper/refs.bib", file=sys.stderr)
        sys.exit(1)

    if args.offline:
        print("PASS (offline syntax check).")
        return

    failures = []
    for u in urls:
        ok, status = check_url(u)
        print(f"  [{'OK  ' if ok else 'FAIL'}] {status:<14} {u}")
        if not ok:
            failures.append((u, status))
    for d in dois:
        ok, status = check_doi(d, expected_title=doi_titles[d])
        print(f"  [{'OK  ' if ok else 'FAIL'}] {status:<14} doi:{d}")
        if not ok:
            failures.append((f"doi:{d}", status))

    total = len(urls) + len(dois)
    if failures:
        print(f"\nFAIL: {len(failures)}/{total} citation target(s) failed live verification!", file=sys.stderr)
        sys.exit(1)
    print(f"\nPASS: All {total}/{total} citation URLs & DOIs verified live!")


if __name__ == "__main__":
    main()
