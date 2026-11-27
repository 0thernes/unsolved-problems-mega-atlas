#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Sovereign target radar & upstream statement-bridge scaffolder for 0thernes.

Reads the local daily Left to Solve mirror (`data/external/lefttosolve/`) strictly
offline and read-only (never calls `/api/desk/` or `/api/verdict`, never opens
external PRs or holds leases, and never mutates the frozen 2,000-problem
Mega-Atlas dataset).

Capabilities
  1. `rank`: Mines all Lean-stated unsolved targets (`open` and `known`, excluding
     unformalized scrapes) against 0thernes frontier domains and the
     Mega-Atlas crosswalk, emitting a deterministic Markdown/JSON target radar.
  2. `scaffold`: Generates a Palomar-ready, Build Standard v1.2.0 sovereign
     bridge & reduction starter pack (`Challenge.lean`, `FormalConjecturesBridge.lean`,
     `Reduction.lean`, `comparator.json`, `formalization.yaml`, `THIRD_PARTY_NOTICES.md`)
     for any Lean-stated target in the local mirror.

Usage
  python scripts/mine_sovereign_targets.py rank --kind open --domain all --limit 25
  python scripts/mine_sovereign_targets.py rank --kind known --domain quantum,combinatorics --limit 20
  python scripts/mine_sovereign_targets.py scaffold --id Arxiv.2104.00502.barker_conjecture --dest /tmp/demo
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
MIRROR_DIR = ROOT / "data" / "external" / "lefttosolve"
PROGRAMS_DIR = MIRROR_DIR / "programs"
SNAPSHOT_PATH = MIRROR_DIR / "snapshot.json"
CROSSWALK_PATH = MIRROR_DIR / "atlas_crosswalk.json"

AUTHOR_NAME = "Alexander Stephen Donahue"
AUTHOR_ORCID = "0009-0006-8168-9648"
AUTHOR_AFFILIATION = "Independent Researcher, Spokane, WA, USA"
UPSTREAM_FC_REPO = "https://github.com/google-deepmind/formal-conjectures"

DOMAIN_KEYWORDS: dict[str, tuple[str, ...]] = {
    "quantum": (
        "quantum", "pauli", "kochen", "specker", "context", "sicpovm", "sic-povm",
        "mutually unbiased", "mub", "entangled", "ame_", "bell", "clifford", "weyl",
        "stabilizer", "hilbert", "unitary", "hadamard",
    ),
    "combinatorics": (
        "shannon", "capacity", "lovasz", "ramsey", "clique", "chromatic", "independent",
        "cycle", "barker", "graph", "tree", "domination", "vertex cover", "hypergraph",
        "turan", "sidon", "sunflower", "hadwiger", "borsuk", "hadamard", "projective plane",
        "mols", "latin square", "combinatorics", "packing", "kissing",
    ),
    "algebra": (
        "cayley", "octonion", "sedenion", "tensor", "cprank", "rank", "group ring",
        "unit conjecture", "dixmier", "poisson", "zariski", "matrix", "eigenvalue",
        "polynomial", "schur", "clifford", "nonassociative", "associative rings",
        "linear algebra", "field theory", "kaplansky",
    ),
    "complexity": (
        "circuit", "catalytic", "entropy", "information", "code", "coding", "strassen",
        "busy beaver", "antihydra", "undecidable", "complexity", "computer science",
        "communication", "turing", "sat",
    ),
    "number_theory": (
        "markov", "apollonian", "sandpile", "collatz", "lonely runner", "prime",
        "brocard", "goldbach", "perfect number", "mersenne", "mahler", "lehmer",
        "zeroless", "digits", "fibonacci", "kurepa", "schanuel", "number theory",
    ),
    "probability": (
        "multinomial", "total variation", "variance", "probability", "martingale",
        "random", "percolation", "autocorrelation", "statistics",
    ),
}

ZERO_MATHLIB_HINTS: tuple[str, ...] = (
    "barker", "list", "digits", "zeroless", "collatz", "ramsey", "hadamard",
    "markov", "sandpile", "antihydra", "clique", "cycle", "sidon", "cayley",
    "brocard", "lonely", "goldbach", "perfect",
)


