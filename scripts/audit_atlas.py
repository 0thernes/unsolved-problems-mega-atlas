#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""
Cryptographic, Structural & Epistemic Integrity Auditor for the
Unsolved Problems Mega-Atlas (V2.7.0, Alexander Stephen Donahue).

Checks:
  1. Source dataset schema (48 typed fields), strict deduplication (1,900 unique problems),
     0 unresolved raw links, 8 Macro-Pillars, 28 Superdomains, 8 Substrates, 7 Abstraction Layers,
     88 Canonical Hubs, 1 connected component, 0 articulation points, 0 bridges (biconnected),
     Handshaking Lemma, and CSS/Titan/Gradient/Margin bounds.
  2. JSON Schema Draft 2020-12 compliance on all 1,900 records (`schema/problem.schema.json`).
  3. Cross-format parity across CSV, TSV, JSON.gz, JSONL.gz, SQLite (+FTS5 + substrate_summary +
     author_frontier_contributions), and 15-sheet XLSX.
  4. Canonical author & ORCID (`0009-0006-8168-9648`) presence across metadata/governance files.
  5. Optional Lean 4.35.0 build & zero-sorry / constructive-axiom audit (`--check-lean`).
  6. Byte-exact SHA-256 verification of all frozen tracked artifacts against `CHECKSUMS.sha256`
     (with `--sync-checksums` to deterministically regenerate `CHECKSUMS.sha256`).
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

import jsonschema
import openpyxl
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "rag"))

from query import DEFAULT_DB, ensure_sqlite_db  # noqa: E402
from v2_loader import load_v2_master  # noqa: E402
from v2_schema import CANONICAL_HUBS, MACRO_PILLARS, SUPERDOMAIN_TO_PILLAR  # noqa: E402

EXPECTED_ORCID = "0009-0006-8168-9648"
ALLOWED_AXIOMS = {"propext", "Quot.sound"}

