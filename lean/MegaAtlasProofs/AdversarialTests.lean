module
-- SPDX-License-Identifier: Apache-2.0
-- Copyright (c) 2026 Alexander Stephen Donahue

public import MegaAtlasProofs.Scoring
public import MegaAtlasProofs.Quadrants
public import MegaAtlasProofs.Taxonomy
public import MegaAtlasProofs.GraphInvariants
public import MegaAtlasProofs.AutoResearchInvariants
public import MegaAtlasProofs.LayerGradients
public import MegaAtlasProofs.NonVacuity

/-!
# Adversarial Definition & False-Variant Refutation Suite (`MegaAtlasProofs.AdversarialTests`)

Per the **Defensible Independent AI Research Playbook v1.3 (Gold Standard Item 12)**:
proves constructively inside the Lean 4.35.0 kernel (`¬ (...)`, zero `sorry`,
zero `Classical.choice`, zero `native_decide`) that deliberately weakened,
tightened-beyond-truth, or off-by-one variants across ALL six formal modules
are provably `False`.
-/

namespace MegaAtlasProofs.AdversarialTests

open MegaAtlasProofs.Scoring
open MegaAtlasProofs.Quadrants
open MegaAtlasProofs.Taxonomy
open MegaAtlasProofs.GraphInvariants
open MegaAtlasProofs.AutoResearchInvariants
open MegaAtlasProofs.LayerGradients
open MegaAtlasProofs.NonVacuity

@[expose] public section

/-- Refutes falsely claiming CSS is strictly below 10000 bps (max attained at 100,100,100,0). -/
theorem refute_css_strictly_below_10000 :
    ¬ (∀ d c a t : Nat, d ≤ 100 → c ≤ 100 → a ≤ 100 → cssBps d c a t < 10000) := by
  intro h
  have h1 := h 100 100 100 0 (by decide) (by decide) (by decide)
  exact absurd h1 (by decide)

/-- Refutes off-by-one age saturation threshold at 299 years (must be 300). -/
theorem refute_age_saturates_at_299 :
    ¬ (∀ age : Nat, 299 ≤ age → ageScoreCentis age = 10000) := by
  intro h
  have h1 := h 299 (by decide)
  exact absurd h1 (by decide)

/-- Refutes falsely claiming Titan Index is strictly below 1000 centis (max attained at 10,10,10,100). -/
theorem refute_titan_strictly_below_1000 :
    ¬ (∀ d i r degT : Nat, 1 ≤ d → d ≤ 10 → 1 ≤ i → i ≤ 10 → 1 ≤ r → r ≤ 10 → degT ≤ 100 →
        titanCentis d i r degT < 1000) := by
  intro h
  have h1 := h 10 10 10 100 (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)
  exact absurd h1 (by decide)

/-- Refutes over-claiming Q1 leverage floor as >= 57 tenths (exact tight floor is 56 at 8*7). -/
theorem refute_Q1_leverage_ge_57 :
    ¬ (∀ imp tr : Nat, classifyQuadrant imp tr = .Q1 → 57 ≤ leverageTenths imp tr) := by
  intro h
  have h1 := h 8 7 (by decide)
  exact absurd h1 (by decide)

/-- Refutes falsely extending the Q1 leverage floor (56 tenths) to Q2. -/
theorem refute_Q2_leverage_ge_56 :
    ¬ (∀ imp tr : Nat, classifyQuadrant imp tr = .Q2 → 56 ≤ leverageTenths imp tr) := by
  intro h
  have h1 := h 8 6 (by decide)
  exact absurd h1 (by decide)

/-- Refutes wrong superdomain cardinality (must be exactly 28, not 27). -/
theorem refute_superdomain_count_27 :
    ¬ (allSuperdomains.length = 27) := by
  decide

/-- Refutes wrong Handshaking coefficient (sum of degrees is 2*|E|, never universally 3*|E|). -/
theorem refute_handshaking_factor_3 :
    ¬ (∀ (vs : List Nat), vs.Nodup → ∀ (es : List (Edge Nat)),
        (∀ e ∈ es, e.u ∈ vs ∧ e.v ∈ vs) →
        sumNat (vs.map (fun x => degreeOf x es)) = 3 * es.length) := by
  intro h
  have h1 := h sampleVertices nonvac_graph_triangle_witness.1 sampleEdges nonvac_graph_triangle_witness.2.1
  have h2 : sumNat (sampleVertices.map (fun x => degreeOf x sampleEdges)) = 6 := by decide
  have h3 : 3 * sampleEdges.length = 9 := by decide
  omega

/-- Refutes any AutoResearch reward-hacking claim where failed hard gates could be kept. -/
theorem refute_autoresearch_keeps_failed_gates :
    ¬ (∃ best cand : Nat, shouldKeep false best cand = true) := by
  intro ⟨best, cand, h⟩
  have h0 := failed_gates_always_discard best cand
  rw [h0] at h
  exact Bool.noConfusion h

/-- Refutes off-by-one apexKeystone threshold at adj >= 2 (must require adj >= 3). -/
theorem refute_apex_keystone_at_2_adjacent :
    ¬ (∀ adj crossSD bps : Nat, adj ≥ 2 → classifyMarginRole adj crossSD bps = .apexKeystone) := by
  intro h
  have h1 := h 2 3 3000 (by decide)
  exact absurd h1 (by decide)

/-- Refutes off-by-one transPillarMargin bridge ratio threshold at 2999 bps (must require >= 3000 bps). -/
theorem refute_trans_pillar_at_2999_bps :
    ¬ (∀ adj crossSD bps : Nat, adj ≥ 1 → bps ≥ 2999 → classifyMarginRole adj crossSD bps = .transPillarMargin) := by
  intro h
  have h1 := h 2 3 2999 (by decide) (by decide)
  exact absurd h1 (by decide)

end

end MegaAtlasProofs.AdversarialTests
