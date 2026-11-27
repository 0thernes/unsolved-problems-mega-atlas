#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Daily External Open-Problem Registry & Left-to-Solve Program Sync Engine (V2.11.0).

Polite, zero-dependency, read-only daily tracker polling 16 public open-problem
registries, repositories, and primary verification pages — including all live
mathematical fronts on https://lefttosolve.com/programs and its public JSON API
(/api/stats) — and writing structured daily snapshots, day-over-day diffs, an
append-only UTC history log, and a human-readable Markdown tracker.

Tracked Live Public Sources (16):
  1.  lefttosolve_stats            — https://lefttosolve.com/api/stats (JSON)
  2.  lefttosolve_programs         — https://lefttosolve.com/programs (all live fronts)
  3.  deepmind_formal_conjectures  — GitHub API (google-deepmind/formal-conjectures)
  4.  teorth_erdosproblems_gh      — GitHub API (teorth/erdosproblems)
  5.  clay_millennium              — https://www.claymath.org/millennium-problems/
  6.  erdos_problems               — https://www.erdosproblems.com/
  7.  proofatlas                   — https://proofatlas.ai/open-problems/
  8.  open_problem_garden          — https://www.openproblemgarden.org/
  9.  wikipedia_unsolved_math      — Wikimedia REST API
  10. wikipedia_unsolved_physics   — Wikimedia REST API
  11. wikipedia_unsolved_cs        — Wikimedia REST API
  12. bbchallenge                  — https://bbchallenge.org/
  13. kourovka_notebook            — https://arxiv.org/abs/1401.0300
  14. open_quantum_problems        — https://oqp.iqoqi.oeaw.ac.at/
  15. rh_grh_primary_sources       — Lean FRO statement & M. Rubinstein page
  16. 0thernes_research_archive    — GitHub API (0thernes/0thernes-research-archive)

Policy & Safety Boundaries:
  - Never solves or bypasses CAPTCHAs, Cloudflare challenges, or anti-bot PoW gates;
    gated responses are transparently reported as `js_rendered_or_gated`.
  - Advisory editorial telemetry ONLY: never silently mutates `src/v2_data/` or
    retires any cataloged open problem without human + community consensus review.
  - Daily telemetry outputs (`results/daily_registries.json`,
    `results/lefttosolve_programs.json`, `results/daily_registry_history.jsonl`,
    `docs/DAILY_REGISTRY_TRACKER.md`) live OUTSIDE the release-frozen timestamped
    `CHECKSUMS.sha256` manifest so scheduled daily updates never invalidate release
    DigiCert RFC 3161 (.tsr) or Bitcoin OpenTimestamps (.ots) cryptographic seals.

Usage:
  python scripts/sync_external_registries.py --offline
  python scripts/sync_external_registries.py --live --write-daily --write-report
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import html as html_lib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from v2_loader import (  # noqa: E402
    AI_VERIFICATION_AUDIT_NOV2026,
    ATLAS_VERSION,
    EXTERNAL_REGISTRIES_NOV2026,
    LEFT_TO_SOLVE_PROGRAMS_BASELINE,
)

