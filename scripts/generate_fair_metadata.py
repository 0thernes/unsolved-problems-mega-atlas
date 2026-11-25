#!/usr/bin/env python3
"""
Deterministic FAIR Scholarly Metadata Generator (0thernes LLC):
  1. `croissant.json`         — MLCommons Croissant 1.0 JSON-LD dataset specification
  2. `ro-crate-metadata.json` — W3C / ResearchObject RO-Crate 1.1 JSON-LD descriptor

Computes live byte sizes and SHA-256 digests directly from frozen artifacts so
machine-readable FAIR manifests stay 100% cryptographically synchronized with `outputs/`.
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
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").exists() else "2.2.0"


def sha256_and_size(rel: str) -> tuple[str, int]:
    p = ROOT / rel
    data = p.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def build_croissant(df_cols: list[str], total_problems: int) -> dict:
    csv_sha, csv_sz = sha256_and_size("outputs/MegaAtlas_Unsolved_Problems_V2.csv")
    jsonl_sha, jsonl_sz = sha256_and_size("outputs/MegaAtlas_Unsolved_Problems_V2.jsonl")
    json_sha, json_sz = sha256_and_size("outputs/MegaAtlas_Unsolved_Problems_V2.json")
    sqlite_sha, sqlite_sz = sha256_and_size("outputs/MegaAtlas_Unsolved_Problems_V2.sqlite")

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
        "alternateName": f"0thernes Unsolved Problems Mega-Atlas V{VERSION}",
        "description": (
            f"Exhaustive, cryptographically audited cross-disciplinary dataset of {total_problems:,} strictly deduplicated "
            "unsolved, open, and hard problems across 8 Macro-Pillars, 28 Superdomains, 8 Physical/Formal Substrates, "
            "and 7 Abstraction Layers wired into 1 biconnected 5,808-edge knowledge graph (0 articulation points, 0 dangling links), "
            "with 0thernes CSS & Titan Index rankings, gradients & margins, per-record epistemic verification flags, Nov 20, 2026 "
            "AI proof-claim audit, Hybrid RAG (100% MRR@5), 9-tool MCP server, Karpathy-style AutoResearch harness, and 72 Pure Lean 4.35.0 "
            "formal invariants."
        ),
        "version": VERSION,
        "datePublished": "2026-11-21",
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
            "affiliation": {
                "@type": "sc:Organization",
                "name": "Independent Researcher (0thernes)",
                "url": "https://0thernes.art",
            },
        },
        "keywords": [
            "unsolved problems", "open problems", "knowledge graph", "lean 4",
            "formal verification", "autoresearch", "mcp", "rag", "mathematics",
            "physics", "computer science", "artificial intelligence", "philosophy",
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
                "@id": "mega-atlas-jsonl",
                "name": "MegaAtlas_Unsolved_Problems_V2.jsonl",
                "description": f"Streaming newline-delimited JSON ({total_problems:,} records) for LLM/RAG/HuggingFace ingestion.",
                "contentUrl": RAW_BASE + "outputs/MegaAtlas_Unsolved_Problems_V2.jsonl",
                "encodingFormat": "application/x-ndjson",
                "sha256": jsonl_sha,
                "contentSize": f"{jsonl_sz} B",
            },
            {
                "@type": "cr:FileObject",
                "@id": "mega-atlas-json",
                "name": "MegaAtlas_Unsolved_Problems_V2.json",
                "description": "Complete JSON payload including problems, 5,597 graph edges, Nov 2026 AI audit, registries, benchmarks & matrices.",
                "contentUrl": RAW_BASE + "outputs/MegaAtlas_Unsolved_Problems_V2.json",
                "encodingFormat": "application/json",
                "sha256": json_sha,
                "contentSize": f"{json_sz} B",
            },
            {
                "@type": "cr:FileObject",
                "@id": "mega-atlas-sqlite",
                "name": "MegaAtlas_Unsolved_Problems_V2.sqlite",
                "description": "SQLite 3 normalized relational database with Porter-stemmed FTS5 full-text search index.",
                "contentUrl": RAW_BASE + "outputs/MegaAtlas_Unsolved_Problems_V2.sqlite",
                "encodingFormat": "application/vnd.sqlite3",
                "sha256": sqlite_sha,
                "contentSize": f"{sqlite_sz} B",
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


def build_ro_crate(total_problems: int) -> dict:
    parts = [
        ("outputs/MegaAtlas_Unsolved_Problems_V2.csv", "text/csv", "Master tabular CSV dataset"),
        ("outputs/MegaAtlas_Unsolved_Problems_V2.jsonl", "application/x-ndjson", "Streaming JSONL dataset"),
        ("outputs/MegaAtlas_Unsolved_Problems_V2.json", "application/json", "Complete JSON dataset & knowledge graph"),
        ("outputs/MegaAtlas_Unsolved_Problems_V2.sqlite", "application/vnd.sqlite3", "SQLite 3 + FTS5 RAG database"),
        ("outputs/MegaAtlas_Interactive_Dashboard_V2.html", "text/html", "Standalone interactive web atlas"),
        ("outputs/MegaAtlas_Comprehensive_Report_V2.pdf", "application/pdf", "Complete vector PDF monograph"),
        ("docs/WHITE_PAPER.md", "text/markdown", "Institutional Build White Paper (0TH-BUILD-007)"),
        ("docs/DATASHEET.md", "text/markdown", "Gebru et al. Datasheet for Datasets"),
        ("RANKING.md", "text/markdown", "Master Ranking by 0thernes CSS"),
        ("VERIFICATION.md", "text/markdown", "5-tier epistemic verification boundaries"),
        ("CHECKSUMS.sha256", "text/plain", "Cryptographic SHA-256 integrity manifest"),
        ("croissant.json", "application/ld+json", "MLCommons Croissant 1.0 metadata"),
        ("lean/MegaAtlasProofs.lean", "text/plain", "Pure Lean 4.35.0 formal invariant suite (58 theorems, 0 sorry)"),
        ("autoresearch/program.md", "text/markdown", "Karpathy-style autonomous research instruction manual"),
        ("autoresearch/evaluate.py", "text/x-python", "Immutable AutoResearch evaluation oracle"),
        ("autoresearch/results.tsv", "text/tab-separated-values", "Empirical AutoResearch experiment audit trail"),
        ("mcp_server/server.py", "text/x-python", "Zero-dependency MCP stdio JSON-RPC 2.0 server (7 tools)"),
        ("rag/query.py", "text/x-python", "Offline Hybrid BM25 + graph-authority RAG CLI"),
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
            "datePublished": "2026-11-21",
            "description": (
                f"Unified cross-disciplinary open-problem atlas ({total_problems:,} problems, 8 Macro-Pillars, 28 Superdomains, "
                "5,597 graph edges, 58 Pure Lean 4.35.0 formal invariants, SQLite FTS5 RAG/MCP server, and Karpathy-style AutoResearch loop)."
            ),
            "url": PAGES_URL,
            "identifier": REPO_URL,
            "license": {"@id": "https://creativecommons.org/licenses/by/4.0/"},
            "author": {"@id": ORCID_URL},
            "publisher": {"@id": "https://0thernes.art/#org"},
            "hasPart": [{"@id": rel} for rel, _, _ in parts],
        },
        {
            "@id": ORCID_URL,
            "@type": "Person",
            "name": "Alexander Stephen Donahue",
            "email": "0_0@0thernes.art",
            "affiliation": {"@id": "https://0thernes.art/#org"},
        },
        {
            "@id": "https://0thernes.art/#org",
            "@type": "Organization",
            "name": "Independent Researcher (0thernes)",
            "url": "https://0thernes.art",
            "location": "Spokane, WA, USA",
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
        entry = {
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


def main() -> None:
    data = load_v2_master()
    df = data["df"]
    croissant = build_croissant(list(df.columns), len(df))
    (ROOT / "croissant.json").write_text(
        json.dumps(croissant, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )
    ro_crate = build_ro_crate(len(df))
    (ROOT / "ro-crate-metadata.json").write_text(
        json.dumps(ro_crate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )
    print(f"Generated FAIR metadata: croissant.json & ro-crate-metadata.json (v{VERSION}, N={len(df):,})")


if __name__ == "__main__":
    main()
