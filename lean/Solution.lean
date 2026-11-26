module
-- SPDX-License-Identifier: Apache-2.0
-- Copyright (c) 2026 Alexander Stephen Donahue

public import Challenge
public import MegaAtlasProofs

/-!
# Verified Solution Module (`M1`–`M7` + Master Conjunction)

Zero-`sorry`, zero-`native_decide`, zero-Mathlib proofs of all 7 headline
specification theorems and the master conjunction `prove_all_mega_atlas_invariants`.
-/

namespace MegaAtlasProofs.Solution

open MegaAtlasProofs.Challenge
open MegaAtlasProofs.Scoring
open MegaAtlasProofs.Quadrants
open MegaAtlasProofs.Taxonomy
open MegaAtlasProofs.GraphInvariants
open MegaAtlasProofs.AutoResearchInvariants
open MegaAtlasProofs.LayerGradients
open MegaAtlasProofs.NonVacuity
open MegaAtlasProofs.AdversarialTests

@[expose] public section

theorem m1_scoring_invariants : M1_ScoringInvariants :=
  ⟨css_weights_sum,
   titan_weights_sum,
   ageScoreCentis_le_cap,
   ageScoreCentis_saturates_at_300,
   fun _ _ _ _ hd hc ha => cssBps_le_max hd hc ha,
   fun _ _ _ _ hd hc => cssBps_ge_valid_min hd hc,
   fun _ _ _ _ _ h => cssBps_mono_diff h,
   fun _ _ _ _ _ h => cssBps_anti_tract h,
   fun _ _ _ _ hd1 hd2 hi1 hi2 hr1 hr2 hdeg => titanCentis_bounds hd1 hd2 hi1 hi2 hr1 hr2 hdeg,
   fun _ _ hi1 hi2 ht1 ht2 => leverageTenths_bounds hi1 hi2 ht1 ht2⟩

theorem m2_quadrant_and_era_invariants : M2_QuadrantAndEraInvariants :=
  ⟨classify_eq_Q1_iff,
   classify_eq_Q2_iff,
   classify_eq_Q3_iff,
   classify_eq_Q4_iff,
   fun _ _ h => Q1_leverage_ge_56 h,
   fun _ _ h => computeEra_mono h⟩

theorem m3_taxonomy_invariants : M3_TaxonomyInvariants :=
  ⟨pillar_count_eq_8,
   superdomain_count_eq_28,
   pillar_partition_sizes,
   allSuperdomains_complete,
   allPillars_complete,
   pillarOf_surjective,
   cross_pillar_implies_cross_superdomain⟩

theorem m4_graph_and_dedup_invariants : M4_GraphAndDedupInvariants :=
  ⟨fun _ _ vs hnd es hclosed => handshaking_lemma vs hnd es hclosed,
   fun _ sd es => edge_hierarchy sd es,
   fun _ _ _ key seen xs => dedupBy_length_le key seen xs⟩

theorem m5_autoresearch_ratchet_invariants : M5_AutoResearchRatchetInvariants :=
  ⟨aqs_weights_sum,
   fun _ _ _ _ _ hs hr hp hg hf => aqsBps_le_max hs hr hp hg hf,
   failed_gates_always_discard,
   shouldKeep_iff,
   updateBest_nondecreasing,
   metricDelta_self,
   metricDelta_antisymm⟩

theorem m6_layer_gradient_margin_invariants : M6_LayerGradientMarginInvariants :=
  ⟨substrate_count_eq_8,
   layer_count_eq_7,
   allSubstrates_complete,
   layerIndex_le_6,
   fun _ _ hd1 hd2 ht1 ht2 => hardnessTractGradient_bounds hd1 hd2 ht1 ht2,
   fun _ _ hc1 hc2 ht1 ht2 => cssTitanMarginBps_bounds hc1 hc2 ht1 ht2,
   fun _ _ h => bridgeMarginBps_le_10000 h,
   apexKeystone_requires_3_adjacent⟩

theorem m7_nonvacuity_certificate : M7_NonVacuityCertificate :=
  nonvac_all_hypotheses

theorem m8_adversarial_refutations : M8_AdversarialRefutations :=
  ⟨refute_css_strictly_below_10000,
   refute_age_saturates_at_299,
   refute_titan_strictly_below_1000,
   refute_Q1_leverage_ge_57,
   refute_Q2_leverage_ge_56,
   refute_superdomain_count_27,
   refute_handshaking_factor_3,
   refute_autoresearch_keeps_failed_gates,
   refute_apex_keystone_at_2_adjacent,
   refute_trans_pillar_at_2999_bps⟩

theorem prove_all_mega_atlas_invariants : AllMegaAtlasInvariants :=
  ⟨m1_scoring_invariants,
   m2_quadrant_and_era_invariants,
   m3_taxonomy_invariants,
   m4_graph_and_dedup_invariants,
   m5_autoresearch_ratchet_invariants,
   m6_layer_gradient_margin_invariants,
   m7_nonvacuity_certificate,
   m8_adversarial_refutations⟩

end

end MegaAtlasProofs.Solution