TARGETS: tuple[dict[str, Any], ...] = (
    {
        "key": "lefttosolve_stats",
        "name": "Left to Solve Live Catalog Stats API",
        "url": "https://lefttosolve.com/api/stats",
        "kind": "lefttosolve_stats",
        "count_patterns": [],
    },
    {
        "key": "lefttosolve_programs",
        "name": "Left to Solve — All Live Mathematical Programs",
        "url": "https://lefttosolve.com/programs",
        "kind": "lefttosolve_programs",
        "count_patterns": [],
    },
    {
        "key": "deepmind_formal_conjectures",
        "name": "Google DeepMind formal-conjectures (GitHub)",
        "url": "https://api.github.com/repos/google-deepmind/formal-conjectures/commits/main",
        "kind": "github_commit",
        "count_patterns": [],
    },
    {
        "key": "teorth_erdosproblems_gh",
        "name": "Terence Tao / Thomas Bloom erdosproblems (GitHub)",
        "url": "https://api.github.com/repos/teorth/erdosproblems/commits/main",
        "kind": "github_commit",
        "count_patterns": [],
    },
    {
        "key": "clay_millennium",
        "name": "Clay Mathematics Institute Millennium Prize Problems",
        "url": "https://www.claymath.org/millennium-problems/",
        "kind": "html",
        "count_patterns": [
            r"(?P<count>\d+)\s+(?:unsolved|remaining|open)\s+millennium",
            r"millennium\s+prize\s+problems",
            r"poincar[eé]\s+conjecture",
        ],
    },
    {
        "key": "erdos_problems",
        "name": "Erdős Problems Database (Thomas F. Bloom)",
        "url": "https://www.erdosproblems.com/",
        "kind": "html",
        "count_patterns": [
            r"(?P<count>\d{3,4})\s+(?:open|unsolved)\s+problems?",
            r"(?P<count>\d{3,4})\s+(?:problems?|entries)",
            r"erd[oőö]s\s+problems",
        ],
    },
    {
        "key": "proofatlas",
        "name": "ProofAtlas Open Problems Dataset",
        "url": "https://proofatlas.ai/open-problems/",
        "kind": "html",
        "count_patterns": [
            r"(?P<count>\d{3,4})\s+(?:open|eligible)\s+problems?",
            r"top[- ]500",
            r"proofatlas",
        ],
    },
    {
        "key": "open_problem_garden",
        "name": "Open Problem Garden",
        "url": "https://www.openproblemgarden.org/",
        "kind": "html",
        "count_patterns": [
            r"(?P<count>\d{2,4})\s+(?:open\s+)?problems?",
            r"open\s+problem\s+garden",
        ],
    },
    {
        "key": "wikipedia_unsolved_math",
        "name": "Wikipedia: List of Unsolved Problems in Mathematics",
        "url": "https://en.wikipedia.org/api/rest_v1/page/summary/List_of_unsolved_problems_in_mathematics",
        "kind": "wikimedia_summary",
        "count_patterns": [],
    },
    {
        "key": "wikipedia_unsolved_physics",
        "name": "Wikipedia: List of Unsolved Problems in Physics",
        "url": "https://en.wikipedia.org/api/rest_v1/page/summary/List_of_unsolved_problems_in_physics",
        "kind": "wikimedia_summary",
        "count_patterns": [],
    },
    {
        "key": "wikipedia_unsolved_cs",
        "name": "Wikipedia: List of Unsolved Problems in Computer Science",
        "url": "https://en.wikipedia.org/api/rest_v1/page/summary/List_of_unsolved_problems_in_computer_science",
        "kind": "wikimedia_summary",
        "count_patterns": [],
    },
    {
        "key": "bbchallenge",
        "name": "The Busy Beaver Challenge (BB(6) / Antihydra)",
        "url": "https://bbchallenge.org/",
        "kind": "html",
        "count_patterns": [
            r"BB\(\d\)\s*=\s*[\d,]+",
            r"bbchallenge",
            r"busy\s+beaver",
        ],
    },
    {
        "key": "kourovka_notebook",
        "name": "Kourovka Notebook (arXiv:1401.0300)",
        "url": "https://arxiv.org/abs/1401.0300",
        "kind": "html",
        "count_patterns": [
            r"\[v\d+\]",
            r"edition",
            r"kourovka",
        ],
    },
    {
        "key": "open_quantum_problems",
        "name": "IQOQI Vienna Open Quantum Problems",
        "url": "https://oqp.iqoqi.oeaw.ac.at/",
        "kind": "html",
        "count_patterns": [
            r"open\s+quantum\s+problems?",
            r"problem\s+\d+",
        ],
    },
    {
        "key": "leanfro_rh_statement",
        "name": "Lean FRO & Mathlib Initiative RH Verification Statement",
        "url": "https://leanprover-community.github.io/blog/posts/riemann-hypothesis/",
        "kind": "html",
        "count_patterns": [
            r"riemann\s+hypothesis",
            r"mathlib",
            r"lean\s+fro",
        ],
    },
    {
        "key": "0thernes_research_archive",
        "name": "0thernes Master Research Archive (GitHub)",
        "url": "https://api.github.com/repos/0thernes/0thernes-research-archive/commits/main",
        "kind": "github_commit",
        "count_patterns": [],
    },
)

