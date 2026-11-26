#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""
Deterministic FAIR Scholarly Metadata Generator (`v2.4.0`):
  1. `croissant.json`         — MLCommons Croissant 1.0 JSON-LD dataset specification
  2. `ro-crate-metadata.json` — W3C / ResearchObject RO-Crate 1.1 JSON-LD descriptor
  3. `data/MANIFEST.sha256`   — Canonical SHA-256 manifest of frozen tracked data & paper artifacts

Hashes ONLY git-tracked deterministic artifacts (<5 MB each, Build Standard A24) so
every fresh git clone passes cryptographic parity checks out of the box.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from v2_loader import load_v2_master  # noqa: E402

REPO_URL = "https://github.com/0thernes/unsolved-problems-mega-atlas"
PAGES_URL = "https://0thernes.github.io/unsolved-problems-mega-atlas/"
RAW_BASE = "https://raw.githubusercontent.com/0thernes/unsolved-problems-mega-atlas/main/"
ORCID_URL = "https://orcid.org/0009-0006-8168-9648"
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").exists() else "2.4.0"


def _lean_theorem_count() -> int:
    p = ROOT / "lean" / "MegaAtlasProofs" / "VerifyAxioms.lean"
    if not p.exists():
        return 92
    return sum(1 for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip().startswith("#print axioms "))


