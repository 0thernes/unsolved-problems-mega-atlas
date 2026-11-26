module
-- SPDX-License-Identifier: Apache-2.0
-- Copyright (c) 2026 Alexander Stephen Donahue

public import Challenge
public import Solution

/-!
# Palomar Comparator Verified Solution (`unsolved-problems-mega-atlas`)

Zero-`sorry`, zero-`native_decide`, zero-Mathlib implementation of every theorem declared
in `palomar/PalomarChallenge.lean`, verified by `lake comparator --config comparator.json --paranoid`
across all six independent Lean 4.35.0 proof kernels.
-/

namespace MegaAtlasProofs.Palomar

open MegaAtlasProofs.Challenge

public theorem m1_scoring_invariants : M1_ScoringInvariants :=
  MegaAtlasProofs.Solution.m1_scoring_invariants

public theorem m2_quadrant_and_era_invariants : M2_QuadrantAndEraInvariants :=
  MegaAtlasProofs.Solution.m2_quadrant_and_era_invariants

public theorem m3_taxonomy_invariants : M3_TaxonomyInvariants :=
  MegaAtlasProofs.Solution.m3_taxonomy_invariants

public theorem m4_graph_and_dedup_invariants : M4_GraphAndDedupInvariants :=
  MegaAtlasProofs.Solution.m4_graph_and_dedup_invariants

public theorem m5_autoresearch_ratchet_invariants : M5_AutoResearchRatchetInvariants :=
  MegaAtlasProofs.Solution.m5_autoresearch_ratchet_invariants

public theorem m6_layer_gradient_margin_invariants : M6_LayerGradientMarginInvariants :=
  MegaAtlasProofs.Solution.m6_layer_gradient_margin_invariants

public theorem m7_nonvacuity_certificate : M7_NonVacuityCertificate :=
  MegaAtlasProofs.Solution.m7_nonvacuity_certificate

public theorem prove_all_mega_atlas_invariants : AllMegaAtlasInvariants :=
  MegaAtlasProofs.Solution.prove_all_mega_atlas_invariants

end MegaAtlasProofs.Palomar