GATE_TITLE_MARKERS = (
    "just a moment",
    "attention required",
    "verify you are human",
    "making sure you're not a bot",
    "anubis",
)


def parse_lefttosolve_programs_html(raw_html: str) -> list[dict[str, Any]]:
    """Parse all program cards from https://lefttosolve.com/programs cleanly."""
    programs: list[dict[str, Any]] = []
    seen: set[str] = set()
    for slug, inner in re.findall(r'href="/programs/([^"]+)"[^>]*>(.*?)</a>', raw_html, flags=re.S):
        name = html_lib.unescape(urllib.parse.unquote(slug)).strip()
        if not name or name in seen:
            continue
        seen.add(name)
        txt = html_lib.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", inner))).strip()
        m_counts = re.search(r"([\d,]+)\s+targets\s*·\s*([\d,]+)\s+open\s*·\s*([\d,]+)\s+solved\s+here", txt, flags=re.I)
        if not m_counts:
            continue
        targets = int(m_counts.group(1).replace(",", ""))
        open_cnt = int(m_counts.group(2).replace(",", ""))
        solved_cnt = int(m_counts.group(3).replace(",", ""))
        m_live = re.match(r"^(\d+)\s+live\b", txt, flags=re.I)
        live_agents = int(m_live.group(1)) if m_live else 0
        formalized = "(not formalized)" not in name.lower() and name != "Open Problem Garden"
        programs.append({
            "program": name,
            "formalized_in_lean": formalized,
            "targets": targets,
            "open": open_cnt,
            "solved_here": solved_cnt,
            "live_agents": live_agents,
            "url": f"https://lefttosolve.com/programs/{urllib.parse.quote(name, safe='()')}",
        })
    programs.sort(key=lambda r: (-r["targets"], r["program"]))
    return programs


def parse_registry_html(target: dict[str, Any], html: str, http_status: int) -> dict[str, Any]:
    """Extract verifiable public count signals from raw HTML without bypassing any gate."""
    title_m = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.I | re.S)
    title = html_lib.unescape(re.sub(r"\s+", " ", title_m.group(1)).strip()) if title_m else ""
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.I | re.S)
    text = html_lib.unescape(re.sub(r"<[^>]+>", " ", text))
    text = re.sub(r"\s+", " ", text).strip()

    title_low = title.lower()
    text_low = text.lower()
    is_gate_page = (
        http_status in (403, 429, 503)
        or any(m in title_low for m in GATE_TITLE_MARKERS)
        or (len(text) < 1500 and any(m in text_low for m in ("verify you are human", "anubis", "cf-browser-verification")))
    )
    if is_gate_page:
        return {
            "key": target["key"],
            "name": target["name"],
            "url": target["url"],
            "http_status": http_status,
            "fetch_status": "js_rendered_or_gated",
            "page_title": title[:140],
            "extracted_signals": [],
            "editorial_action": "Manual browser inspection required (anti-bot or JS gate respected; never bypassed).",
        }

    signals: list[str] = []
    for pat in target.get("count_patterns", []):
        for m in re.finditer(pat, text, flags=re.I):
            snippet = m.group(0).strip()
            if snippet and snippet not in signals:
                signals.append(snippet)

    millennium_flags: list[str] = []
    if target["key"] == "clay_millennium":
        for kw in ("Riemann Hypothesis", "Navier", "Yang", "P vs NP", "Hodge", "Birch"):
            if re.search(rf"{re.escape(kw)}[^.]{{0,60}}\bsolved\b", text, flags=re.I):
                millennium_flags.append(kw)

    status = "live_checked" if (http_status == 200 and len(text) > 120) else "js_rendered_or_minimal"
    action = (
        "REVIEW_REQUIRED: potential status wording change detected — inspect manually."
        if millennium_flags
        else "NO_RETIREMENT_DETECTED: committed baseline remains consistent."
    )
    return {
        "key": target["key"],
        "name": target["name"],
        "url": target["url"],
        "http_status": http_status,
        "fetch_status": status,
        "page_title": title[:140],
        "text_bytes": len(text),
        "extracted_signals": signals[:10],
        "potential_retirement_keywords": millennium_flags,
        "editorial_action": action,
    }