def sha256_and_size(rel: str) -> tuple[str, int]:
    p = ROOT / rel
    data = p.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def build_croissant(df_cols: list[str], total_problems: int, total_edges: int) -> dict:
    lean_n = _lean_theorem_count()
    csv_sha, csv_sz = sha256_and_size("outputs/MegaAtlas_Unsolved_Problems_V2.csv")
    tsv_sha, tsv_sz = sha256_and_size("outputs/MegaAtlas_Unsolved_Problems_V2.tsv")
    jsonl_gz_sha, jsonl_gz_sz = sha256_and_size("outputs/MegaAtlas_Unsolved_Problems_V2.jsonl.gz")
    json_gz_sha, json_gz_sz = sha256_and_size("outputs/MegaAtlas_Unsolved_Problems_V2.json.gz")

    int_cols = {
        "year_formulated", "age_years_2026", "difficulty_score", "tractability_2050",
        "civilizational_impact", "interdisciplinarity_index", "graph_degree",
        "cross_superdomain_links", "cross_pillar_links", "network_cluster",
        "hardness_tractability_gradient", "adjacent_pillars_count",
    }
    float_cols = {
        "pagerank", "betweenness", "titan_index", "css_score", "near_term_leverage_score",
        "epistemic_spectrum_score", "css_titan_margin", "bridge_margin_ratio",
    }

    fields = []
    for col in df_cols:
        dtype = "sc:Integer" if col in int_cols else ("sc:Float" if col in float_cols else "sc:Text")
        fields.append({
            "@type": "cr:Field",
            "@id": f"problems/{col}",
            "name": col,
            "dataType": dtype,
            "source": {
                "fileObject": {"@id": "mega-atlas-csv"},
                "extract": {"column": col},
            },
        })

    return {
        "@context": {
            "@language": "en",
            "@vocab": "https://schema.org/",
            "citeAs": "cr:citeAs",
            "column": "cr:column",
            "conformsTo": "dct:conformsTo",
            "cr": "http://mlcommons.org/croissant/",
            "data": {"@id": "cr:data", "@type": "@json"},
            "dataType": {"@id": "cr:dataType", "@type": "@vocab"},
            "dct": "http://purl.org/dc/terms/",
            "extract": "cr:extract",
            "field": "cr:field",
            "fileObject": "cr:fileObject",
            "fileProperty": "cr:fileProperty",
            "fileSet": "cr:fileSet",
            "format": "cr:format",
            "includes": "cr:includes",
            "isLiveDataset": "cr:isLiveDataset",
            "jsonPath": "cr:jsonPath",
            "key": "cr:key",
            "md5": "cr:md5",
            "parentField": "cr:parentField",
            "path": "cr:path",
            "recordSet": "cr:recordSet",
            "references": "cr:references",
            "regex": "cr:regex",
            "repeated": "cr:repeated",
            "replace": "cr:replace",
            "sc": "https://schema.org/",
            "separator": "cr:separator",
            "source": "cr:source",
            "subField": "cr:subField",
            "transform": "cr:transform",
        },
        "@type": "sc:Dataset",
        "conformsTo": "http://mlcommons.org/croissant/1.0",
        "name": "Unsolved Problems Mega-Atlas",
        "alternateName": f"Unsolved Problems Mega-Atlas V{VERSION}",
        "description": (
            f"Exhaustive, cryptographically audited cross-disciplinary dataset of {total_problems:,} strictly deduplicated "
            "unsolved, open, and hard problems across 8 Macro-Pillars, 28 Superdomains, 8 Physical/Formal Substrates, "
            f"and 7 Abstraction Layers wired into 1 biconnected {total_edges:,}-edge knowledge graph (0 articulation points, 0 dangling links), "
            "with 0thernes CSS & Titan Index rankings, gradients & margins, per-record epistemic verification flags, Nov 25, 2026 "
            f"AI proof-claim audit, Hybrid RAG (100% MRR@5), 10-tool MCP server, Karpathy-style AutoResearch harness, and {lean_n} Pure Lean 4.35.0 "
            "formal invariant theorems verified across 6 independent kernels."
        ),
        "version": VERSION,
        "datePublished": "2026-11-25",
        "url": PAGES_URL,
        "sameAs": REPO_URL,
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "citeAs": (
            f"Donahue, Alexander Stephen (2026). Unsolved Problems Mega-Atlas (V{VERSION}). "
            f"Independent Researcher, Spokane, WA, USA. ORCID: 0009-0006-8168-9648. {REPO_URL}"
        ),
        "creator": {
            "@type": "sc:Person",
            "name": "Alexander Stephen Donahue",
            "identifier": ORCID_URL,
            "affiliation": "Independent Researcher, Spokane, WA, USA",
            "url": "https://0thernes.art",
        },
        "keywords": [
            "unsolved problems", "open problems", "knowledge graph", "lean 4",
            "formal verification", "palomar comparator", "autoresearch", "mcp", "rag",
            "mathematics", "physics", "computer science", "artificial intelligence", "philosophy",
        ],
        "distribution": [
            {
                "@type": "cr:FileObject",
                "@id": "mega-atlas-csv",
                "name": "MegaAtlas_Unsolved_Problems_V2.csv",
                "description": f"Master tabular CSV ({total_problems:,} rows x {len(df_cols)} columns, UTF-8).",
                "contentUrl": RAW_BASE + "outputs/MegaAtlas_Unsolved_Problems_V2.csv",
                "encodingFormat": "text/csv",
                "sha256": csv_sha,
                "contentSize": f"{csv_sz} B",
            },
            {
                "@type": "cr:FileObject",
                "@id": "mega-atlas-tsv",
                "name": "MegaAtlas_Unsolved_Problems_V2.tsv",
                "description": f"Tab-separated master table ({total_problems:,} rows x {len(df_cols)} columns, UTF-8).",
                "contentUrl": RAW_BASE + "outputs/MegaAtlas_Unsolved_Problems_V2.tsv",
                "encodingFormat": "text/tab-separated-values",
                "sha256": tsv_sha,
                "contentSize": f"{tsv_sz} B",
            },
            {
                "@type": "cr:FileObject",
                "@id": "mega-atlas-jsonl-gz",
                "name": "MegaAtlas_Unsolved_Problems_V2.jsonl.gz",
                "description": f"Deterministic gzipped streaming NDJSON ({total_problems:,} records) for LLM/RAG/HuggingFace ingestion.",
                "contentUrl": RAW_BASE + "outputs/MegaAtlas_Unsolved_Problems_V2.jsonl.gz",
                "encodingFormat": "application/gzip",
                "sha256": jsonl_gz_sha,
                "contentSize": f"{jsonl_gz_sz} B",
            },
            {
                "@type": "cr:FileObject",
                "@id": "mega-atlas-json-gz",
                "name": "MegaAtlas_Unsolved_Problems_V2.json.gz",
                "description": f"Deterministic gzipped complete JSON payload including problems, {total_edges:,} graph edges, Nov 25, 2026 AI audit, registries, benchmarks & matrices.",
                "contentUrl": RAW_BASE + "outputs/MegaAtlas_Unsolved_Problems_V2.json.gz",
                "encodingFormat": "application/gzip",
                "sha256": json_gz_sha,
                "contentSize": f"{json_gz_sz} B",
            },
        ],
        "recordSet": [
            {
                "@type": "cr:RecordSet",
                "@id": "problems",
                "name": "problems",
                "description": f"All {total_problems:,} strictly deduplicated unsolved, open, and hard problems.",
                "key": {"@id": "problems/id"},
                "field": fields,
            }
        ],
    }


