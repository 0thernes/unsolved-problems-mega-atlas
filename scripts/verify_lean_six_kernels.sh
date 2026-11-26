#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
# Single-source six-kernel Lean 4.35.0 & Palomar Comparator verification script.
# Invoked identically by GitHub Actions CI (`ci.yml`), `just lean-kernels`, and local Linux users.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR/lean"

elan show
lake build
lake env lean MegaAtlasProofs/VerifyAxioms.lean > /tmp/ci_axioms.txt
cat /tmp/ci_axioms.txt

# Enforce zero sorry, zero native evaluation, zero Classical.choice, and exact frozen-axiom parity
if grep -E "sorryAx|_native|Lean\.ofReduceBool|Lean\.trustCompiler|Classical\.choice" /tmp/ci_axioms.txt; then
  echo "FAIL: forbidden axiom detected!" >&2
  exit 1
fi
diff -u --strip-trailing-cr ../results/lean_axioms.txt /tmp/ci_axioms.txt

# Replay Solution & PalomarSolution through leanchecker & paranoid checker
lake env leanchecker Solution
lake env leanchecker PalomarSolution
lake env leanchecker-paranoid Solution
lake env leanchecker-paranoid PalomarSolution

# Export headline PalomarSolution theorems and replay through con-leche, con-ron & nanoda_bin
lake env leanexport PalomarSolution -- \
  MegaAtlasProofs.Palomar.prove_all_mega_atlas_invariants \
  MegaAtlasProofs.NonVacuity.nonvac_all_hypotheses \
  MegaAtlasProofs.Palomar.m8_adversarial_refutations > /tmp/PalomarSolution.export
lake env con-leche --verified /tmp/PalomarSolution.export
lake env con-ron --verified /tmp/PalomarSolution.export

cat << 'EOF' > /tmp/nanoda.json
{
  "export_file_path": "/tmp/PalomarSolution.export",
  "use_stdin": false,
  "permitted_axioms": ["propext", "Quot.sound"],
  "unpermitted_axiom_hard_error": true,
  "nat_extension": true,
  "string_extension": true
}
EOF
lake env nanoda_bin /tmp/nanoda.json

# Sandboxed (bubblewrap) 6-kernel verification of all defaultTargets
lake check --paranoid

# Build and export PalomarChallenge (stored outside lean/ per ADR 0004 to preserve immutable evaluate.py)
lake build PalomarChallenge
lake env leanexport PalomarChallenge -- \
  Quot Quot.mk Quot.lift Quot.ind propext Quot.sound \
  MegaAtlasProofs.Palomar.m1_scoring_invariants \
  MegaAtlasProofs.Palomar.m2_quadrant_and_era_invariants \
  MegaAtlasProofs.Palomar.m3_taxonomy_invariants \
  MegaAtlasProofs.Palomar.m4_graph_and_dedup_invariants \
  MegaAtlasProofs.Palomar.m5_autoresearch_ratchet_invariants \
  MegaAtlasProofs.Palomar.m6_layer_gradient_margin_invariants \
  MegaAtlasProofs.Palomar.m7_nonvacuity_certificate \
  MegaAtlasProofs.Palomar.m8_adversarial_refutations \
  MegaAtlasProofs.Palomar.prove_all_mega_atlas_invariants \
  Nat.add Nat.sub Nat.mul Nat.pow Nat.gcd Nat.div Nat.mod Nat.beq Nat.ble \
  Nat.land Nat.lor Nat.xor Nat.shiftLeft Nat.shiftRight \
  String.ofList Char.ofNat List eagerReduce Nat String String.mk Char \
  optParam autoParam semiOutParam outParam > /tmp/PalomarChallenge.export

# Sandboxed (bubblewrap) 6-kernel Palomar Comparator verification against exported Challenge
lake comparator --config comparator.json --challenge-from-export=/tmp/PalomarChallenge.export --paranoid

echo "PASS: All 103 audited theorems and 9 Palomar targets verified across all 6 independent Lean 4.35.0 kernels!"
