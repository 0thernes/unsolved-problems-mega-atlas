#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Daily mirror of the Left to Solve program lists (https://lefttosolve.com/programs).

Left to Solve publishes a read-only JSON catalogue at ``/api/problems`` (paged with
``limit``/``offset``, filterable with ``source``) and summary counts at
``/api/stats``. Its ``robots.txt`` allows everything except ``/api/desk/`` and
``/api/verdict``, which this script never touches.

What this script does
  * Pages through the full catalogue politely (identified User-Agent, fixed delay,
    bounded retries) and groups problems by program (the API ``source`` field).
  * Cross-checks every program count against the API's own per-source ``total``
    and refuses to write anything if the crawl is incomplete or inconsistent.
  * Stores metadata only: id, title, kind, fields, difficulty, prize, solved and a
    link back. Statement excerpts are not copied (many come from CC BY-SA sites);
    volatile fields (``liveAgents``, ``claimed``) are dropped so daily diffs show
    real catalogue changes only.
  * Writes one JSONL file per program (split if a file would exceed 4 MB, to stay
    under the repository's 5 MB tracked-file limit), a summary ``snapshot.json``
    (with ``by_kind`` and ``solved_by_kind`` disaggregation), a per-run delta,
    an append-only ``CHANGES.jsonl``, a candidate crosswalk to Mega-Atlas problems
    by exact normalised title (with ``kind`` and ``solved`` advisory flags), a
    browsable zero-CDN WCAG 2.2 AA ``index.html`` for GitHub Pages, a
    ``MANIFEST.sha256`` and ``docs/lefttosolve-programs.md``.

What it does not do
  * It never edits the frozen 1,900-problem Mega-Atlas dataset (``src/v2_data``,
    ``outputs/``) and never retires an Atlas problem. The mirror is a sidecar layer.
  * Crosswalk rows are automatic title matches, labelled as candidates, not
    curated identifications.

Usage
  python scripts/sync_lefttosolve.py --offline      # verify the committed mirror
  python scripts/sync_lefttosolve.py --rebuild      # rebuild derived summaries/HTML from committed JSONL
  python scripts/sync_lefttosolve.py --live         # crawl and rewrite the mirror
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import html
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "external" / "lefttosolve"
PROGRAM_DIR = OUT_DIR / "programs"
SNAPSHOT = OUT_DIR / "snapshot.json"
CHANGES = OUT_DIR / "CHANGES.jsonl"
CROSSWALK = OUT_DIR / "atlas_crosswalk.json"
HTML_INDEX = OUT_DIR / "index.html"
MANIFEST = OUT_DIR / "MANIFEST.sha256"
DELTA = ROOT / "results" / "lefttosolve_delta.json"
REPORT = ROOT / "docs" / "lefttosolve-programs.md"
ATLAS_CSV = ROOT / "outputs" / "MegaAtlas_Unsolved_Problems_V2.csv"

BASE = "https://lefttosolve.com"
PAGES_URL = "https://0thernes.github.io/unsolved-problems-mega-atlas/external/lefttosolve/"
API_PROBLEMS = BASE + "/api/problems"
API_STATS = BASE + "/api/stats"
USER_AGENT = "unsolved-problems-mega-atlas-sync/1.0 (+https://github.com/0thernes/unsolved-problems-mega-atlas; mailto:0_0@0thernes.art)"
PAGE_LIMIT = 200
REQUEST_DELAY_S = 0.35
MAX_RETRIES = 4
MAX_FILE_BYTES = 4 * 1024 * 1024
KEEP_FIELDS = ("id", "title", "kind", "fields", "difficulty", "prize", "solved")
KINDS = ("open", "known", "warmup", "unformalized")
SCHEMA_VERSION = "1.0.0"
MIN_COMPLETENESS = 0.995


class SyncError(RuntimeError):
    """Raised when the crawl is incomplete or inconsistent; nothing is written."""


def _get_json(url: str) -> Any:
    last: Exception | None = None
    for attempt in range(MAX_RETRIES):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                ctype = resp.headers.get("Content-Type", "")
                body = resp.read().decode("utf-8")
            if "json" not in ctype:
                raise SyncError(f"non-JSON response ({ctype!r}) from {url}; possibly gated, refusing to parse")
            return json.loads(body)
        except SyncError:
            raise
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ConnectionError) as exc:
            last = exc
            time.sleep(2.0 * (attempt + 1))
    raise SyncError(f"GET {url} failed after {MAX_RETRIES} attempts: {last}")


def slugify(name: str) -> str:
    text = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "unnamed"


def program_url(name: str) -> str:
    return f"{BASE}/programs/{urllib.parse.quote(name, safe='')}"


def problem_url(pid: str) -> str:
    return f"{BASE}/p/{urllib.parse.quote(pid, safe='.-_')}"


def normalise_item(raw: dict[str, Any]) -> dict[str, Any]:
    item = {k: raw.get(k) for k in KEEP_FIELDS}
    item["fields"] = sorted(item["fields"] or [])
    item["solved"] = bool(item["solved"])
    item["url"] = problem_url(str(item["id"]))
    return item


