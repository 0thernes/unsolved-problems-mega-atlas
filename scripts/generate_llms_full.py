#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Deterministically generate `llms-full.txt` from the canonical repo documentation
and Lean formal specification (Build Standard A32)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SECTIONS = [
    ("README.md", "Project Overview & Quick Start"),
    ("AGENTS.md", "Agent Entry Point & Hard Rules"),
    ("CLAIMS.md", "Falsifiable Claims Ledger"),
    ("VERIFICATION.md", "Epistemic Verification Boundaries"),
    ("LIMITATIONS.md", "Known Limitations & Literal vs. Metaphor Table"),
    ("docs/statement-fidelity.md", "Lean 4.35.0 Statement-Fidelity Audit"),
    ("lean/Challenge.lean", "Formal Lean 4.35.0 Challenge Specification (M1-M7)"),
    ("results/lean_axioms.txt", "Verbatim 92-Theorem Lean 4.35.0 Axiom Audit"),
    ("REPLICATION.md", "Clean-Clone Replication Protocol & Log"),
]


def main() -> None:
    ver = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    out = [
        f"# Unsolved Problems Mega-Atlas (v{ver}) — Complete Agent Context (`llms-full.txt`)",
        "",
        "> Generated deterministically by `python scripts/generate_llms_full.py`.",
        "> Author: Alexander Stephen Donahue (Independent Researcher, Spokane, WA, USA; ORCID 0009-0006-8168-9648).",
        "> License: CC-BY-4.0 (data/prose) / Apache-2.0 (code/Lean).",
        "",
    ]
    for rel, title in SECTIONS:
        p = ROOT / rel
        if not p.exists():
            continue
        out.append("=" * 80)
        out.append(f"## FILE: {rel} — {title}")
        out.append("=" * 80)
        out.append("")
        out.append(p.read_text(encoding="utf-8").replace("\r\n", "\n").strip())
        out.append("")

    target = ROOT / "llms-full.txt"
    target.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    print(f"Generated {target} ({target.stat().st_size:,} bytes, {len(SECTIONS)} sections)")


if __name__ == "__main__":
    main()