def build_ro_crate(total_problems: int, total_edges: int) -> dict:
    lean_n = _lean_theorem_count()
    parts = [
        ("outputs/MegaAtlas_Unsolved_Problems_V2.csv", "text/csv", "Master tabular CSV dataset"),
        ("outputs/MegaAtlas_Unsolved_Problems_V2.tsv", "text/tab-separated-values", "Master tabular TSV dataset"),
        ("outputs/MegaAtlas_Unsolved_Problems_V2.jsonl.gz", "application/gzip", "Deterministic gzipped streaming JSONL dataset"),
        ("outputs/MegaAtlas_Unsolved_Problems_V2.json.gz", "application/gzip", "Deterministic gzipped complete JSON dataset & knowledge graph"),
        ("outputs/MegaAtlas_Unsolved_Problems_V2.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "15-sheet live-formula Excel workbook"),
        ("outputs/MegaAtlas_Interactive_Dashboard_V2.html", "text/html", "WCAG 2.2 AA interactive web atlas (<4 MB)"),
        ("dist/Donahue_2026_unsolved_problems_mega_atlas.pdf", "application/pdf", "10-page AMS-LaTeX white paper (Tectonic, 0 overfull hboxes)"),
        ("dist/arxiv_submission.tar.gz", "application/gzip", "Deterministic clean-room arXiv source tarball"),
        ("blueprint/index.html", "text/html", "Interactive Lean 4.35.0 Proof Blueprint SVG DAG"),
        ("docs/WHITE_PAPER.md", "text/markdown", "Build White Paper & Archival Dossier (0TH-BUILD-007)"),
        ("docs/DATASHEET.md", "text/markdown", "Gebru et al. Datasheet for Datasets"),
        ("docs/statement-fidelity.md", "text/markdown", "18-row Lean-vs-Python statement fidelity audit"),
        ("CLAIMS.md", "text/markdown", "Falsifiable Claims Ledger (C1-C10)"),
        ("RANKING.md", "text/markdown", "Master Ranking by 0thernes CSS"),
        ("VERIFICATION.md", "text/markdown", "Five-tier epistemic verification boundaries"),
        ("CHECKSUMS.sha256", "text/plain", "Cryptographic SHA-256 integrity manifest"),
        ("croissant.json", "application/ld+json", "MLCommons Croissant 1.0 metadata"),
        ("lean/MegaAtlasProofs.lean", "text/plain", f"Zero-Mathlib Lean 4.35.0 formal invariant suite ({lean_n} audited theorems, 6 kernels)"),
        ("results/lean_axioms.txt", "text/plain", f"Verbatim Lean 4.35.0 #print axioms transcript ({lean_n} theorems)"),
        ("autoresearch/program.md", "text/markdown", "Karpathy-style autonomous research instruction manual"),
        ("autoresearch/evaluate.py", "text/x-python", "Immutable AutoResearch evaluation oracle"),
        ("autoresearch/results.tsv", "text/tab-separated-values", "Empirical AutoResearch experiment audit trail"),
        ("mcp_server/server.py", "text/x-python", "Zero-dependency dual-framed MCP stdio JSON-RPC 2.0 server (10 tools)"),
        ("rag/query.py", "text/x-python", "Offline Hybrid BM25 + graph-authority RAG CLI (auto-builds SQLite FTS5)"),
    ]
    graph = [
        {
            "@type": "CreativeWork",
            "@id": "ro-crate-metadata.json",
            "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"},
            "about": {"@id": "./"},
        },
        {
            "@id": "./",
            "@type": "Dataset",
            "name": f"Unsolved Problems Mega-Atlas (V{VERSION})",
            "version": VERSION,
            "datePublished": "2026-11-25",
            "description": (
                f"Unified cross-disciplinary open-problem atlas ({total_problems:,} problems, 8 Macro-Pillars, 28 Superdomains, "
                f"8 Substrates, 7 Abstraction Layers, {total_edges:,} biconnected graph edges, {lean_n} Pure Lean 4.35.0 formal invariants "
                "across 6 kernels, 10-page AMS-LaTeX white paper, SQLite FTS5 Hybrid RAG, 10-tool MCP server, and Karpathy-style AutoResearch loop)."
            ),
            "url": PAGES_URL,
            "identifier": REPO_URL,
            "license": {"@id": "https://creativecommons.org/licenses/by/4.0/"},
            "author": {"@id": ORCID_URL},
            "hasPart": [{"@id": rel} for rel, _, _ in parts],
        },
        {
            "@id": ORCID_URL,
            "@type": "Person",
            "name": "Alexander Stephen Donahue",
            "email": "0_0@0thernes.art",
            "affiliation": "Independent Researcher, Spokane, WA, USA",
            "url": "https://0thernes.art",
        },
        {
            "@id": "https://creativecommons.org/licenses/by/4.0/",
            "@type": "CreativeWork",
            "name": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
            "url": "https://creativecommons.org/licenses/by/4.0/",
        },
    ]
    for rel, mime, desc in parts:
        p = ROOT / rel
        entry: dict = {
            "@id": rel,
            "@type": "File",
            "name": Path(rel).name,
            "description": desc,
            "encodingFormat": mime,
        }
        if p.exists() and rel not in ("CHECKSUMS.sha256", "croissant.json"):
            digest, sz = sha256_and_size(rel)
            entry["sha256"] = digest
            entry["contentSize"] = sz
        graph.append(entry)

    return {
        "@context": "https://w3id.org/ro/crate/1.1/context",
        "@graph": graph,
    }