def crawl() -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    first = _get_json(f"{API_PROBLEMS}?limit={PAGE_LIMIT}&offset=0")
    total = int(first["total"])
    upstream = first.get("upstream") or {}
    by_id: dict[str, tuple[str, dict[str, Any]]] = {}
    offset = 0
    page = first
    while True:
        for raw in page.get("items", []):
            by_id[str(raw["id"])] = (str(raw.get("source") or "Unknown"), normalise_item(raw))
        offset += PAGE_LIMIT
        if offset >= total:
            break
        time.sleep(REQUEST_DELAY_S)
        page = _get_json(f"{API_PROBLEMS}?limit={PAGE_LIMIT}&offset={offset}")
    if len(by_id) < MIN_COMPLETENESS * total:
        raise SyncError(f"incomplete crawl: {len(by_id)} unique ids for reported total {total}")

    programs: dict[str, list[dict[str, Any]]] = {}
    for source, item in by_id.values():
        programs.setdefault(source, []).append(item)
    for items in programs.values():
        items.sort(key=lambda it: str(it["id"]))

    # Cross-check every program against the API's own per-source total.
    reported: dict[str, int] = {}
    for name in sorted(programs):
        time.sleep(REQUEST_DELAY_S)
        res = _get_json(f"{API_PROBLEMS}?limit=1&offset=0&source={urllib.parse.quote(name)}")
        reported[name] = int(res["total"])
        got = len(programs[name])
        if abs(got - reported[name]) > max(2, int(0.005 * reported[name])):
            raise SyncError(f"program {name!r}: fetched {got}, API reports {reported[name]}")

    time.sleep(REQUEST_DELAY_S)
    stats = _get_json(API_STATS)
    meta = {
        "reported_total": total,
        "fetched_total": len(by_id),
        "upstream": {"repo": upstream.get("repo"), "commit": upstream.get("commit")},
        "catalog": stats.get("catalog"),
        "reported_program_totals": reported,
    }
    return programs, meta