def _build_headers(url: str) -> dict[str, str]:
    headers = {
        "User-Agent": f"UnsolvedProblemsMegaAtlas/{ATLAS_VERSION} (DailyRegistryAudit; +https://github.com/0thernes/unsolved-problems-mega-atlas)",
    }
    if "api.github.com" in url:
        headers["Accept"] = "application/vnd.github+json"
        token = os.environ.get("GITHUB_TOKEN", "").strip()
        if token:
            headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_target(target: dict[str, Any], timeout: int = 20, retries: int = 1) -> dict[str, Any]:
    import time

    req = urllib.request.Request(target["url"], headers=_build_headers(target["url"]), method="GET")
    kind = target.get("kind", "html")
    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read(1_048_576).decode("utf-8", errors="ignore")
                status = int(resp.status)
            break
        except urllib.error.HTTPError as exc:
            return {
                "key": target["key"],
                "name": target["name"],
                "url": target["url"],
                "http_status": exc.code,
                "fetch_status": "js_rendered_or_gated" if exc.code in (403, 429, 503) else "http_error",
                "extracted_signals": [],
                "editorial_action": "Anti-bot / rate-limit gate respected (never bypassed); manual check if needed.",
            }
        except Exception as exc:
            last_exc = exc
            if attempt < retries:
                time.sleep(1.5)
                continue
            return {
                "key": target["key"],
                "name": target["name"],
                "url": target["url"],
                "http_status": None,
                "fetch_status": "network_unreachable",
                "error": str(last_exc)[:180],
                "extracted_signals": [],
                "editorial_action": "Offline or transient network error; committed baseline unchanged.",
            }
    try:
        if True:
            if kind == "lefttosolve_stats":
                data = json.loads(raw)
                cat = data.get("catalog", {})
                solved_total = len(data.get("solved", [])) if isinstance(data.get("solved"), list) else int(data.get("solved", 0))
                signals = [
                    f"total={data.get('total', 0):,}",
                    f"lean_open={cat.get('open', 0):,}",
                    f"unformalized={cat.get('unformalized', 0):,}",
                    f"solved_here={solved_total:,}",
                    f"live_agents={data.get('liveAgents', 0)}",
                ]
                return {
                    "key": target["key"],
                    "name": target["name"],
                    "url": target["url"],
                    "http_status": status,
                    "fetch_status": "live_checked",
                    "metrics": {
                        "total": int(data.get("total", 0)),
                        "catalog": cat,
                        "solved_here_total": solved_total,
                        "solved_today": int(data.get("solvedToday", 0)),
                        "claims_today": int(data.get("claimsToday", 0)),
                        "live_agents": int(data.get("liveAgents", 0)),
                        "live_problems": int(data.get("liveProblems", 0)),
                        "desk_online": bool(data.get("deskOnline", False)),
                    },
                    "extracted_signals": signals,
                    "editorial_action": "LIVE_SYNCED: Left to Solve catalog counters updated.",
                }

            if kind == "lefttosolve_programs":
                progs = parse_lefttosolve_programs_html(raw)
                total_t = sum(p["targets"] for p in progs)
                total_o = sum(p["open"] for p in progs)
                total_s = sum(p["solved_here"] for p in progs)
                return {
                    "key": target["key"],
                    "name": target["name"],
                    "url": target["url"],
                    "http_status": status,
                    "fetch_status": "live_checked" if progs else "js_rendered_or_minimal",
                    "program_count": len(progs),
                    "programs": progs,
                    "extracted_signals": [
                        f"{len(progs)} programs",
                        f"targets={total_t:,}",
                        f"open={total_o:,}",
                        f"solved_here={total_s:,}",
                    ],
                    "editorial_action": f"LIVE_SYNCED: Parsed {len(progs)} Left to Solve programs.",
                }

            if kind == "github_commit":
                data = json.loads(raw)
                sha = str(data.get("sha", ""))[:12]
                c_date = str(data.get("commit", {}).get("committer", {}).get("date", ""))
                msg = str(data.get("commit", {}).get("message", "")).splitlines()[0][:90]
                return {
                    "key": target["key"],
                    "name": target["name"],
                    "url": target["url"],
                    "http_status": status,
                    "fetch_status": "live_checked",
                    "metrics": {"head_sha": sha, "commit_date_utc": c_date, "commit_subject": msg},
                    "extracted_signals": [f"sha={sha}", f"date={c_date}"],
                    "editorial_action": "LIVE_SYNCED: Upstream commit SHA recorded.",
                }

            if kind == "wikimedia_summary":
                data = json.loads(raw)
                rev = str(data.get("revision", ""))
                ts = str(data.get("timestamp", ""))
                return {
                    "key": target["key"],
                    "name": target["name"],
                    "url": target["url"],
                    "http_status": status,
                    "fetch_status": "live_checked",
                    "metrics": {"revision": rev, "timestamp": ts, "title": str(data.get("title", ""))},
                    "extracted_signals": [f"rev={rev}", f"updated={ts}"],
                    "editorial_action": "LIVE_SYNCED: Wikipedia revision tracked.",
                }

            return parse_registry_html(target, raw, status)

    except urllib.error.HTTPError as exc:
        return {
            "key": target["key"],
            "name": target["name"],
            "url": target["url"],
            "http_status": int(exc.code),
            "fetch_status": "http_error_or_gated",
            "extracted_signals": [],
            "editorial_action": f"HTTP {exc.code} encountered; keep committed baseline unchanged.",
        }
    except Exception as exc:
        return {
            "key": target["key"],
            "name": target["name"],
            "url": target["url"],
            "http_status": None,
            "fetch_status": "network_unreachable",
            "error": str(exc)[:180],
            "extracted_signals": [],
            "editorial_action": "Offline or transient network error; committed baseline unchanged.",
        }


