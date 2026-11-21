/-
  MegaAtlasProofs/VerifyAxioms.lean
  Axiom-allowlist audit across ALL 58 formal theorems in MegaAtlasProofs.
  Every theorem must depend strictly on standard kernel axioms within
  [propext, Quot.sound] (or empty) — zero sorryAx, zero Lean.ofReduceBool,
  zero Classical.choice, zero custom axioms.
-/

import MegaAtlasProofs.Scoring
import MegaAtlasProofs.Quadrants
import MegaAtlasProofs.Taxonomy
import MegaAtlasProofs.GraphInvariants
import MegaAtlasProofs.AutoResearchInvariants

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