def _encode_lines(items: list[dict[str, Any]]) -> list[str]:
    return [json.dumps(it, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for it in items]


def write_program_files(programs: dict[str, list[dict[str, Any]]]) -> dict[str, list[str]]:
    PROGRAM_DIR.mkdir(parents=True, exist_ok=True)
    for old in PROGRAM_DIR.glob("*.jsonl"):
        old.unlink()
    files: dict[str, list[str]] = {}
    for name, items in sorted(programs.items()):
        slug = slugify(name)
        lines = _encode_lines(items)
        chunks: list[list[str]] = [[]]
        size = 0
        for line in lines:
            n = len(line.encode("utf-8"))
            if chunks[-1] and size + n > MAX_FILE_BYTES:
                chunks.append([])
                size = 0
            chunks[-1].append(line)
            size += n
        names = [f"{slug}.jsonl"] if len(chunks) == 1 else [f"{slug}.part-{i + 1:03d}.jsonl" for i in range(len(chunks))]
        for fname, chunk in zip(names, chunks):
            (PROGRAM_DIR / fname).write_text("".join(chunk), encoding="utf-8", newline="\n")
        files[name] = [f"programs/{f}" for f in names]
    return files


def load_committed() -> dict[str, dict[str, Any]]:
    """Return {id: item-with-program} from the committed mirror (empty if none)."""
    if not SNAPSHOT.exists():
        return {}
    snap = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    out: dict[str, dict[str, Any]] = {}
    for prog in snap.get("programs", []):
        for rel in prog.get("files", []):
            path = OUT_DIR / rel
            if not path.exists():
                continue
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    item = json.loads(line)
                    item["program"] = prog["program"]
                    out[str(item["id"])] = item
    return out


def load_committed_by_program() -> tuple[dict[str, list[dict[str, Any]]], dict[str, list[str]], dict[str, Any]]:
    """Load grouped program records, existing file paths, and snapshot metadata from disk."""
    if not SNAPSHOT.exists():
        raise SyncError("no committed mirror; run with --live first")
    snap = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    programs: dict[str, list[dict[str, Any]]] = {}
    files: dict[str, list[str]] = {}
    for prog in snap.get("programs", []):
        name = str(prog["program"])
        rel_files = list(prog.get("files", []))
        files[name] = rel_files
        items: list[dict[str, Any]] = []
        for rel in rel_files:
            path = OUT_DIR / rel
            if not path.exists():
                raise SyncError(f"missing committed shard {rel}")
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    items.append(json.loads(line))
        programs[name] = items
    return programs, files, snap


def _format_solved_by_kind(solved_by_kind: dict[str, int]) -> str:
    parts = [f"{k}: {v:,}" for k, v in solved_by_kind.items() if v > 0]
    return ", ".join(parts) if parts else "0"


def summarise(programs: dict[str, list[dict[str, Any]]], files: dict[str, list[str]]) -> list[dict[str, Any]]:
    rows = []
    for name, items in sorted(programs.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        by_kind = {k: 0 for k in KINDS}
        solved_by_kind = {k: 0 for k in KINDS}
        for it in items:
            kind = str(it["kind"])
            by_kind[kind] = by_kind.get(kind, 0) + 1
            if it["solved"]:
                solved_by_kind[kind] = solved_by_kind.get(kind, 0) + 1
        diffs = [it["difficulty"] for it in items if isinstance(it["difficulty"], (int, float))]
        fields: dict[str, int] = {}
        for it in items:
            for f in it["fields"]:
                fields[f] = fields.get(f, 0) + 1
        rows.append({
            "program": name,
            "slug": slugify(name),
            "url": program_url(name),
            "total": len(items),
            "by_kind": by_kind,
            "formalized_in_lean": len(items) - by_kind.get("unformalized", 0),
            "solved": sum(solved_by_kind.values()),
            "solved_by_kind": solved_by_kind,
            "with_prize": sum(1 for it in items if it["prize"]),
            "mean_difficulty": round(sum(diffs) / len(diffs), 2) if diffs else None,
            "top_fields": [f for f, _ in sorted(fields.items(), key=lambda kv: (-kv[1], kv[0]))[:5]],
            "files": files[name],
        })
    return rows


def aggregate_solved_by_kind(program_rows: list[dict[str, Any]]) -> dict[str, int]:
    totals = {k: 0 for k in KINDS}
    for row in program_rows:
        for k, v in row.get("solved_by_kind", {}).items():
            totals[k] = totals.get(k, 0) + int(v)
    return totals


def compute_delta(old: dict[str, dict[str, Any]], programs: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    new = {str(it["id"]): {**it, "program": name} for name, items in programs.items() for it in items}
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    common = set(new) & set(old)
    newly_solved = sorted(i for i in common if new[i]["solved"] and not old[i].get("solved"))
    kind_changes = sorted(i for i in common if new[i]["kind"] != old[i].get("kind"))
    moved = sorted(i for i in common if new[i]["program"] != old[i].get("program"))
    sample = 50
    return {
        "baseline_present": bool(old),
        "added": len(added), "removed": len(removed), "newly_solved": len(newly_solved),
        "kind_changes": len(kind_changes), "program_moves": len(moved),
        "added_sample": added[:sample], "removed_sample": removed[:sample],
        "newly_solved_ids": newly_solved[:500],
        "kind_change_sample": [{"id": i, "from": old[i].get("kind"), "to": new[i]["kind"]} for i in kind_changes[:sample]],
    }


_STOP = {"the", "a", "an", "of", "on", "for", "and", "conjecture", "problem", "hypothesis", "question"}


def norm_title(text: str) -> str:
    text = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode("ascii").lower()
    text = re.sub(r"\([^)]*\)", " ", text)
    words = [w for w in re.findall(r"[a-z0-9]+", text) if w not in _STOP]
    return " ".join(words)


def _load_atlas_titles() -> list[tuple[str, str]]:
    """Load (id, name) pairs from v2_loader, falling back to UTF-8-BOM-safe CSV."""
    sys.path.insert(0, str(ROOT / "src"))
    try:
        from v2_loader import load_v2_master  # noqa: PLC0415

        df = load_v2_master()["df"]
        return [(str(r["id"]), str(r["name"])) for _, r in df[["id", "name"]].iterrows()]
    except Exception:
        if not ATLAS_CSV.exists():
            raise
        with ATLAS_CSV.open("r", encoding="utf-8-sig", newline="") as fh:
            return [(str(row["id"]), str(row["name"])) for row in csv.DictReader(fh)]


def build_crosswalk(programs: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    try:
        atlas = _load_atlas_titles()
    except Exception as exc:  # pragma: no cover - environment without atlas data
        return {"status": "skipped", "reason": f"atlas loader unavailable: {exc}", "matches": []}
    index: dict[str, list[tuple[str, str, str, str, bool]]] = {}
    for name, items in programs.items():
        for it in items:
            key = norm_title(it["title"] or "")
            if len(key) >= 6:
                index.setdefault(key, []).append(
                    (str(it["id"]), str(it["title"]), name, str(it["kind"]), bool(it["solved"]))
                )
    matches = []
    solved_signals: list[dict[str, Any]] = []
    for aid, aname in atlas:
        key = norm_title(aname)
        hits = index.get(key, [])
        if hits and len(key) >= 6:
            cands = [
                {
                    "id": h[0],
                    "title": h[1],
                    "program": h[2],
                    "kind": h[3],
                    "solved": h[4],
                    "url": problem_url(h[0]),
                }
                for h in sorted(hits)[:10]
            ]
            matches.append({
                "atlas_id": aid,
                "atlas_name": aname,
                "match_type": "exact-normalised-title (candidate)",
                "lefttosolve": cands,
            })
            for c in cands:
                if c["solved"]:
                    solved_signals.append({
                        "atlas_id": aid,
                        "atlas_name": aname,
                        "lts_id": c["id"],
                        "lts_title": c["title"],
                        "program": c["program"],
                        "kind": c["kind"],
                        "url": c["url"],
                    })
    return {
        "status": "ok",
        "method": "exact match after NFKD, lowercase, parenthetical and stop-word removal",
        "policy": (
            "Advisory only. A Left to Solve 'solved' flag never modifies the status of any "
            "curated Mega-Atlas problem; matching solved flags are listed under "
            "external_solved_signals for human review."
        ),
        "atlas_problems": len(atlas),
        "matched_atlas_problems": len(matches),
        "external_solved_signals": solved_signals,
        "matches": matches,
    }


def write_manifest() -> None:
    lines = []
    for path in sorted(OUT_DIR.rglob("*")):
        if path.is_file() and path.name != "MANIFEST.sha256":
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            lines.append(f"{digest}  {path.relative_to(OUT_DIR).as_posix()}\n")
    MANIFEST.write_text("".join(lines), encoding="utf-8", newline="\n")


def _load_recent_changes(limit: int = 10) -> list[dict[str, Any]]:
    if not CHANGES.exists():
        return []
    rows = [json.loads(line) for line in CHANGES.read_text(encoding="utf-8").splitlines() if line.strip()]
    return rows[-limit:][::-1]


def render_report(snap: dict[str, Any], delta: dict[str, Any], crosswalk: dict[str, Any]) -> str:
    cat = snap.get("catalog") or {}
    sbk = snap.get("solved_by_kind") or aggregate_solved_by_kind(snap.get("programs", []))
    total_solved = sum(sbk.values())
    signals = crosswalk.get("external_solved_signals") or []
    out = [
        "<!-- SPDX-License-Identifier: CC-BY-4.0 -->",
        "# Left to Solve program lists (daily mirror)",
        "",
        "Generated by `scripts/sync_lefttosolve.py`; do not edit by hand. "
        f"Source: <{BASE}/programs> · Browsable GitHub Pages mirror: <{PAGES_URL}>.",
        "Problem statements live on Left to Solve and in [google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures); this mirror keeps metadata and links only.",
        "",
        f"- **Retrieved (UTC):** `{snap['retrieved_utc']}`",
        f"- **Problems:** {snap['fetched_total']:,} fetched of {snap['reported_total']:,} reported, in {len(snap['programs'])} programs",
        f"- **Catalogue counts (`/api/stats`):** open {cat.get('open', '?'):,} · known {cat.get('known', '?'):,} · warmup {cat.get('warmup', '?'):,} · unformalized {cat.get('unformalized', '?'):,}"
        if cat else "- **Catalogue counts:** unavailable",
        f"- **Flagged `solved` on Left to Solve ({total_solved:,} total):** {_format_solved_by_kind(sbk)} "
        "(Left to Solve's own Lean checker flag; mostly `known`/`warmup` theorems, not re-verified here)",
        f"- **Upstream formal-conjectures commit:** `{(snap.get('upstream') or {}).get('commit')}`",
        f"- **Change since previous snapshot:** +{delta['added']:,} added, −{delta['removed']:,} removed, {delta['newly_solved']:,} newly solved, {delta['kind_changes']:,} kind changes"
        + ("" if delta.get("baseline_present", True) else " (first snapshot)"),
        f"- **Candidate Atlas crosswalk:** {snap.get('crosswalk_matches', 0)} Mega-Atlas problems share an exact normalised title with a Left to Solve problem "
        f"(`data/external/lefttosolve/atlas_crosswalk.json`; automatic, not curated; {len(signals)} candidate link(s) carry a Left to Solve `solved` flag; zero Atlas statuses changed)",
        "",
        "| Program | Total | `open` | Lean-stated | Unformalized | Solved (by kind) | Mean difficulty | Top fields |",
        "|---|---:|---:|---:|---:|---|---:|---|",
    ]
    for p in snap["programs"]:
        md = "—" if p["mean_difficulty"] is None else f"{p['mean_difficulty']}"
        psbk = _format_solved_by_kind(p.get("solved_by_kind") or {})
        out.append(
            f"| [{p['program']}]({p['url']}) | {p['total']:,} | {p['by_kind'].get('open', 0):,} | "
            f"{p['formalized_in_lean']:,} | {p['by_kind'].get('unformalized', 0):,} | "
            f"{psbk} | {md} | {', '.join(p['top_fields']) or '—'} |"
        )
    out += [
        "",
        "## Field semantics",
        "",
        "- `open` marks a problem Left to Solve classifies as open; `known` marks a statement whose answer is already known in the literature but formalized as a Lean proof target; `warmup` marks a smaller companion exercise; `unformalized` marks an entry without an upstream Lean statement.",
        "- `Lean-stated` counts `open + known + warmup`. `Solved (by kind)` reports Left to Solve's own checker flag disaggregated by kind (for example, Millennium Prize `warmup: 2` reflects warmup targets, not solved Millennium Prize problems). Nothing here is re-verified by this repository.",
        "",
        "## Provenance, licensing & limits",
        "",
        "- **Source & crawl etiquette:** Public endpoints `/api/problems` and `/api/stats` at <https://lefttosolve.com>, allowed by its `robots.txt`. Disallowed paths `/api/desk/` and `/api/verdict` are never requested. Requests are sequential with fixed delay and back-off.",
        "- **Upstream sources & licensing:** Left to Solve draws Lean statements from `google-deepmind/formal-conjectures` (`Apache-2.0`), Erdős metadata from `teorth/erdosproblems`, descriptions from Wikipedia (`CC BY-SA 4.0`) and links from Open Problem Garden; MathOverflow, Mathematics Stack Exchange and OEIS titles are `CC BY-SA 4.0`. Left to Solve publishes no licence for its aggregate catalogue.",
        "- **Scope & carve-out:** `data/external/lefttosolve/` stores identifiers, titles, program membership, status flags and links only — no statement excerpts are copied. Third-party titles remain under their upstream sources' licences; `data/external/lefttosolve/` is **not** covered by this repository's `CC-BY-4.0` data licence (see [`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md)). Entries are removed on request.",
        "- **Non-affiliation:** Not affiliated with Left to Solve or any of its upstream sources. This sidecar never modifies the frozen 1,900-problem Mega-Atlas dataset or retires any problem.",
        "",
        "## Reproduction",
        "",
        "```bash",
        "python scripts/sync_lefttosolve.py --live     # crawl (about 330 requests, ~5–15 min)",
        "python scripts/sync_lefttosolve.py --rebuild  # regenerate derived views from committed JSONL",
        "python scripts/sync_lefttosolve.py --offline  # verify the committed mirror",
        "```",
        "",
    ]
    return "\n".join(out)


def render_html(
    snap: dict[str, Any],
    delta: dict[str, Any],
    crosswalk: dict[str, Any],
    changes: list[dict[str, Any]],
) -> str:
    esc = html.escape
    cat = snap.get("catalog") or {}
    sbk = snap.get("solved_by_kind") or aggregate_solved_by_kind(snap.get("programs", []))
    total_solved = sum(sbk.values())
    upstream = snap.get("upstream") or {}
    commit = str(upstream.get("commit") or "")
    commit_short = commit[:12] if commit else "—"
    repo_url = str(upstream.get("repo") or "https://github.com/google-deepmind/formal-conjectures")

    prog_rows: list[str] = []
    for p in snap["programs"]:
        md = "—" if p["mean_difficulty"] is None else f"{p['mean_difficulty']}"
        psbk = _format_solved_by_kind(p.get("solved_by_kind") or {})
        shards = " ".join(
            f'<a href="{esc(rel)}">[{i + 1}]</a>' for i, rel in enumerate(p["files"])
        )
        fields_str = ", ".join(p.get("top_fields") or []) or "—"
        prog_rows.append(
            "<tr>"
            f'<th scope="row"><a href="{esc(p["url"])}" rel="noopener noreferrer">{esc(p["program"])}</a></th>'
            f'<td class="num">{p["total"]:,}</td>'
            f'<td class="num">{p["by_kind"].get("open", 0):,}</td>'
            f'<td class="num">{p["formalized_in_lean"]:,}</td>'
            f'<td class="num">{p["by_kind"].get("unformalized", 0):,}</td>'
            f"<td>{esc(psbk)}</td>"
            f'<td class="num">{esc(md)}</td>'
            f"<td>{esc(fields_str)}</td>"
            f"<td>{shards}</td>"
            "</tr>"
        )

    cw_rows: list[str] = []
    for m in crosswalk.get("matches", []):
        links = []
        for c in m.get("lefttosolve", []):
            tag = f"{c.get('kind', '?')}" + (" · solved on LtS" if c.get("solved") else "")
            links.append(
                f'<li><a href="{esc(c["url"])}" rel="noopener noreferrer">{esc(c["title"])}</a> '
                f'<span class="meta">({esc(c["program"])} · {esc(tag)})</span></li>'
            )
        cw_rows.append(
            "<tr>"
            f'<th scope="row"><code>{esc(m["atlas_id"])}</code></th>'
            f"<td>{esc(m['atlas_name'])}</td>"
            f'<td><ul class="compact">{"".join(links)}</ul></td>'
            "</tr>"
        )

    ch_rows: list[str] = []
    for row in changes:
        ch_rows.append(
            "<tr>"
            f'<td><code>{esc(str(row.get("retrieved_utc", "")))}</code></td>'
            f'<td class="num">{int(row.get("reported_total", 0)):,}</td>'
            f'<td class="num">+{int(row.get("added", 0)):,}</td>'
            f'<td class="num">−{int(row.get("removed", 0)):,}</td>'
            f'<td class="num">{int(row.get("newly_solved", 0)):,}</td>'
            f'<td class="num">{int(row.get("kind_changes", 0)):,}</td>'
            "</tr>"
        )

    signals = crosswalk.get("external_solved_signals") or []
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src 'self' data:; base-uri 'none'; form-action 'none'">
<meta name="referrer" content="no-referrer">
<title>Left to Solve Programs — Daily Mirror · Unsolved Problems Mega-Atlas</title>
<style>
:root {{ color-scheme: light dark; --bg: #ffffff; --fg: #14171a; --muted: #525d68; --card: #f5f7fa; --border: #d0d7de; --accent: #0969da; --warn-bg: #fff8c5; --warn-fg: #4d2d00; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg: #0d1117; --fg: #e6edf3; --muted: #9198a1; --card: #161b22; --border: #30363d; --accent: #58a6ff; --warn-bg: #3b2e00; --warn-fg: #f8e3a1; }} }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; line-height: 1.5; background: var(--bg); color: var(--fg); }}
.skip {{ position: absolute; left: -9999px; }}
.skip:focus {{ position: static; display: inline-block; padding: 0.5rem 1rem; background: var(--accent); color: #fff; }}
header, main, footer {{ max-width: 1220px; margin: 0 auto; padding: 1.25rem 1.25rem; }}
header {{ border-bottom: 1px solid var(--border); }}
nav a {{ margin-right: 1rem; color: var(--accent); text-decoration: none; font-weight: 600; }}
nav a:hover {{ text-decoration: underline; }}
h1 {{ margin: 0.5rem 0 0.25rem; font-size: 1.65rem; }}
h2 {{ margin-top: 2rem; font-size: 1.25rem; border-bottom: 1px solid var(--border); padding-bottom: 0.3rem; }}
.subtitle {{ color: var(--muted); margin: 0 0 0.75rem; }}
.notice {{ background: var(--warn-bg); color: var(--warn-fg); border: 1px solid var(--border); border-radius: 6px; padding: 0.75rem 1rem; margin: 1rem 0; font-size: 0.94rem; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(175px, 1fr)); gap: 0.75rem; margin: 1rem 0; }}
.card {{ background: var(--card); border: 1px solid var(--border); border-radius: 6px; padding: 0.75rem 0.9rem; }}
.card .k {{ font-size: 0.8rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.03em; }}
.card .v {{ font-size: 1.35rem; font-weight: 700; margin-top: 0.15rem; }}
.card .s {{ font-size: 0.82rem; color: var(--muted); }}
.controls {{ display: flex; flex-wrap: wrap; gap: 0.75rem; align-items: center; margin: 0.75rem 0; }}
input[type="search"] {{ padding: 0.45rem 0.7rem; border: 1px solid var(--border); border-radius: 6px; background: var(--bg); color: var(--fg); min-width: 260px; font-size: 0.95rem; }}
.table-wrap {{ overflow-x: auto; }}
table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
th, td {{ border-bottom: 1px solid var(--border); padding: 0.5rem 0.6rem; text-align: left; vertical-align: top; }}
thead th {{ background: var(--card); position: sticky; top: 0; }}
.num {{ text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }}
a {{ color: var(--accent); }}
code {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.86em; }}
.meta {{ color: var(--muted); font-size: 0.85em; }}
ul.compact {{ margin: 0; padding-left: 1.1rem; }}
footer {{ border-top: 1px solid var(--border); color: var(--muted); font-size: 0.88rem; margin-top: 2rem; }}
</style>
</head>
<body>
<a class="skip" href="#main-content">Skip to main content</a>
<header>
  <nav aria-label="Atlas navigation">
    <a href="../../">Interactive Web Atlas (1,900 Problems)</a>
    <a href="../../blueprint/">Lean 4.35.0 Proof Blueprint</a>
    <a href="https://github.com/0thernes/unsolved-problems-mega-atlas" rel="noopener noreferrer">GitHub Repository</a>
    <a href="{esc(BASE)}/programs" rel="noopener noreferrer">Left to Solve Upstream</a>
  </nav>
  <h1>Left to Solve Program Lists — Daily Mirror</h1>
  <p class="subtitle">
    Sidecar metadata index of all <strong>{len(snap["programs"])}</strong> programs at
    <a href="{esc(BASE)}/programs" rel="noopener noreferrer">lefttosolve.com/programs</a>,
    refreshed daily by GitHub Actions (<code>07:23 UTC</code>).
    Retrieved <code>{esc(str(snap["retrieved_utc"]))}</code> ·
    Upstream <a href="{esc(repo_url)}" rel="noopener noreferrer"><code>formal-conjectures</code></a> @ <code>{esc(commit_short)}</code>.
  </p>
</header>

<main id="main-content">
  <div class="notice" role="note">
    <strong>Epistemic &amp; licensing boundary:</strong> This mirror stores metadata and links only (no problem statements or excerpts) and is a sidecar — it never modifies the frozen 1,900-problem Mega-Atlas dataset or retires any problem.
    Left to Solve&rsquo;s <code>solved</code> flags reflect its own Lean checker (mostly <code>known</code> and <code>warmup</code> targets) and are not re-verified here.
    Third-party titles retain their upstream sources&rsquo; licences and are not covered by this repository&rsquo;s CC-BY-4.0 data licence.
  </div>

  <section aria-label="Summary statistics" class="grid">
    <div class="card"><div class="k">Programs</div><div class="v">{len(snap["programs"]):,}</div><div class="s">All listed programs</div></div>
    <div class="card"><div class="k">Mirrored Targets</div><div class="v">{snap["fetched_total"]:,}</div><div class="s">of {snap["reported_total"]:,} reported</div></div>
    <div class="card"><div class="k">Kind: open</div><div class="v">{cat.get("open", 0):,}</div><div class="s">Lean-stated open targets</div></div>
    <div class="card"><div class="k">Known / Warmup</div><div class="v">{cat.get("known", 0):,} / {cat.get("warmup", 0):,}</div><div class="s">Unformalized: {cat.get("unformalized", 0):,}</div></div>
    <div class="card"><div class="k">Flagged Solved (LtS)</div><div class="v">{total_solved:,}</div><div class="s">{esc(_format_solved_by_kind(sbk))}</div></div>
    <div class="card"><div class="k">Latest Delta</div><div class="v">+{delta["added"]:,} / −{delta["removed"]:,}</div><div class="s">{delta["newly_solved"]:,} newly solved · {delta["kind_changes"]:,} kind changes</div></div>
  </section>

  <section aria-labelledby="downloads-heading">
    <h2 id="downloads-heading">Machine-Readable Files</h2>
    <p>
      <a href="snapshot.json"><code>snapshot.json</code></a> ·
      <a href="atlas_crosswalk.json"><code>atlas_crosswalk.json</code></a> ·
      <a href="CHANGES.jsonl"><code>CHANGES.jsonl</code></a> ·
      <a href="MANIFEST.sha256"><code>MANIFEST.sha256</code></a> ·
      Per-program JSONL shards linked in the table below (each &lt; 4 MB).
    </p>
  </section>

  <section aria-labelledby="programs-heading">
    <h2 id="programs-heading">All {len(snap["programs"])} Programs</h2>
    <div class="controls">
      <label for="prog-filter">Filter programs or fields:</label>
      <input id="prog-filter" type="search" placeholder="e.g. Erdős, Millennium, Number Theory…" autocomplete="off">
      <span id="prog-count" class="meta"></span>
    </div>
    <div class="table-wrap">
      <table id="prog-table">
        <thead>
          <tr>
            <th scope="col">Program</th>
            <th scope="col" class="num">Total</th>
            <th scope="col" class="num"><code>open</code></th>
            <th scope="col" class="num">Lean-stated</th>
            <th scope="col" class="num">Unformalized</th>
            <th scope="col">Solved (by kind)</th>
            <th scope="col" class="num">Mean diff.</th>
            <th scope="col">Top fields</th>
            <th scope="col">JSONL</th>
          </tr>
        </thead>
        <tbody>
          {"".join(prog_rows)}
        </tbody>
      </table>
    </div>
  </section>

  <section aria-labelledby="crosswalk-heading">
    <h2 id="crosswalk-heading">Candidate Mega-Atlas Crosswalk ({crosswalk.get("matched_atlas_problems", 0)} of {crosswalk.get("atlas_problems", 1900)} Atlas Problems)</h2>
    <p class="subtitle">
      Automatic exact normalised-title candidates only (not curated identifications).
      <code>{len(signals)}</code> candidate link(s) carry a Left to Solve <code>solved</code> flag; zero Mega-Atlas statuses are changed.
    </p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th scope="col">Atlas ID</th>
            <th scope="col">Mega-Atlas Name</th>
            <th scope="col">Left to Solve Candidate(s)</th>
          </tr>
        </thead>
        <tbody>
          {"".join(cw_rows) if cw_rows else '<tr><td colspan="3">No candidates recorded.</td></tr>'}
        </tbody>
      </table>
    </div>
  </section>

  <section aria-labelledby="changes-heading">
    <h2 id="changes-heading">Recent Sync Log (<code>CHANGES.jsonl</code>)</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th scope="col">Retrieved (UTC)</th>
            <th scope="col" class="num">Reported Total</th>
            <th scope="col" class="num">Added</th>
            <th scope="col" class="num">Removed</th>
            <th scope="col" class="num">Newly Solved</th>
            <th scope="col" class="num">Kind Changes</th>
          </tr>
        </thead>
        <tbody>
          {"".join(ch_rows) if ch_rows else '<tr><td colspan="6">No logged changes yet.</td></tr>'}
        </tbody>
      </table>
    </div>
  </section>
</main>

<footer>
  <p>
    <strong>Provenance &amp; Licensing:</strong> Fetched sequentially from public endpoints <code>/api/problems</code> and <code>/api/stats</code> on
    <a href="{esc(BASE)}" rel="noopener noreferrer">lefttosolve.com</a> (permitted by <code>robots.txt</code>; disallowed paths <code>/api/desk/</code> and <code>/api/verdict</code> are never requested).
    Upstream sources cited by Left to Solve include <code>google-deepmind/formal-conjectures</code> (Apache-2.0), <code>teorth/erdosproblems</code>, Wikipedia (CC BY-SA 4.0), Open Problem Garden, MathOverflow (CC BY-SA 4.0), Mathematics Stack Exchange (CC BY-SA 4.0) and OEIS (CC BY-SA 4.0).
    Not affiliated with Left to Solve or any upstream source. Entries removed on request.
  </p>
</footer>
<script>
(function () {{
  var input = document.getElementById("prog-filter");
  var tbody = document.querySelector("#prog-table tbody");
  var counter = document.getElementById("prog-count");
  if (!input || !tbody) return;
  var rows = Array.prototype.slice.call(tbody.querySelectorAll("tr"));
  function update() {{
    var q = input.value.trim().toLowerCase();
    var shown = 0;
    rows.forEach(function (tr) {{
      var match = !q || tr.textContent.toLowerCase().indexOf(q) !== -1;
      tr.style.display = match ? "" : "none";
      if (match) shown += 1;
    }});
    if (counter) counter.textContent = "Showing " + shown + " of " + rows.length + " programs";
  }}
  input.addEventListener("input", update);
  update();
}})();
</script>
</body>
</html>
"""


def _write_derived_views(
    programs: dict[str, list[dict[str, Any]]],
    files: dict[str, list[str]],
    meta: dict[str, Any],
    delta: dict[str, Any],
    retrieved_utc: str,
) -> dict[str, Any]:
    crosswalk = build_crosswalk(programs)
    program_rows = summarise(programs, files)
    solved_by_kind = aggregate_solved_by_kind(program_rows)
    snap = {
        "schema_version": SCHEMA_VERSION,
        "source": BASE + "/programs",
        "api": API_PROBLEMS,
        "retrieved_utc": retrieved_utc,
        "kept_fields": list(KEEP_FIELDS) + ["url"],
        "policy": "Metadata mirror only; no statement excerpts; never mutates the frozen Mega-Atlas dataset.",
        "crosswalk_matches": crosswalk.get("matched_atlas_problems", 0),
        "solved_by_kind": solved_by_kind,
        **meta,
        "programs": program_rows,
    }
    SNAPSHOT.write_text(json.dumps(snap, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    CROSSWALK.write_text(json.dumps(crosswalk, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    REPORT.write_text(render_report(snap, delta, crosswalk), encoding="utf-8", newline="\n")
    HTML_INDEX.write_text(render_html(snap, delta, crosswalk, _load_recent_changes()), encoding="utf-8", newline="\n")
    write_manifest()
    return snap


def run_live() -> dict[str, Any]:
    old = load_committed()
    programs, meta = crawl()
    delta = compute_delta(old, programs)
    files = write_program_files(programs)
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    delta_doc = {"retrieved_utc": now, "reported_total": meta["reported_total"], **delta}
    DELTA.parent.mkdir(parents=True, exist_ok=True)
    DELTA.write_text(json.dumps(delta_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    if not delta["baseline_present"] or any(delta[k] for k in ("added", "removed", "newly_solved", "kind_changes", "program_moves")):
        entry = {k: delta_doc[k] for k in ("retrieved_utc", "reported_total", "added", "removed", "newly_solved", "kind_changes", "program_moves")}
        entry["newly_solved_ids"] = delta["newly_solved_ids"][:50]
        with CHANGES.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
    return _write_derived_views(programs, files, meta, delta, now)


def run_rebuild() -> dict[str, Any]:
    """Regenerate snapshot summaries, crosswalk, report, HTML dashboard and manifest from committed shards."""
    programs, files, old_snap = load_committed_by_program()
    meta = {
        "reported_total": int(old_snap["reported_total"]),
        "fetched_total": sum(len(items) for items in programs.values()),
        "upstream": old_snap.get("upstream"),
        "catalog": old_snap.get("catalog"),
        "reported_program_totals": old_snap.get("reported_program_totals"),
    }
    if DELTA.exists():
        delta = json.loads(DELTA.read_text(encoding="utf-8"))
    else:
        delta = {
            "baseline_present": True,
            "added": 0,
            "removed": 0,
            "newly_solved": 0,
            "kind_changes": 0,
            "program_moves": 0,
        }
    return _write_derived_views(programs, files, meta, delta, str(old_snap["retrieved_utc"]))


def verify_offline() -> dict[str, Any]:
    if not SNAPSHOT.exists():
        raise SyncError("no committed mirror; run with --live first")
    for required in (SNAPSHOT, CROSSWALK, CHANGES, HTML_INDEX, MANIFEST):
        if not required.exists():
            raise SyncError(f"missing required mirror file: {required.relative_to(OUT_DIR).as_posix()}")
    snap = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    expected: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel = line.split("  ", 1)
        expected[rel] = digest

    actual_files = {
        p.relative_to(OUT_DIR).as_posix()
        for p in OUT_DIR.rglob("*")
        if p.is_file() and p.name != "MANIFEST.sha256"
    }
    unmanifested = sorted(actual_files - set(expected))
    if unmanifested:
        raise SyncError(f"unmanifested files under mirror directory: {unmanifested}")
    missing = sorted(set(expected) - actual_files)
    if missing:
        raise SyncError(f"files listed in MANIFEST.sha256 are missing: {missing}")
    for rel, digest in expected.items():
        actual = hashlib.sha256((OUT_DIR / rel).read_bytes()).hexdigest()
        if actual != digest:
            raise SyncError(f"checksum mismatch for {rel}")

    html_text = HTML_INDEX.read_text(encoding="utf-8")
    if "Content-Security-Policy" not in html_text or "<main id=\"main-content\">" not in html_text:
        raise SyncError("index.html missing strict CSP header or main landmark")

    crosswalk = json.loads(CROSSWALK.read_text(encoding="utf-8"))
    if crosswalk.get("status") != "ok":
        raise SyncError(f"atlas_crosswalk.json status is {crosswalk.get('status')!r}, expected 'ok'")
    if int(crosswalk.get("matched_atlas_problems", -1)) != int(snap.get("crosswalk_matches", -2)):
        raise SyncError("snapshot.json crosswalk_matches disagrees with atlas_crosswalk.json")

    seen_ids: set[str] = set()
    total = 0
    total_solved_by_kind = {k: 0 for k in KINDS}
    for prog in snap["programs"]:
        count = 0
        prog_ids: list[str] = []
        by_kind = {k: 0 for k in KINDS}
        solved_by_kind = {k: 0 for k in KINDS}
        for rel in prog["files"]:
            path = OUT_DIR / rel
            if rel not in expected:
                raise SyncError(f"{rel} not covered by MANIFEST.sha256")
            if path.stat().st_size >= 5 * 1024 * 1024:
                raise SyncError(f"{rel} exceeds the 5 MB tracked-file limit")
            for line in path.read_text(encoding="utf-8").splitlines():
                item = json.loads(line)
                if set(item) != set(KEEP_FIELDS) | {"url"}:
                    raise SyncError(f"{rel}: unexpected fields {sorted(item)}")
                pid = str(item["id"])
                if pid in seen_ids:
                    raise SyncError(f"duplicate problem id across mirror: {pid}")
                seen_ids.add(pid)
                prog_ids.append(pid)
                if item["url"] != problem_url(pid):
                    raise SyncError(f"{rel}: malformed url for {pid}: {item['url']!r}")
                kind = str(item["kind"])
                by_kind[kind] = by_kind.get(kind, 0) + 1
                if item["solved"]:
                    solved_by_kind[kind] = solved_by_kind.get(kind, 0) + 1
                    total_solved_by_kind[kind] = total_solved_by_kind.get(kind, 0) + 1
                count += 1
        if prog_ids != sorted(prog_ids):
            raise SyncError(f"{prog['program']}: problem ids are not sorted")
        if count != prog["total"]:
            raise SyncError(f"{prog['program']}: snapshot says {prog['total']}, files hold {count}")
        if by_kind != prog["by_kind"]:
            raise SyncError(f"{prog['program']}: by_kind mismatch")
        if prog["formalized_in_lean"] != count - by_kind.get("unformalized", 0):
            raise SyncError(f"{prog['program']}: formalized_in_lean mismatch")
        if prog["solved"] != sum(solved_by_kind.values()):
            raise SyncError(f"{prog['program']}: solved count mismatch")
        if prog.get("solved_by_kind") != solved_by_kind:
            raise SyncError(f"{prog['program']}: solved_by_kind mismatch")
        total += count
    if total != snap["fetched_total"]:
        raise SyncError(f"fetched_total {snap['fetched_total']} != sum of program files {total}")
    if snap.get("solved_by_kind") != total_solved_by_kind:
        raise SyncError("top-level solved_by_kind mismatch")
    if snap["fetched_total"] < MIN_COMPLETENESS * snap["reported_total"]:
        raise SyncError("committed mirror is below the completeness threshold")
    return snap


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--live", action="store_true", help="crawl lefttosolve.com and rewrite the mirror")
    mode.add_argument("--rebuild", action="store_true", help="rebuild summaries, crosswalk, HTML and manifest from committed shards")
    mode.add_argument("--offline", action="store_true", help="verify the committed mirror without network access")
    args = parser.parse_args()
    try:
        if args.live:
            snap = run_live()
            label = "live"
        elif args.rebuild:
            snap = run_rebuild()
            label = "rebuild"
        else:
            snap = verify_offline()
            label = "offline"
    except SyncError as exc:
        print(f"FAIL: {exc} (committed mirror left unchanged)", file=sys.stderr)
        return 1
    print(
        f"PASS: Left to Solve mirror ({label}): {snap['fetched_total']:,} problems in "
        f"{len(snap['programs'])} programs, retrieved {snap['retrieved_utc']}, crosswalk candidates {snap.get('crosswalk_matches', 0)}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