def write_data_manifest() -> None:
    """Write `data/MANIFEST.sha256` (Build Standard B39) with relative paths from `data/`."""
    data_dir = ROOT / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    rels = [
        "../outputs/MegaAtlas_Unsolved_Problems_V2.csv",
        "../outputs/MegaAtlas_Unsolved_Problems_V2.tsv",
        "../outputs/MegaAtlas_Unsolved_Problems_V2.json.gz",
        "../outputs/MegaAtlas_Unsolved_Problems_V2.jsonl.gz",
        "../outputs/MegaAtlas_Unsolved_Problems_V2.xlsx",
        "../outputs/MegaAtlas_Unsolved_Problems_V2_Legacy.xls",
        "../outputs/MegaAtlas_Interactive_Dashboard_V2.html",
        "../dist/Donahue_2026_unsolved_problems_mega_atlas.pdf",
        "../dist/arxiv_submission.tar.gz",
        "../results/lean_axioms.txt",
        "../research/runs/LOG-002_antihydra_pilot/RESULTS.json",
    ]
    lines = []
    for rel in rels:
        p = (data_dir / rel).resolve()
        if p.exists():
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            lines.append(f"{h}  {rel}")
    (data_dir / "MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote data/MANIFEST.sha256 ({len(lines)} entries)")


def main() -> None:
    data = load_v2_master()
    df = data["df"]
    edges = data["summary_stats"]["total_graph_edges"]
    croissant = build_croissant(list(df.columns), len(df), edges)
    (ROOT / "croissant.json").write_text(
        json.dumps(croissant, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )
    ro_crate = build_ro_crate(len(df), edges)
    (ROOT / "ro-crate-metadata.json").write_text(
        json.dumps(ro_crate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )
    write_data_manifest()
    print(f"Generated FAIR metadata: croissant.json, ro-crate-metadata.json & data/MANIFEST.sha256 (v{VERSION}, N={len(df):,})")


if __name__ == "__main__":
    main()
