-- SPDX-License-Identifier: Apache-2.0
-- Copyright (c) 2026 Alexander Stephen Donahue
/-
  MegaAtlasProofs/VerifyAxioms.lean
  Per-theorem `#print axioms` audit covering 103 of the 117 theorem declarations in `lean/`
  (72 public core module theorems + 12 concrete NonVacuity & boundary witnesses +
   10 constructive AdversarialTests refutations + 9 headline PalomarSolution contract
   theorems; excludes 5 private `sumNat_*` helper lemmas in `GraphInvariants.lean` and
   the 9 `Solution.*` aliases re-exported directly by `PalomarSolution.lean`).
  Each audited theorem must depend strictly on standard constructive kernel axioms
  within [propext, Quot.sound] (or empty) in its per-theorem `#print axioms` output
  — zero sorryAx, zero `_native`/Lean.ofReduceBool, zero custom axioms. Note: the
  whole-environment `lake check --paranoid` step over Lean core also lists `Classical.choice`.
-/

import MegaAtlasProofs.Scoring
import MegaAtlasProofs.Quadrants
import MegaAtlasProofs.Taxonomy
import MegaAtlasProofs.GraphInvariants
import MegaAtlasProofs.AutoResearchInvariants
import MegaAtlasProofs.LayerGradients
import MegaAtlasProofs.NonVacuity
import MegaAtlasProofs.AdversarialTests
import PalomarSolution

-- Scoring invariants (22 theorems)
#print axioms MegaAtlasProofs.Scoring.ageScoreCentis_le_cap
#print axioms MegaAtlasProofs.Scoring.ageScoreCentis_zero
#print axioms MegaAtlasProofs.Scoring.ageScoreCentis_saturates_at_300
#print axioms MegaAtlasProofs.Scoring.ageScoreCentis_mono
#print axioms MegaAtlasProofs.Scoring.css_weights_sum
#print axioms MegaAtlasProofs.Scoring.cssBps_le_max
#print axioms MegaAtlasProofs.Scoring.cssBps_ge_valid_min
#print axioms MegaAtlasProofs.Scoring.cssBps_mono_diff
#print axioms MegaAtlasProofs.Scoring.cssBps_mono_cent
#print axioms MegaAtlasProofs.Scoring.cssBps_mono_age
#print axioms MegaAtlasProofs.Scoring.cssBps_anti_tract
#print axioms MegaAtlasProofs.Scoring.cssBps_extreme_max
#print axioms MegaAtlasProofs.Scoring.cssBps_extreme_min
#print axioms MegaAtlasProofs.Scoring.titan_weights_sum
#print axioms MegaAtlasProofs.Scoring.titanCentis_bounds
#print axioms MegaAtlasProofs.Scoring.titanCentis_mono_diff
#print axioms MegaAtlasProofs.Scoring.titanCentis_mono_impact
#print axioms MegaAtlasProofs.Scoring.titanCentis_mono_interdisc
#print axioms MegaAtlasProofs.Scoring.titanCentis_mono_deg
#print axioms MegaAtlasProofs.Scoring.leverageTenths_bounds
#print axioms MegaAtlasProofs.Scoring.leverageTenths_comm
#print axioms MegaAtlasProofs.Scoring.leverageTenths_mono

-- Quadrant & Era invariants (11 theorems)
#print axioms MegaAtlasProofs.Quadrants.classify_eq_Q1_iff
#print axioms MegaAtlasProofs.Quadrants.classify_eq_Q2_iff
#print axioms MegaAtlasProofs.Quadrants.classify_eq_Q3_iff
#print axioms MegaAtlasProofs.Quadrants.classify_eq_Q4_iff
#print axioms MegaAtlasProofs.Quadrants.classify_exhaustive
#print axioms MegaAtlasProofs.Quadrants.highImpact_preserved
#print axioms MegaAtlasProofs.Quadrants.highTract_preserved
#print axioms MegaAtlasProofs.Quadrants.Q1_leverage_ge_56
#print axioms MegaAtlasProofs.Quadrants.computeEra_mono
#print axioms MegaAtlasProofs.Quadrants.computeEra_ancient_sample
#print axioms MegaAtlasProofs.Quadrants.computeEra_nov2026_sample

-- Taxonomy invariants (8 theorems)
#print axioms MegaAtlasProofs.Taxonomy.pillar_count_eq_8
#print axioms MegaAtlasProofs.Taxonomy.superdomain_count_eq_28
#print axioms MegaAtlasProofs.Taxonomy.pillar_partition_sizes
#print axioms MegaAtlasProofs.Taxonomy.pillar_partition_sum_28
#print axioms MegaAtlasProofs.Taxonomy.allSuperdomains_complete
#print axioms MegaAtlasProofs.Taxonomy.allPillars_complete
#print axioms MegaAtlasProofs.Taxonomy.pillarOf_surjective
#print axioms MegaAtlasProofs.Taxonomy.cross_pillar_implies_cross_superdomain

-- Graph & Deduplication invariants (5 theorems)
#print axioms MegaAtlasProofs.GraphInvariants.handshaking_lemma
#print axioms MegaAtlasProofs.GraphInvariants.cross_pillar_le_cross_superdomain
#print axioms MegaAtlasProofs.GraphInvariants.cross_superdomain_le_total
#print axioms MegaAtlasProofs.GraphInvariants.edge_hierarchy
#print axioms MegaAtlasProofs.GraphInvariants.dedupBy_length_le