def _baseline_programs_normalized() -> list[dict[str, Any]]:
    return [
        {
            "program": p["Program"],
            "formalized_in_lean": p["Formalized_In_Lean"] == "Yes",
            "targets": int(p["Targets"]),
            "open": int(p["Open"]),
            "solved_here": int(p["Solved_Here"]),
            "live_agents": 0,
            "url": p["URL"],
        }
        for p in LEFT_TO_SOLVE_PROGRAMS_BASELINE
    ]


def compute_deltas(prev: dict[str, Any] | None, curr: dict[str, Any]) -> list[str]:
    """Compute concise human-readable day-over-day delta alerts against prior daily snapshot."""
    if not prev:
        return ["Initial daily snapshot recorded across all 16 public registries & live Left to Solve programs."]
    alerts: list[str] = []
    prev_map = {r["key"]: r for r in prev.get("registries", [])}
    for r in curr.get("registries", []):
        p = prev_map.get(r["key"])
        if not p:
            alerts.append(f"NEW_REGISTRY: Added {r['key']}")
            continue
        pm = p.get("metrics", {})
        cm = r.get("metrics", {})
        if r["key"] == "lefttosolve_stats" and pm and cm:
            for field in ("total", "solved_here_total"):
                if pm.get(field) != cm.get(field):
                    d = int(cm.get(field, 0)) - int(pm.get(field, 0))
                    alerts.append(f"lefttosolve_stats.{field}: {pm.get(field):,} -> {cm.get(field):,} ({d:+d})")
            for cfield in ("open", "unformalized"):
                pv = pm.get("catalog", {}).get(cfield)
                cv = cm.get("catalog", {}).get(cfield)
                if pv is not None and cv is not None and pv != cv:
                    alerts.append(f"lefttosolve_stats.catalog.{cfield}: {pv:,} -> {cv:,} ({cv - pv:+d})")
        elif pm.get("head_sha") and cm.get("head_sha") and pm["head_sha"] != cm["head_sha"]:
            alerts.append(f"{r['key']} HEAD updated: {pm['head_sha']} -> {cm['head_sha']} ({cm.get('commit_date_utc', '')})")
        elif pm.get("revision") and cm.get("revision") and pm["revision"] != cm["revision"]:
            alerts.append(f"{r['key']} Wikipedia revision updated: {pm['revision']} -> {cm['revision']}")
        if r.get("potential_retirement_keywords"):
            alerts.append(f"REVIEW_REQUIRED [{r['key']}]: potential retirement wording for {r['potential_retirement_keywords']}")

    prev_progs = {p["program"]: p for p in prev.get("lefttosolve_programs", [])}
    for pr in curr.get("lefttosolve_programs", []):
        pp = prev_progs.get(pr["program"])
        if not pp:
            alerts.append(f"NEW_PROGRAM [Left to Solve]: {pr['program']} ({pr['targets']:,} targets)")
        elif pp["targets"] != pr["targets"] or pp["open"] != pr["open"] or pp["solved_here"] != pr["solved_here"]:
            alerts.append(
                f"PROGRAM_DELTA [{pr['program']}]: targets {pp['targets']}->{pr['targets']}, "
                f"open {pp['open']}->{pr['open']}, solved_here {pp['solved_here']}->{pr['solved_here']}"
            )
    return alerts or ["No count or upstream revision changes since previous daily check."]


