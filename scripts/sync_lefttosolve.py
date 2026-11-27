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
    under the repository's 5 MB tracked-file limit), a summary ``snapshot.json``,
    a per-run delta (added, removed, newly solved, kind changes), an append-only
    ``CHANGES.jsonl``, a candidate crosswalk to Mega-Atlas problems by exact
    normalised title, a ``MANIFEST.sha256`` and ``docs/lefttosolve-programs.md``.

What it does not do
  * It never edits the frozen 1,900-problem Mega-Atlas dataset (``src/v2_data``,
    ``outputs/``) and never retires an Atlas problem. The mirror is a sidecar layer.
  * Crosswalk rows are automatic title matches, labelled as candidates, not
    curated identifications.

Usage
  python scripts/sync_lefttosolve.py --offline      # verify the committed mirror
  python scripts/sync_lefttosolve.py --live         # crawl and rewrite the mirror
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
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
MANIFEST = OUT_DIR / "MANIFEST.sha256"
DELTA = ROOT / "results" / "lefttosolve_delta.json"
REPORT = ROOT / "docs" / "lefttosolve-programs.md"

BASE = "https://lefttosolve.com"
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


def summarise(programs: dict[str, list[dict[str, Any]]], files: dict[str, list[str]]) -> list[dict[str, Any]]:
    rows = []
    for name, items in sorted(programs.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        by_kind = {k: 0 for k in KINDS}
        for it in items:
            by_kind[str(it["kind"])] = by_kind.get(str(it["kind"]), 0) + 1
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
            "solved": sum(1 for it in items if it["solved"]),
            "with_prize": sum(1 for it in items if it["prize"]),
            "mean_difficulty": round(sum(diffs) / len(diffs), 2) if diffs else None,
            "top_fields": [f for f, _ in sorted(fields.items(), key=lambda kv: (-kv[1], kv[0]))[:5]],
            "files": files[name],
        })
    return rows


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