def load_snapshot(mirror_dir: Path = MIRROR_DIR) -> dict[str, Any]:
    snap_path = mirror_dir / "snapshot.json"
    if not snap_path.is_file():
        raise FileNotFoundError(f"Left to Solve mirror snapshot not found: {snap_path}")
    return json.loads(snap_path.read_text(encoding="utf-8"))


def load_crosswalk_index(mirror_dir: Path = MIRROR_DIR) -> dict[str, list[str]]:
    cw_path = mirror_dir / "atlas_crosswalk.json"
    if not cw_path.is_file():
        return {}
    cw = json.loads(cw_path.read_text(encoding="utf-8"))
    by_lts_id: dict[str, list[str]] = {}
    for row in cw.get("matches", []):
        atlas_id = str(row.get("atlas_id", ""))
        for cand in row.get("lefttosolve", []):
            lid = str(cand.get("id", ""))
            if lid and atlas_id:
                by_lts_id.setdefault(lid, []).append(atlas_id)
    return by_lts_id


def load_lean_stated_targets(mirror_dir: Path = MIRROR_DIR) -> list[dict[str, Any]]:
    """Load all Lean-stated (`open`, `known`, `warmup`) records from the offline mirror."""
    prog_dir = mirror_dir / "programs"
    if not prog_dir.is_dir():
        raise FileNotFoundError(f"Programs directory not found: {prog_dir}")
    snap = load_snapshot(mirror_dir)
    file_to_program: dict[str, str] = {}
    for p in snap.get("programs", []):
        pname = str(p.get("program", ""))
        for rel in p.get("files", []):
            file_to_program[Path(rel).name] = pname

    records: list[dict[str, Any]] = []
    for entry in sorted(prog_dir.iterdir(), key=lambda x: x.name):
        if entry.suffix != ".jsonl":
            continue
        prog_name = file_to_program.get(entry.name, entry.stem)
        with entry.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                if rec.get("kind") == "unformalized":
                    continue
                rec["program"] = prog_name
                records.append(rec)
    return records


def classify_domains(rec: dict[str, Any]) -> list[str]:
    blob = " ".join(
        [
            str(rec.get("id", "")),
            str(rec.get("title", "")),
            str(rec.get("program", "")),
            " ".join(str(x) for x in (rec.get("fields") or [])),
        ]
    ).lower()
    matched: list[str] = []
    for dom, kws in DOMAIN_KEYWORDS.items():
        if any(kw in blob for kw in kws):
            matched.append(dom)
    return matched


def score_target(
    rec: dict[str, Any],
    domains: list[str],
    atlas_ids: list[str],
) -> tuple[float, bool]:
    """Deterministic sovereign priority score (higher = stronger fit)."""
    score = 0.0
    if rec.get("kind") == "open":
        score += 25.0
    elif rec.get("kind") == "known":
        score += 15.0

    # Domain affinity with active 0thernes frontier lines
    score += min(len(domains), 3) * 14.0
    if "quantum" in domains:
        score += 8.0
    if "combinatorics" in domains or "algebra" in domains:
        score += 6.0

    # Mega-Atlas crosswalk bonus
    if atlas_ids:
        score += 18.0

    # Tractability heuristic (prefer concrete / mid-difficulty over 90+ mammoth goals)
    diff = rec.get("difficulty")
    if isinstance(diff, (int, float)):
        score += max(0.0, (75.0 - float(diff)) * 0.65)

    # Prize signal (informational only; never a promise)
    prize = rec.get("prize")
    if prize:
        score += 5.0

    blob = f"{rec.get('id', '')} {rec.get('title', '')}".lower()
    zero_mathlib_friendly = any(h in blob for h in ZERO_MATHLIB_HINTS)
    if zero_mathlib_friendly:
        score += 10.0

    return round(score, 2), zero_mathlib_friendly


def get_upstream_commit(snap: dict[str, Any]) -> str:
    upstream = snap.get("upstream")
    if isinstance(upstream, dict) and upstream.get("commit"):
        return str(upstream["commit"])
    if snap.get("upstream_commit"):
        return str(snap["upstream_commit"])
    raise ValueError("Left to Solve snapshot.json is missing upstream.commit (refusing to fabricate a commit SHA)")