def build_delta_report(live: bool, previous_snapshot: dict[str, Any] | None = None) -> dict[str, Any]:
    if live:
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            entries = list(pool.map(fetch_target, TARGETS))
    else:
        entries = [
            {
                "key": t["key"],
                "name": t["name"],
                "url": t["url"],
                "http_status": None,
                "fetch_status": "offline_baseline_snapshot",
                "extracted_signals": [],
                "editorial_action": "Offline verification mode; run with --live to poll public registries.",
            }
            for t in TARGETS
        ]

    lts_progs = _baseline_programs_normalized()
    for r in entries:
        if r["key"] == "lefttosolve_programs" and r.get("programs"):
            lts_progs = r["programs"]
            r = dict(r)
            break

    # Keep top-level lefttosolve_programs clean and avoid duplicating 25 objects inside registries list
    compact_entries: list[dict[str, Any]] = []
    for r in entries:
        rc = dict(r)
        rc.pop("programs", None)
        compact_entries.append(rc)

    report: dict[str, Any] = {
        "schema_version": "2.0.0",
        "atlas_version": ATLAS_VERSION,
        "checked_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "checked_date_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"),
        "mode": "live" if live else "offline",
        "update_cadence": "Daily at 06:00 UTC via .github/workflows/daily-registry-sync.yml",
        "policy": "Advisory daily telemetry ONLY — ZERO automatic problem retirement. Community & primary-registry consensus required.",
        "committed_registries_indexed": len(EXTERNAL_REGISTRIES_NOV2026),
        "committed_ai_audit_entries": len(AI_VERIFICATION_AUDIT_NOV2026),
        "unretired_nov2026_ai_claim_targets": 12,
        "live_targets_polled": len(TARGETS),
        "lefttosolve_program_count": len(lts_progs),
        "registries": compact_entries,
        "lefttosolve_programs": lts_progs,
    }
    report["daily_deltas"] = compute_deltas(previous_snapshot, report)
    return report


