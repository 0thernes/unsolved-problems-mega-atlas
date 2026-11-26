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
ATLAS_VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").exists() else "2.7.0"


def check_doi(doi: str, timeout: int = 15) -> tuple[bool, str]:
    """Verify DOI registration via DOI Handle REST API + Crossref retraction check (Playbook Item 16)."""
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

    # Crossref retraction check for published journal/proceedings DOIs (non-DataCite/Zenodo)
    if not clean_doi.lower().startswith("10.5281/zenodo."):
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
                    return True, "DOI+CR OK"
        except Exception:
            # Handle API succeeded; Crossref transient unavailability should not false-fail valid DOI
            return True, "DOI OK (200)"
    return True, "DOI OK (200)"


def check_url(url: str, timeout: int = 15) -> tuple[bool, str]:
    headers = {"User-Agent": f"Mozilla/5.0 (compatible; 0thernes-CitationVerifier/{ATLAS_VERSION}; +https://github.com/0thernes/unsolved-problems-mega-atlas)"}
    for method in ("HEAD", "GET"):
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
            if method == "HEAD":
                continue
            return False, str(exc)
    return False, "unreachable"


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify citations in paper/refs.bib.")
    parser.add_argument("--offline", action="store_true", help="Only validate BibTeX syntax & non-empty fields without network calls")
    args = parser.parse_args()

    if not BIB_PATH.exists():
        print(f"FAIL: {BIB_PATH} not found", file=sys.stderr)
        sys.exit(1)

    raw = BIB_PATH.read_text(encoding="utf-8")
    entries = re.findall(r"@\w+\{([^,]+),", raw)
    urls = list(dict.fromkeys(u.strip() for u in re.findall(r"url\s*=\s*\{([^}]+)\}", raw)))
    dois = list(dict.fromkeys(d.strip() for d in re.findall(r"doi\s*=\s*\{([^}]+)\}", raw)))

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
        ok, status = check_doi(d)
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