def mine_targets(
    mirror_dir: Path = MIRROR_DIR,
    *,
    kind: str = "open",
    domains_filter: list[str] | None = None,
    include_solved: bool = False,
    limit: int = 25,
) -> dict[str, Any]:
    snap = load_snapshot(mirror_dir)
    cw_index = load_crosswalk_index(mirror_dir)
    all_lean = load_lean_stated_targets(mirror_dir)

    allowed_kinds = {"open", "known", "warmup"} if kind == "any" else {kind}
    dom_set = set(domains_filter) if domains_filter else set()

    ranked: list[dict[str, Any]] = []
    for rec in all_lean:
        if rec.get("kind") not in allowed_kinds:
            continue
        if not include_solved and rec.get("solved"):
            continue
        doms = classify_domains(rec)
        if dom_set and not (dom_set & set(doms)):
            continue
        atlas_ids = cw_index.get(str(rec.get("id", "")), [])
        score, zm_hint = score_target(rec, doms, atlas_ids)
        ranked.append(
            {
                "score": score,
                "id": rec["id"],
                "kind": rec["kind"],
                "difficulty": rec.get("difficulty"),
                "program": rec["program"],
                "title": rec.get("title", ""),
                "fields": rec.get("fields") or [],
                "domains": doms,
                "atlas_ids": atlas_ids,
                "zero_mathlib_hint": zm_hint,
                "prize": rec.get("prize"),
                "url": rec.get("url", ""),
            }
        )

    ranked.sort(key=lambda r: (-r["score"], 999 if r["difficulty"] is None else r["difficulty"], r["id"]))
    return {
        "schema_version": "1.0.0",
        "generated_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_snapshot_utc": snap.get("retrieved_utc"),
        "upstream_formal_conjectures_commit": get_upstream_commit(snap),
        "filter": {
            "kind": kind,
            "domains": sorted(dom_set) if dom_set else ["all"],
            "include_solved": include_solved,
        },
        "total_lean_stated_in_mirror": len(all_lean),
        "total_matching": len(ranked),
        "targets": ranked[:limit],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "<!-- SPDX-License-Identifier: CC-BY-4.0 -->",
        "# 0thernes Sovereign Target Radar (Read-Only Formal-Conjectures Feed)",
        "",
        f"- **Author:** {AUTHOR_NAME} ({AUTHOR_AFFILIATION}, ORCID `{AUTHOR_ORCID}`)",
        f"- **Mirror snapshot (UTC):** `{report.get('source_snapshot_utc')}`",
        f"- **Pinned `google-deepmind/formal-conjectures` commit:** `{report.get('upstream_formal_conjectures_commit')}`",
        f"- **Filter:** `kind={report['filter']['kind']}`, `domains={','.join(report['filter']['domains'])}`",
        f"- **Matching unsolved Lean-stated targets:** {report['total_matching']} (of {report['total_lean_stated_in_mirror']} Lean-stated entries in mirror)",
        "",
        "| Rank | Score | Diff | Kind | Target ID | Domains | Mega-Atlas | Zero-Mathlib Hint | Program |",
        "|---:|---:|---:|---|---|---|---|---|---|",
    ]
    for idx, t in enumerate(report["targets"], start=1):
        doms = ", ".join(t["domains"]) if t["domains"] else "-"
        atlas = ", ".join(t["atlas_ids"]) if t["atlas_ids"] else "-"
        zm = "yes" if t["zero_mathlib_hint"] else "no"
        diff = "-" if t["difficulty"] is None else str(t["difficulty"])
        lines.append(
            f"| {idx} | {t['score']:.1f} | {diff} | `{t['kind']}` | `{t['id']}` | {doms} | {atlas} | {zm} | {t['program']} |"
        )
    lines.append("")
    return "\n".join(lines)


def _lean_ident(raw: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]", "_", raw)
    if not cleaned or cleaned[0].isdigit():
        cleaned = "T_" + cleaned
    return cleaned