-- AutoResearch & Comparator invariants (12 theorems)
#print axioms MegaAtlasProofs.AutoResearchInvariants.aqs_weights_sum
#print axioms MegaAtlasProofs.AutoResearchInvariants.aqsBps_le_max
#print axioms MegaAtlasProofs.AutoResearchInvariants.aqsBps_extreme_max
#print axioms MegaAtlasProofs.AutoResearchInvariants.aqsBps_mono_rag
#print axioms MegaAtlasProofs.AutoResearchInvariants.aqsBps_mono_provenance
#print axioms MegaAtlasProofs.AutoResearchInvariants.aqsBps_mono_formal
#print axioms MegaAtlasProofs.AutoResearchInvariants.failed_gates_always_discard
#print axioms MegaAtlasProofs.AutoResearchInvariants.shouldKeep_iff
#print axioms MegaAtlasProofs.AutoResearchInvariants.updateBest_nondecreasing
#print axioms MegaAtlasProofs.AutoResearchInvariants.updateBest_strict_on_keep
#print axioms MegaAtlasProofs.AutoResearchInvariants.metricDelta_self
#print axioms MegaAtlasProofs.AutoResearchInvariants.metricDelta_antisymm

-- Substrate, Abstraction-Layer, Gradient, Margin & Adjacent invariants (14 theorems)
#print axioms MegaAtlasProofs.LayerGradients.substrate_count_eq_8
#print axioms MegaAtlasProofs.LayerGradients.layer_count_eq_7
#print axioms MegaAtlasProofs.LayerGradients.allSubstrates_complete
#print axioms MegaAtlasProofs.LayerGradients.layerIndex_le_6
#print axioms MegaAtlasProofs.LayerGradients.hardnessTractGradient_bounds
#print axioms MegaAtlasProofs.LayerGradients.hardnessTractGradient_zero_iff
#print axioms MegaAtlasProofs.LayerGradients.hardnessTractGradient_mono_diff
#print axioms MegaAtlasProofs.LayerGradients.hardnessTractGradient_anti_tract
#print axioms MegaAtlasProofs.LayerGradients.cssTitanMarginBps_bounds
#print axioms MegaAtlasProofs.LayerGradients.bridgeMarginBps_le_10000
#print axioms MegaAtlasProofs.LayerGradients.bridgeMarginBps_zero_when_no_cross
#print axioms MegaAtlasProofs.LayerGradients.adjacent_pillars_lt_8
#print axioms MegaAtlasProofs.LayerGradients.marginRole_exhaustive
#print axioms MegaAtlasProofs.LayerGradients.apexKeystone_requires_3_adjacent

-- Concrete Non-Vacuity & Negative Boundary Witnesses (12 theorems)
#print axioms MegaAtlasProofs.NonVacuity.nonvac_scoring_valid_witness
#print axioms MegaAtlasProofs.NonVacuity.boundary_age_299_not_saturated
#print axioms MegaAtlasProofs.NonVacuity.nonvac_all_four_quadrants
#print axioms MegaAtlasProofs.NonVacuity.boundary_non_Q1_leverage_below_56
#print axioms MegaAtlasProofs.NonVacuity.nonvac_all_six_eras
#print axioms MegaAtlasProofs.NonVacuity.nonvac_graph_triangle_witness
#print axioms MegaAtlasProofs.NonVacuity.nonvac_dedup_strict_shrink
#print axioms MegaAtlasProofs.NonVacuity.nonvac_autoresearch_keep_and_discard
#print axioms MegaAtlasProofs.NonVacuity.nonvac_all_four_margin_roles
#print axioms MegaAtlasProofs.NonVacuity.nonvac_gradient_and_margin_extremes
#print axioms MegaAtlasProofs.NonVacuity.nonvac_taxonomy_cross_pillar_witness
#print axioms MegaAtlasProofs.NonVacuity.nonvac_all_hypotheses

-- Constructive Adversarial Definition Refutations (10 theorems; Playbook Item 12)
#print axioms MegaAtlasProofs.AdversarialTests.refute_css_strictly_below_10000
#print axioms MegaAtlasProofs.AdversarialTests.refute_age_saturates_at_299
#print axioms MegaAtlasProofs.AdversarialTests.refute_titan_strictly_below_1000
#print axioms MegaAtlasProofs.AdversarialTests.refute_Q1_leverage_ge_57
#print axioms MegaAtlasProofs.AdversarialTests.refute_Q2_leverage_ge_56
#print axioms MegaAtlasProofs.AdversarialTests.refute_superdomain_count_27
#print axioms MegaAtlasProofs.AdversarialTests.refute_handshaking_factor_3
#print axioms MegaAtlasProofs.AdversarialTests.refute_autoresearch_keeps_failed_gates
#print axioms MegaAtlasProofs.AdversarialTests.refute_apex_keystone_at_2_adjacent
#print axioms MegaAtlasProofs.AdversarialTests.refute_trans_pillar_at_2999_bps

-- Palomar Comparator Headline Contract Theorems (9 theorems)
#print axioms MegaAtlasProofs.Palomar.m1_scoring_invariants
#print axioms MegaAtlasProofs.Palomar.m2_quadrant_and_era_invariants
#print axioms MegaAtlasProofs.Palomar.m3_taxonomy_invariants
#print axioms MegaAtlasProofs.Palomar.m4_graph_and_dedup_invariants
#print axioms MegaAtlasProofs.Palomar.m5_autoresearch_ratchet_invariants
#print axioms MegaAtlasProofs.Palomar.m6_layer_gradient_margin_invariants
#print axioms MegaAtlasProofs.Palomar.m7_nonvacuity_certificate
#print axioms MegaAtlasProofs.Palomar.m8_adversarial_refutations
#print axioms MegaAtlasProofs.Palomar.prove_all_mega_atlas_invariants