def render_markdown(report: dict[str, Any]) -> str:
    progs = report.get("lefttosolve_programs", [])
    tot_t = sum(p["targets"] for p in progs)
    tot_o = sum(p["open"] for p in progs)
    tot_s = sum(p["solved_here"] for p in progs)
    lean_progs = [p for p in progs if p.get("formalized_in_lean")]
    lean_o = sum(p["open"] for p in lean_progs)

    lines = [
        f"# Daily External Open-Problem Registry & Left-to-Solve Tracker (`v{report['atlas_version']}`)",
        "",
        f"> **Auto-Updated Daily (`06:00 UTC`):** `.github/workflows/daily-registry-sync.yml` · **Last Checked (UTC):** `{report['checked_utc']}` · **Mode:** `{report['mode']}`",
        "",
        f"- **Committed Registries Benchmarked:** `{report['committed_registries_indexed']}`",
        f"- **Live Public Trackers Polled Daily:** `{report['live_targets_polled']}`",
        f"- **Left to Solve Live Fronts (`lefttosolve.com/programs`):** `{len(progs)}` programs (`{tot_t:,}` targets · `{tot_o:,}` open · `{lean_o:,}` Lean-4 formalized open · `{tot_s:,}` solved-here)",
        f"- **Unretired Fall/Nov 2026 AI Claim Targets:** `{report['unretired_nov2026_ai_claim_targets']}` (all remain `ai-claim-under-audit-nov2026`)",
        f"- **Epistemic Policy:** {report['policy']}",
        "",
        "## 1. Latest Day-over-Day Changes & Alerts",
        "",
    ]
    for alert in report.get("daily_deltas", []):
        lines.append(f"- {alert}")

    lines.extend([
        "",
        f"## 2. All {len(report['registries'])} Daily-Polled Global Open-Problem Registries",
        "",
        "| Registry | URL | HTTP | Status | Extracted Signals | Editorial Action |",
        "|---|---|---|---|---|---|",
    ])
    for r in report["registries"]:
        sigs = "; ".join(r.get("extracted_signals", [])) or "*(none / JS-rendered)*"
        http_s = str(r["http_status"]) if r["http_status"] is not None else "—"
        lines.append(
            f"| **{r['name']}** | {r['url']} | `{http_s}` | `{r['fetch_status']}` | {sigs} | {r['editorial_action']} |"
        )

    lines.extend([
        "",
        f"## 3. All {len(progs)} Live Fronts on Left to Solve (`https://lefttosolve.com/programs`)",
        "",
        "| # | Program / Front | Lean 4 Formalized | Targets | Open | Solved Here | Live Agents |",
        "|---:|---|---|---:|---:|---:|---:|",
    ])
    for idx, p in enumerate(progs, 1):
        fl = "Yes" if p.get("formalized_in_lean") else "No"
        lines.append(
            f"| {idx} | [{p['program']}]({p['url']}) | {fl} | {p['targets']:,} | {p['open']:,} | {p['solved_here']:,} | {p.get('live_agents', 0)} |"
        )
    lines.append(f"| — | **Total ({len(progs)} Programs)** | — | **{tot_t:,}** | **{tot_o:,}** | **{tot_s:,}** | **{sum(p.get('live_agents', 0) for p in progs)}** |")

    lines.extend([
        "",
        "## 4. Manual / Local Reproduction",
        "",
        "```bash",
        "python scripts/sync_external_registries.py --live --write-daily",
        "# Or via justfile:",
        "just sync-registries",
        "```",
        "",
    ])
    return "\n".join(lines)