def scaffold_sovereign_bridge(
    target_id: str,
    dest: Path,
    mirror_dir: Path = MIRROR_DIR,
    *,
    project_name: str | None = None,
) -> dict[str, Any]:
    """Generate a sovereign Palomar + upstream-bridge + reduction starter pack."""
    snap = load_snapshot(mirror_dir)
    upstream_commit = get_upstream_commit(snap)
    all_lean = load_lean_stated_targets(mirror_dir)
    match = next((r for r in all_lean if r.get("id") == target_id), None)
    if match is None:
        raise ValueError(f"Target ID not found among Lean-stated mirror entries: {target_id}")

    proj = _lean_ident(project_name) if project_name else _lean_ident(target_id.split(".")[0]) + "Frontier"
    lean_dir = dest / "lean"
    lean_dir.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    q_commit = json.dumps(upstream_commit)
    q_target_id = json.dumps(target_id)
    q_title = json.dumps(f"{match.get('title') or target_id} — Sovereign Formalization", ensure_ascii=False)
    q_kind = json.dumps(str(match.get("kind") or "unknown"))

    # 1. Challenge.lean (Palomar isolated statement stub)
    challenge_lean = (
        "-- SPDX-License-Identifier: Apache-2.0\n"
        f"-- Copyright (c) {dt.date.today().year} {AUTHOR_NAME}\n"
        "module\n\n"
        f"/-!\n# Sovereign Palomar Challenge — `{target_id}`\n\n"
        f"Upstream reference: `{UPSTREAM_FC_REPO}` @ `{upstream_commit}`\n"
        f"Upstream declaration: `{target_id}` (`{match.get('kind')}`)\n"
        "-/\n\n"
        f"namespace {proj}.Challenge\n\n"
        "-- Replace `TargetStatement` with the exact zero-Mathlib or Mathlib specification\n"
        "-- matching the upstream formal-conjectures declaration line-for-line.\n"
        "public def TargetStatement : Prop := True\n\n"
        "public theorem target_main : TargetStatement := by\n"
        "  sorry\n\n"
        f"end {proj}.Challenge\n"
    )

    # 2. FormalConjecturesBridge.lean (exact upstream type_of% pinning protocol)
    bridge_lean = (
        "-- SPDX-License-Identifier: Apache-2.0\n"
        f"-- Copyright (c) {dt.date.today().year} {AUTHOR_NAME}\n"
        "module\n\n"
        f"/-!\n# Sovereign Upstream Statement Bridge — `{target_id}`\n\n"
        f"Pins the sovereign statement directly against `{UPSTREAM_FC_REPO}`\n"
        f"at commit `{upstream_commit}` (`Apache-2.0`).\n\n"
        "Protocol:\n"
        "  1. When building with pinned `formal-conjectures`, import the upstream module and prove:\n"
        f"       `theorem sovereign_matches_upstream : type_of% @{target_id} := ...`\n"
        "  2. Audit `#print axioms` strictly within `[propext, Classical.choice, Quot.sound]`.\n"
        "  3. Never call the upstream `sorry`-backed theorem in the proof term.\n"
        "-/\n\n"
        f"namespace {proj}.UpstreamBridge\n\n"
        f"public def upstreamCommit : String := {q_commit}\n"
        f"public def upstreamDecl : String := {q_target_id}\n\n"
        f"end {proj}.UpstreamBridge\n"
    )

    # 3. Reduction.lean (kernel-checked H1 -> H2 -> Target decomposition skeleton)
    reduction_lean = (
        "-- SPDX-License-Identifier: Apache-2.0\n"
        f"-- Copyright (c) {dt.date.today().year} {AUTHOR_NAME}\n"
        "module\n\n"
        f"/-!\n# Kernel-Checked Reduction Decomposition — `{target_id}`\n\n"
        "Decomposes an open target into non-vacuous sub-hypotheses `H1`, `H2`, ...\n"
        "with a kernel-checked implication `H1 -> H2 -> Target`, paired with\n"
        "`NonVacuity` witnesses and `AdversarialTests`.\n"
        "-/\n\n"
        f"namespace {proj}.Reduction\n\n"
        "public def H1 : Prop := True\n"
        "public def H2 : Prop := True\n\n"
        "public theorem reduction_glue (Target : Prop) (hImpl : H1 → H2 → Target) (h1 : H1) (h2 : H2) : Target :=\n"
        "  hImpl h1 h2\n\n"
        f"end {proj}.Reduction\n"
    )

    # 4. comparator.json
    comparator_json = {
        "challenge_module": "Challenge",
        "solution_module": "Solution",
        "theorem_names": [f"{proj}.Challenge.target_main"],
        "definition_names": [],
        "permitted_axioms": ["propext", "Quot.sound", "Classical.choice"],
    }

    # 5. formalization.yaml (Palomar metadata, Playbook v1.3 compliant)
    formalization_yaml = (
        f"title: {q_title}\n"
        "authors:\n"
        f"  - name: {json.dumps(AUTHOR_NAME)}\n"
        f"    orcid: {json.dumps(AUTHOR_ORCID)}\n"
        f"    affiliation: {json.dumps(AUTHOR_AFFILIATION)}\n"
        "license: \"Apache-2.0\"\n"
        "challenge_file: \"lean/Challenge.lean\"\n"
        "solution_file: \"lean/Solution.lean\"\n"
        "comparator_config: \"lean/comparator.json\"\n"
        "upstream_reference:\n"
        f"  repository: {json.dumps(UPSTREAM_FC_REPO)}\n"
        f"  commit: {q_commit}\n"
        f"  declaration: {q_target_id}\n"
        f"  kind: {q_kind}\n"
        f"date: {json.dumps(today)}\n"
        "review_status: \"Preprint; not peer reviewed\"\n"
        "limitations: \"Draft starter scaffold; replace stubs with verified proofs before release.\"\n"
    )

    # 6. THIRD_PARTY_NOTICES.md
    notices_md = (
        "<!-- SPDX-License-Identifier: CC-BY-4.0 -->\n"
        "# Third-Party Notices\n\n"
        f"- **Upstream statement source:** `google-deepmind/formal-conjectures` ({UPSTREAM_FC_REPO}),\n"
        f"  commit `{upstream_commit}`, declaration `{target_id}`, licensed under `Apache-2.0`.\n"
        f"- **Discovery metadata:** Read-only offline mirror from `unsolved-problems-mega-atlas`\n"
        f"  (`data/external/lefttosolve/`, retrieved `{snap.get('retrieved_utc')}`).\n"
    )

    files_written = {
        lean_dir / "Challenge.lean": challenge_lean,
        lean_dir / "FormalConjecturesBridge.lean": bridge_lean,
        lean_dir / "Reduction.lean": reduction_lean,
        lean_dir / "comparator.json": json.dumps(comparator_json, indent=2) + "\n",
        dest / "formalization.yaml": formalization_yaml,
        dest / "THIRD_PARTY_NOTICES.md": notices_md,
    }
    for path, content in files_written.items():
        path.write_text(content, encoding="utf-8", newline="\n")

    return {
        "target_id": target_id,
        "kind": match.get("kind"),
        "project_name": proj,
        "upstream_commit": upstream_commit,
        "dest": str(dest),
        "files": sorted(str(p.relative_to(dest).as_posix()) for p in files_written),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="0thernes sovereign target radar & bridge scaffolder")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_rank = sub.add_parser("rank", help="Rank unsolved Lean-stated targets from the offline mirror")
    p_rank.add_argument("--kind", choices=("open", "known", "warmup", "any"), default="open")
    p_rank.add_argument("--domain", default="all", help="Comma-separated domains or 'all'")
    p_rank.add_argument("--include-solved", action="store_true")
    p_rank.add_argument("--limit", type=int, default=25)
    p_rank.add_argument("--out-json", type=Path, default=None)
    p_rank.add_argument("--out-md", type=Path, default=None)

    p_scaf = sub.add_parser("scaffold", help="Generate a sovereign Palomar + bridge + reduction starter pack")
    p_scaf.add_argument("--id", required=True, dest="target_id", help="Exact Left-to-Solve / formal-conjectures ID")
    p_scaf.add_argument("--dest", type=Path, required=True, help="Output directory for the starter pack")
    p_scaf.add_argument("--project", default=None, help="Optional Lean project namespace")

    args = parser.parse_args(argv)
    if args.cmd == "rank":
        doms = None if args.domain == "all" else [d.strip() for d in args.domain.split(",") if d.strip()]
        report = mine_targets(kind=args.kind, domains_filter=doms, include_solved=args.include_solved, limit=args.limit)
        md = render_markdown(report)
        if args.out_json:
            args.out_json.parent.mkdir(parents=True, exist_ok=True)
            args.out_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
        if args.out_md:
            args.out_md.parent.mkdir(parents=True, exist_ok=True)
            args.out_md.write_text(md, encoding="utf-8", newline="\n")
        if not args.out_json and not args.out_md:
            sys.stdout.write(md)
        return 0

    if args.cmd == "scaffold":
        res = scaffold_sovereign_bridge(args.target_id, args.dest, project_name=args.project)
        sys.stdout.write(json.dumps(res, indent=2) + "\n")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
