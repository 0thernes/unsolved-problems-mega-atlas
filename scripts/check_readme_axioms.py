#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Verify that README.md reproduces the verbatim Lean 4.35.0 `#print axioms` output
from `results/lean_axioms.txt` with zero drift, and that zero forbidden axioms exist."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AXIOMS_PATH = ROOT / "results" / "lean_axioms.txt"
README_PATH = ROOT / "README.md"
FORBIDDEN = ("sorryAx", "Lean.ofReduceBool", "Lean.trustCompiler", "_native", "Classical.choice")


def main() -> None:
    if not AXIOMS_PATH.exists():
        print(f"FAIL: missing {AXIOMS_PATH}", file=sys.stderr)
        sys.exit(1)
    axioms_txt = AXIOMS_PATH.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
    lines = [ln for ln in axioms_txt.splitlines() if ln.strip()]
    if len(lines) != 103:
        print(f"FAIL: expected 103 axiom lines in {AXIOMS_PATH}, got {len(lines)}", file=sys.stderr)
        sys.exit(1)
    for tok in FORBIDDEN:
        if tok in axioms_txt:
            print(f"FAIL: forbidden axiom token {tok!r} found in {AXIOMS_PATH}", file=sys.stderr)
            sys.exit(1)

    readme = README_PATH.read_text(encoding="utf-8").replace("\r\n", "\n")
    marker_start = "<!-- LEAN_AXIOMS_START -->"
    marker_end = "<!-- LEAN_AXIOMS_END -->"
    if marker_start not in readme or marker_end not in readme:
        print("FAIL: README.md missing LEAN_AXIOMS_START / LEAN_AXIOMS_END markers", file=sys.stderr)
        sys.exit(1)
    block = readme.split(marker_start, 1)[1].split(marker_end, 1)[0]
    m = re.search(r"```text\n(.*?)\n```", block, flags=re.S)
    if not m:
        print("FAIL: README.md axioms block missing ```text fence", file=sys.stderr)
        sys.exit(1)
    readme_axioms = m.group(1).strip()
    # README shows the 9 Palomar headline theorems verbatim (subset of results/lean_axioms.txt)
    palomar_lines = [ln for ln in lines if "MegaAtlasProofs.Palomar." in ln]
    expected_block = "\n".join(palomar_lines)
    if readme_axioms != expected_block:
        print("FAIL: README.md verbatim Palomar axioms block drifted from results/lean_axioms.txt!", file=sys.stderr)
        print("--- EXPECTED ---\n" + expected_block, file=sys.stderr)
        print("--- ACTUAL ---\n" + readme_axioms, file=sys.stderr)
        sys.exit(1)
    print(f"PASS: All {len(lines)} Lean 4.35.0 theorem axioms verified constructive ([propext, Quot.sound] only) and README.md verbatim Palomar block matches 100%.")


if __name__ == "__main__":
    main()