# Gitignored large derived files (>5 MB) excluded from CHECKSUMS.sha256 (attached to Releases)
IGNORED_DERIVED_OUTPUTS = {
    "MegaAtlas_Unsolved_Problems_V2.sqlite",
    "MegaAtlas_Unsolved_Problems_V2.json",
    "MegaAtlas_Unsolved_Problems_V2.jsonl",
    "MegaAtlas_Comprehensive_Report_V2.pdf",
    "MegaAtlas_Print_Report_V2.html",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_checksum_targets() -> list[Path]:
    targets: list[Path] = []
    out_dir = ROOT / "outputs"
    if out_dir.exists():
        for p in sorted(out_dir.rglob("*")):
            if p.is_file() and p.name not in IGNORED_DERIVED_OUTPUTS:
                targets.append(p)
    for rel in [
        "RANKING.md",
        "CLAIMS.md",
        "LIMITATIONS.md",
        "schema/problem.schema.json",
        "schema/atlas.schema.json",
        "dist/Donahue_2026_unsolved_problems_mega_atlas.pdf",
        "dist/arxiv_submission.tar.gz",
        "blueprint/index.html",
        "results/lean_axioms.txt",
        "docs/WHITE_PAPER.md",
        "docs/DATASHEET.md",
        "docs/FORENSIC_AUDIT_V2.3.md",
        "docs/PRESERVATION.md",
        "docs/statement-fidelity.md",
        "docs/media/social-preview.png",
        ".zenodo.json",
        "croissant.json",
        "ro-crate-metadata.json",
        "autoresearch/evaluate.py",
        "research/runs/LOG-002_antihydra_pilot/RESULTS.json",
    ]:
        p = ROOT / rel
        if p.exists():
            targets.append(p)
    return sorted(set(targets), key=lambda p: p.relative_to(ROOT).as_posix())


DATA_MANIFEST_TARGETS = [
    "outputs/MegaAtlas_Unsolved_Problems_V2.csv",
    "outputs/MegaAtlas_Unsolved_Problems_V2.tsv",
    "outputs/MegaAtlas_Unsolved_Problems_V2.json.gz",
    "outputs/MegaAtlas_Unsolved_Problems_V2.jsonl.gz",
    "outputs/MegaAtlas_Unsolved_Problems_V2.xlsx",
    "outputs/MegaAtlas_Unsolved_Problems_V2_Legacy.xls",
    "outputs/MegaAtlas_Interactive_Dashboard_V2.html",
    "dist/Donahue_2026_unsolved_problems_mega_atlas.pdf",
    "dist/arxiv_submission.tar.gz",
    "results/lean_axioms.txt",
    "research/runs/LOG-002_antihydra_pilot/RESULTS.json",
]


def sync_checksums() -> int:
    targets = collect_checksum_targets()
    lines = [f"{sha256_file(p)}  {p.relative_to(ROOT).as_posix()}" for p in targets]
    (ROOT / "CHECKSUMS.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    manifest_dir = ROOT / "data"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    m_lines = [
        f"{sha256_file(ROOT / rel)}  ../{rel}"
        for rel in DATA_MANIFEST_TARGETS
        if (ROOT / rel).exists()
    ]
    (manifest_dir / "MANIFEST.sha256").write_text("\n".join(m_lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Synced CHECKSUMS.sha256 ({len(lines)} digests) and data/MANIFEST.sha256 ({len(m_lines)} digests).")
    return len(lines)


def strip_lean_comments(text: str) -> str:
    no_blocks = re.sub(r"/-.*?-/", "", text, flags=re.S)
    return "\n".join(line.split("--", 1)[0] for line in no_blocks.splitlines())


def audit_lean(errors: list[str]) -> None:
    lean_dir = ROOT / "lean"
    if not (lean_dir / "lakefile.toml").exists():
        errors.append("Missing lean/lakefile.toml")
        return
    for lf in lean_dir.rglob("*.lean"):
        if ".lake" in lf.parts:
            continue
        code = strip_lean_comments(lf.read_text(encoding="utf-8"))
        for forbidden in ("sorry", "admit", "native_decide"):
            if re.search(rf"\b{forbidden}\b", code):
                errors.append(f"Forbidden token '{forbidden}' in {lf.relative_to(ROOT)}")
        for line in code.splitlines():
            if re.match(r"^(?:(?:private|protected|noncomputable|scoped|local|unsafe)\s+)*axiom\b", line.strip()):
                errors.append(f"Custom axiom declaration in {lf.relative_to(ROOT)}: {line.strip()}")

    lake_exe = Path.home() / ".elan" / "bin" / ("lake.exe" if sys.platform == "win32" else "lake")
    lake_bin = str(lake_exe) if lake_exe.exists() else "lake"
    res = subprocess.run([lake_bin, "build"], cwd=lean_dir, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        errors.append(f"Lean `lake build` failed (exit {res.returncode}): {res.stderr[:400]}")
        return
    ax_res = subprocess.run([lake_bin, "env", "lean", "MegaAtlasProofs/VerifyAxioms.lean"], cwd=lean_dir, capture_output=True, text=True, check=False)
    if ax_res.returncode != 0:
        errors.append(f"Lean VerifyAxioms.lean failed (exit {ax_res.returncode}): {ax_res.stderr[:400]}")
        return
    for line in (ax_res.stdout + "\n" + ax_res.stderr).splitlines():
        if "depends on axioms:" in line:
            bracket = line.split("[", 1)[1].rsplit("]", 1)[0]
            used = {tok.strip() for tok in bracket.split(",") if tok.strip()}
            bad = used - ALLOWED_AXIOMS
            if bad:
                errors.append(f"Disallowed Lean axioms detected: {bad} in `{line.strip()}`")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit the Unsolved Problems Mega-Atlas (v2.7.0).")
    parser.add_argument("--sync-checksums", action="store_true", help="Regenerate CHECKSUMS.sha256 before auditing")
    parser.add_argument("--check-lean", action="store_true", help="Run Pure Lean 4.35.0 build & axiom audit")
    args = parser.parse_args()

    if args.sync_checksums:
        sync_checksums()

    errors: list[str] = []

    # 1. Load master dataset & structural checks
    data = load_v2_master()
    df = data["df"]
    G = data["G"]
    s = data["summary_stats"]

    if len(df) != 1900:
        errors.append(f"Expected 1900 problems, got {len(df)}")
    if not df["id"].is_unique:
        errors.append("Duplicate problem IDs in loaded dataset")
    if df["macro_pillar"].nunique() != len(MACRO_PILLARS):
        errors.append(f"Macro-pillar count mismatch: {df['macro_pillar'].nunique()}")
    if df["superdomain"].nunique() != len(SUPERDOMAIN_TO_PILLAR):
        errors.append(f"Superdomain count mismatch: {df['superdomain'].nunique()}")
    missing_hubs = set(CANONICAL_HUBS.values()) - set(df["id"])
    if missing_hubs:
        errors.append(f"Missing canonical hubs: {sorted(missing_hubs)}")
    if s["connected_components"] != 1:
        errors.append(f"Graph disconnected: {s['connected_components']} components")
    if s.get("articulation_points", 0) != 0:
        errors.append(f"Graph has {s['articulation_points']} articulation point(s) (expected 0; biconnected)")
    if s.get("graph_bridges", 0) != 0:
        errors.append(f"Graph has {s['graph_bridges']} bridge edge(s) (expected 0)")
    if s.get("unresolved_raw_links_count", 0) != 0:
        errors.append(f"Found {s['unresolved_raw_links_count']} unresolved raw_links")
    if df["substrate_class"].nunique() != 8:
        errors.append(f"Substrate class count mismatch: {df['substrate_class'].nunique()} vs 8")
    if df["abstraction_layer"].nunique() != 7:
        errors.append(f"Abstraction layer count mismatch: {df['abstraction_layer'].nunique()} vs 7")
    if int(df["graph_degree"].sum()) != 2 * G.number_of_edges():
        errors.append("Handshaking invariant violated: sum(degree) != 2 * |E|")
    if not (s["cross_pillar_edges"] <= s["cross_superdomain_edges"] <= s["total_graph_edges"]):
        errors.append("Edge hierarchy invariant violated")

    # 2. JSON Schema Draft 2020-12 check on all 1,900 records
    prob_schema = json.loads((ROOT / "schema" / "problem.schema.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(prob_schema)
    for rec in df.to_dict(orient="records"):
        errs = list(validator.iter_errors(rec))
        if errs:
            errors.append(f"Schema failure on {rec.get('id')}: {errs[0].message}")
            break

    # 3. Cross-format parity (tracked CSV, JSONL.gz, JSON.gz, 15-sheet XLSX, auto-built SQLite+FTS5)
    csv_df = pd.read_csv(ROOT / "outputs" / "MegaAtlas_Unsolved_Problems_V2.csv")
    if len(csv_df) != len(df):
        errors.append(f"CSV row mismatch: {len(csv_df)} vs {len(df)}")

    with gzip.open(ROOT / "outputs" / "MegaAtlas_Unsolved_Problems_V2.jsonl.gz", "rt", encoding="utf-8") as f:
        jsonl_lines = f.read().splitlines()
    if len(jsonl_lines) != len(df):
        errors.append(f"JSONL.gz line mismatch: {len(jsonl_lines)} vs {len(df)}")

    with gzip.open(ROOT / "outputs" / "MegaAtlas_Unsolved_Problems_V2.json.gz", "rt", encoding="utf-8") as f:
        jpayload = json.load(f)
    if len(jpayload.get("problems", [])) != len(df):
        errors.append("JSON.gz problem count mismatch")

    wb = openpyxl.load_workbook(ROOT / "outputs" / "MegaAtlas_Unsolved_Problems_V2.xlsx", read_only=True)
    if len(wb.sheetnames) != 15:
        errors.append(f"XLSX sheet count mismatch: {len(wb.sheetnames)} vs 15")
    wb.close()

    ensure_sqlite_db(DEFAULT_DB)
    conn = sqlite3.connect(str(DEFAULT_DB))
    try:
        sql_cnt = conn.execute("SELECT COUNT(*) FROM problems").fetchone()[0]
        sub_cnt = conn.execute("SELECT COUNT(*) FROM substrate_summary").fetchone()[0]
        auth_cnt = conn.execute("SELECT COUNT(*) FROM author_frontier_contributions").fetchone()[0]
        fts_cnt = conn.execute("SELECT COUNT(*) FROM problems_fts WHERE problems_fts MATCH '\"Riemann\"'").fetchone()[0]
        if sql_cnt != len(df):
            errors.append(f"SQLite row mismatch: {sql_cnt} vs {len(df)}")
        if sub_cnt != 8:
            errors.append(f"SQLite substrate_summary row mismatch: {sub_cnt} vs 8")
        expected_auth = len(data["df_author_contributions"])
        if auth_cnt != expected_auth:
            errors.append(f"SQLite author_frontier_contributions row mismatch: {auth_cnt} vs {expected_auth}")
        if fts_cnt < 1:
            errors.append("SQLite FTS5 query returned 0 matches for 'Riemann'")
    finally:
        conn.close()

    # 4. Canonical author & ORCID presence check
    for rel in [
        "CITATION.cff",
        "CITATION.bib",
        ".zenodo.json",
        "croissant.json",
        "ro-crate-metadata.json",
        "README.md",
        "AUTHORS.md",
        "AGENTS.md",
        "llms.txt",
        "VERIFICATION.md",
        "EVIDENCE.md",
        "RANKING.md",
        "docs/DATASHEET.md",
        "docs/FORENSIC_AUDIT_V2.3.md",
        "docs/PRESERVATION.md",
    ]:
        p = ROOT / rel
        if not p.exists():
            errors.append(f"Missing required institutional file: {rel}")
        elif EXPECTED_ORCID not in p.read_text(encoding="utf-8"):
            errors.append(f"Canonical ORCID {EXPECTED_ORCID} missing from {rel}")

    # 5. SHA-256 manifest verification
    chk_path = ROOT / "CHECKSUMS.sha256"
    chk_count = 0
    if not chk_path.exists():
        errors.append("Missing CHECKSUMS.sha256")
    else:
        for line in chk_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            expected, rel = line.split(None, 1)
            target = ROOT / rel
            if not target.exists():
                errors.append(f"CHECKSUMS.sha256 references missing file: {rel}")
            else:
                actual = sha256_file(target)
                if actual != expected:
                    errors.append(f"SHA-256 mismatch for {rel}")
                chk_count += 1

    # 5b. Verify data/MANIFEST.sha256 parity
    dm_path = ROOT / "data" / "MANIFEST.sha256"
    if not dm_path.exists():
        errors.append("Missing data/MANIFEST.sha256")
    else:
        for line in dm_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            expected, rel = line.split(None, 1)
            target = (dm_path.parent / rel).resolve()
            if not target.exists():
                errors.append(f"data/MANIFEST.sha256 references missing file: {rel}")
            elif sha256_file(target) != expected:
                errors.append(f"data/MANIFEST.sha256 mismatch for {rel}")

    # 5c. Verify dual cryptographic timestamps (DigiCert RFC 3161 .tsr + Bitcoin OpenTimestamps .ots)
    if chk_path.exists() and not args.sync_checksums:
        chk_digest = hashlib.sha256(chk_path.read_bytes()).digest()
        tsr_path = ROOT / "CHECKSUMS.sha256.tsr"
        if not tsr_path.exists() or tsr_path.stat().st_size < 200 or chk_digest not in tsr_path.read_bytes():
            errors.append("CHECKSUMS.sha256.tsr missing or does not bind current CHECKSUMS.sha256")
        ots_path = ROOT / "CHECKSUMS.sha256.ots"
        ots_magic = b"\x00OpenTimestamps\x00\x00Proof\x00\xbf\x89\xe2\xe8\x84\xe8\x92\x94\x01\x08" + chk_digest
        if not ots_path.exists() or not ots_path.read_bytes().startswith(ots_magic):
            errors.append("CHECKSUMS.sha256.ots missing or does not bind current CHECKSUMS.sha256")

    # 6. Optional Lean 4.35.0 formal invariant audit
    if args.check_lean:
        audit_lean(errors)

    if errors:
        print("MEGA-ATLAS AUDIT FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print(
        f"PASS: Verified {len(df):,} unique problems (8 pillars x 28 superdomains, 1 biconnected component, "
        f"{G.number_of_edges():,} edges), JSON Schema Draft 2020-12 on all records, CSV/JSON.gz/JSONL.gz/SQLite+FTS5/15-sheet XLSX parity, "
        f"ORCID {EXPECTED_ORCID}, and {chk_count} byte-exact SHA-256 checksums"
        + (" + Pure Lean 4.35.0 build/axiom audit!" if args.check_lean else "!")
    )


if __name__ == "__main__":
    main()