def build_crosswalk(programs: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    sys.path.insert(0, str(ROOT / "src"))
    try:
        from v2_loader import load_v2_master  # noqa: PLC0415
        df = load_v2_master()["df"]
        atlas = [(str(r["id"]), str(r["name"])) for _, r in df[["id", "name"]].iterrows()]
    except Exception as exc:  # pragma: no cover - environment without pandas
        return {"status": "skipped", "reason": f"atlas loader unavailable: {exc}", "matches": []}
    index: dict[str, list[tuple[str, str, str]]] = {}
    for name, items in programs.items():
        for it in items:
            key = norm_title(it["title"] or "")
            if len(key) >= 6:
                index.setdefault(key, []).append((str(it["id"]), str(it["title"]), name))
    matches = []
    for aid, aname in atlas:
        key = norm_title(aname)
        hits = index.get(key, [])
        if hits and len(key) >= 6:
            matches.append({
                "atlas_id": aid, "atlas_name": aname, "match_type": "exact-normalised-title (candidate)",
                "lefttosolve": [{"id": h[0], "title": h[1], "program": h[2], "url": problem_url(h[0])} for h in sorted(hits)[:10]],
            })
    return {"status": "ok", "method": "exact match after NFKD, lowercase, parenthetical and stop-word removal",
            "atlas_problems": len(atlas), "matched_atlas_problems": len(matches), "matches": matches}


def write_manifest() -> None:
    lines = []
    for path in sorted(OUT_DIR.rglob("*")):
        if path.is_file() and path.name != "MANIFEST.sha256":
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            lines.append(f"{digest}  {path.relative_to(OUT_DIR).as_posix()}\n")
    MANIFEST.write_text("".join(lines), encoding="utf-8", newline="\n")


def render_report(snap: dict[str, Any], delta: dict[str, Any]) -> str:
    cat = snap.get("catalog") or {}
    out = [
        "<!-- SPDX-License-Identifier: CC-BY-4.0 -->",
        "# Left to Solve program lists (daily mirror)",
        "",
        "Generated by `scripts/sync_lefttosolve.py`; do not edit by hand. Source: <https://lefttosolve.com/programs>.",
        "Problem statements live on Left to Solve and in [google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures); this mirror keeps metadata and links only.",
        "",
        f"- **Retrieved (UTC):** `{snap['retrieved_utc']}`",
        f"- **Problems:** {snap['fetched_total']:,} fetched of {snap['reported_total']:,} reported, in {len(snap['programs'])} programs",
        f"- **Catalogue counts (`/api/stats`):** open {cat.get('open', '?'):,} · known {cat.get('known', '?'):,} · warmup {cat.get('warmup', '?'):,} · unformalized {cat.get('unformalized', '?'):,}"
        if cat else "- **Catalogue counts:** unavailable",
        f"- **Upstream formal-conjectures commit:** `{(snap.get('upstream') or {}).get('commit')}`",
        f"- **Change since previous snapshot:** +{delta['added']:,} added, −{delta['removed']:,} removed, {delta['newly_solved']:,} newly solved, {delta['kind_changes']:,} kind changes"
        + ("" if delta["baseline_present"] else " (first snapshot)"),
        f"- **Candidate Atlas crosswalk:** {snap.get('crosswalk_matches', 0)} Mega-Atlas problems share an exact normalised title with a Left to Solve problem (`data/external/lefttosolve/atlas_crosswalk.json`; automatic, not curated)",
        "",
        "| Program | Total | Lean-stated | Unformalized | Solved | Mean difficulty | Top fields |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for p in snap["programs"]:
        md = "—" if p["mean_difficulty"] is None else f"{p['mean_difficulty']}"
        out.append(
            f"| [{p['program']}]({p['url']}) | {p['total']:,} | {p['formalized_in_lean']:,} | {p['by_kind'].get('unformalized', 0):,} | "
            f"{p['solved']:,} | {md} | {', '.join(p['top_fields']) or '—'} |"
        )
    out += [
        "",
        "`Lean-stated` counts problems whose kind is `open`, `known` or `warmup` (stated in Lean upstream); `Solved` is Left to Solve's own flag. Neither is verified by this repository.",
        "",
        "## Reproduction",
        "",
        "```bash",
        "python scripts/sync_lefttosolve.py --live     # crawl (about 330 requests, roughly 15 minutes)",
        "python scripts/sync_lefttosolve.py --offline  # verify the committed mirror",
        "```",
        "",
    ]
    return "\n".join(out)


def run_live() -> dict[str, Any]:
    old = load_committed()
    programs, meta = crawl()
    delta = compute_delta(old, programs)
    files = write_program_files(programs)
    crosswalk = build_crosswalk(programs)
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    snap = {
        "schema_version": SCHEMA_VERSION,
        "source": BASE + "/programs",
        "api": API_PROBLEMS,
        "retrieved_utc": now,
        "kept_fields": list(KEEP_FIELDS) + ["url"],
        "policy": "Metadata mirror only; no statement excerpts; never mutates the frozen Mega-Atlas dataset.",
        "crosswalk_matches": crosswalk.get("matched_atlas_problems", 0),
        **meta,
        "programs": summarise(programs, files),
    }
    SNAPSHOT.write_text(json.dumps(snap, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    CROSSWALK.write_text(json.dumps(crosswalk, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    delta_doc = {"retrieved_utc": now, "reported_total": meta["reported_total"], **delta}
    DELTA.parent.mkdir(parents=True, exist_ok=True)
    DELTA.write_text(json.dumps(delta_doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    if not delta["baseline_present"] or any(delta[k] for k in ("added", "removed", "newly_solved", "kind_changes", "program_moves")):
        entry = {k: delta_doc[k] for k in ("retrieved_utc", "reported_total", "added", "removed", "newly_solved", "kind_changes", "program_moves")}
        entry["newly_solved_ids"] = delta["newly_solved_ids"][:50]
        with CHANGES.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
    REPORT.write_text(render_report(snap, delta), encoding="utf-8", newline="\n")
    write_manifest()
    return snap


def verify_offline() -> dict[str, Any]:
    if not SNAPSHOT.exists():
        raise SyncError("no committed mirror; run with --live first")
    snap = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    expected = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        digest, rel = line.split("  ", 1)
        expected[rel] = digest
    for rel, digest in expected.items():
        actual = hashlib.sha256((OUT_DIR / rel).read_bytes()).hexdigest()
        if actual != digest:
            raise SyncError(f"checksum mismatch for {rel}")
    total = 0
    for prog in snap["programs"]:
        count = 0
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
                count += 1
        if count != prog["total"]:
            raise SyncError(f"{prog['program']}: snapshot says {prog['total']}, files hold {count}")
        total += count
    if total != snap["fetched_total"]:
        raise SyncError(f"fetched_total {snap['fetched_total']} != sum of program files {total}")
    if snap["fetched_total"] < MIN_COMPLETENESS * snap["reported_total"]:
        raise SyncError("committed mirror is below the completeness threshold")
    return snap


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--live", action="store_true", help="crawl lefttosolve.com and rewrite the mirror")
    mode.add_argument("--offline", action="store_true", help="verify the committed mirror without network access")
    args = parser.parse_args()
    try:
        snap = run_live() if args.live else verify_offline()
    except SyncError as exc:
        print(f"FAIL: {exc} (committed mirror left unchanged)", file=sys.stderr)
        return 1
    print(
        f"PASS: Left to Solve mirror ({'live' if args.live else 'offline'}): {snap['fetched_total']:,} problems in "
        f"{len(snap['programs'])} programs, retrieved {snap['retrieved_utc']}, crosswalk candidates {snap.get('crosswalk_matches', 0)}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