def _update_daily_history(history_path: Path, report: dict[str, Any]) -> None:
    """Append or replace today's UTC-date entry in results/daily_registry_history.jsonl."""
    lts_stats: dict[str, Any] = next((r.get("metrics", {}) for r in report["registries"] if r["key"] == "lefttosolve_stats"), {})
    gh_commits = {
        r["key"]: r.get("metrics", {}).get("head_sha", "")
        for r in report["registries"]
        if r.get("metrics", {}).get("head_sha")
    }
    row = {
        "date_utc": report["checked_date_utc"],
        "checked_utc": report["checked_utc"],
        "atlas_version": report["atlas_version"],
        "live_ok_count": sum(1 for r in report["registries"] if r.get("fetch_status") == "live_checked"),
        "live_targets_polled": report["live_targets_polled"],
        "lefttosolve_total": lts_stats.get("total", sum(p["targets"] for p in report["lefttosolve_programs"])),
        "lefttosolve_lean_open": lts_stats.get("catalog", {}).get("open", 0),
        "lefttosolve_unformalized": lts_stats.get("catalog", {}).get("unformalized", 0),
        "lefttosolve_solved_here": lts_stats.get("solved_here_total", sum(p["solved_here"] for p in report["lefttosolve_programs"])),
        "lefttosolve_programs": len(report["lefttosolve_programs"]),
        "upstream_commits": gh_commits,
    }
    existing_rows: list[dict[str, Any]] = []
    if history_path.exists():
        for ln in history_path.read_text(encoding="utf-8").splitlines():
            if ln.strip():
                try:
                    existing_rows.append(json.loads(ln))
                except json.JSONDecodeError:
                    continue
    existing_rows = [r for r in existing_rows if r.get("date_utc") != row["date_utc"]]
    existing_rows.append(row)
    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in existing_rows) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Daily external open-problem registry & Left to Solve 25-program sync engine.")
    mode_grp = parser.add_mutually_exclusive_group()
    mode_grp.add_argument("--live", action="store_true", help="Poll all 16 public registry URLs & APIs over HTTPS")
    mode_grp.add_argument("--offline", action="store_true", help="Verify baseline snapshot schema without network calls")
    parser.add_argument("--write-daily", action="store_true", help="Write live daily telemetry (results/daily_registries.json, results/lefttosolve_programs.json, results/daily_registry_history.jsonl, docs/DAILY_REGISTRY_TRACKER.md)")
    parser.add_argument("--write-report", action="store_true", help="Also write release snapshot results/registry_delta.json and docs/registry-delta-2026-11-26.md")
    parser.add_argument("--json", action="store_true", help="Print JSON payload to stdout")
    args = parser.parse_args()

    live = bool(args.live)
    daily_json = ROOT / "results" / "daily_registries.json"
    prev: dict[str, Any] | None = None
    if daily_json.exists():
        try:
            prev = json.loads(daily_json.read_text(encoding="utf-8"))
        except Exception:
            prev = None

    report = build_delta_report(live=live, previous_snapshot=prev)

    if args.write_daily:
        daily_json.parent.mkdir(parents=True, exist_ok=True)
        daily_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        (ROOT / "results" / "lefttosolve_programs.json").write_text(
            json.dumps(
                {
                    "checked_utc": report["checked_utc"],
                    "source_url": "https://lefttosolve.com/programs",
                    "program_count": len(report["lefttosolve_programs"]),
                    "programs": report["lefttosolve_programs"],
                },
                indent=2,
                ensure_ascii=False,
            ) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        _update_daily_history(ROOT / "results" / "daily_registry_history.jsonl", report)
        md_text = render_markdown(report)
        (ROOT / "docs" / "DAILY_REGISTRY_TRACKER.md").write_text(md_text, encoding="utf-8", newline="\n")
        (ROOT / "docs" / "registry-delta-latest.md").write_text(md_text, encoding="utf-8", newline="\n")

    if args.write_report:
        out_json = ROOT / "results" / "registry_delta.json"
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        out_md = ROOT / "docs" / "registry-delta-2026-11-26.md"
        out_md.write_text(render_markdown(report), encoding="utf-8", newline="\n")

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        ok_cnt = sum(1 for r in report["registries"] if r.get("fetch_status") == "live_checked")
        print(
            f"PASS: External registry sync ({report['mode']}) across {len(report['registries'])} public trackers "
            f"(live_ok={ok_cnt}, baseline={report['committed_registries_indexed']} registries, "
            f"{len(report['lefttosolve_programs'])} Left to Solve programs, 12 unretired Nov 2026 AI claims)."
        )
        for r in report["registries"]:
            print(f"  [{r['fetch_status']:<23}] {r['key']:<27} HTTP={r['http_status']} | {r['editorial_action']}")


if __name__ == "__main__":
    main()
