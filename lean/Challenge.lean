module
-- SPDX-License-Identifier: Apache-2.0
-- Copyright (c) 2026 Alexander Stephen Donahue

public import MegaAtlasProofs

/-!
# Formal Challenge Specification (`M1`–`M7`)

Clean exported theorem specification contract for independent 6-kernel verification
(`lean`, `leanchecker`, `leanchecker-paranoid`, `lean4lean`, `nanoda_bin`, `con-leche`,
`con-ron` via `lake comparator --config comparator.json --paranoid`).
All proofs live in `Solution.lean` and `MegaAtlasProofs.*`.
-/

namespace MegaAtlasProofs.Challenge

open MegaAtlasProofs.Scoring
open MegaAtlasProofs.Quadrants
open MegaAtlasProofs.Taxonomy
open MegaAtlasProofs.GraphInvariants
open MegaAtlasProofs.AutoResearchInvariants
open MegaAtlasProofs.LayerGradients
open MegaAtlasProofs.NonVacuity

@[expose] public section

def M1_ScoringInvariants : Prop :=
  (40 + 30 + 20 + 10 = 100) ∧
  (35 + 35 + 20 + 10 = 100) ∧
  (∀ ageYears : Nat, ageScoreCentis ageYears ≤ 10000) ∧
  (∀ ageYears : Nat, 300 ≤ ageYears → ageScoreCentis ageYears = 10000) ∧
  (∀ d c a t : Nat, d ≤ 100 → c ≤ 100 → a ≤ 100 → cssBps d c a t ≤ 10000) ∧
  (∀ d c a t : Nat, 10 ≤ d → 5 ≤ c → 550 ≤ cssBps d c a t) ∧
  (∀ d₁ d₂ c a t : Nat, d₁ ≤ d₂ → cssBps d₁ c a t ≤ cssBps d₂ c a t) ∧
  (∀ d c a t₁ t₂ : Nat, t₁ ≤ t₂ → cssBps d c a t₂ ≤ cssBps d c a t₁) ∧
  (∀ d i r degT : Nat, 1 ≤ d → d ≤ 10 → 1 ≤ i → i ≤ 10 → 1 ≤ r → r ≤ 10 → degT ≤ 100 →
    90 ≤ titanCentis d i r degT ∧ titanCentis d i r degT ≤ 1000) ∧
  (∀ imp tr : Nat, 1 ≤ imp → imp ≤ 10 → 1 ≤ tr → tr ≤ 10 →
    1 ≤ leverageTenths imp tr ∧ leverageTenths imp tr ≤ 100)

def M2_QuadrantAndEraInvariants : Prop :=
  (∀ imp tr : Nat, classifyQuadrant imp tr = .Q1 ↔ imp ≥ 8 ∧ tr ≥ 7) ∧
  (∀ imp tr : Nat, classifyQuadrant imp tr = .Q2 ↔ imp ≥ 8 ∧ tr < 7) ∧
  (∀ imp tr : Nat, classifyQuadrant imp tr = .Q3 ↔ imp < 8 ∧ tr ≥ 7) ∧
  (∀ imp tr : Nat, classifyQuadrant imp tr = .Q4 ↔ imp < 8 ∧ tr < 7) ∧
  (∀ imp tr : Nat, classifyQuadrant imp tr = .Q1 → 56 ≤ leverageTenths imp tr) ∧
  (∀ y₁ y₂ : Int, y₁ ≤ y₂ → eraRank (computeEra y₁) ≤ eraRank (computeEra y₂))

def M3_TaxonomyInvariants : Prop :=
  allPillars.length = 8 ∧
  allSuperdomains.length = 28 ∧
  allPillars.map (fun p => (superdomainsIn p).length) = [5, 3, 3, 3, 3, 4, 4, 3] ∧
  (∀ s : Superdomain, s ∈ allSuperdomains) ∧
  (∀ p : MacroPillar, p ∈ allPillars) ∧
  (∀ p : MacroPillar, ∃ s : Superdomain, pillarOf s = p) ∧
  (∀ s₁ s₂ : Superdomain, pillarOf s₁ ≠ pillarOf s₂ → s₁ ≠ s₂)

def M4_GraphAndDedupInvariants : Prop :=
  (∀ (V : Type) [DecidableEq V] (vs : List V) (_ : vs.Nodup) (es : List (Edge V)),
    (∀ e ∈ es, e.u ∈ vs ∧ e.v ∈ vs) →
    sumNat (vs.map (fun x => degreeOf x es)) = 2 * es.length) ∧
  (∀ (V : Type) (sd : V → Superdomain) (es : List (Edge V)),
    crossPillarCount sd es ≤ crossSuperdomainCount sd es ∧
    crossSuperdomainCount sd es ≤ es.length) ∧
  (∀ (α β : Type) [DecidableEq β] (key : α → β) (seen : List β) (xs : List α),
    (dedupBy key seen xs).length ≤ xs.length)

def M5_AutoResearchRatchetInvariants : Prop :=
  (25 + 25 + 20 + 15 + 15 = 100) ∧
  (∀ s r p g f : Nat, s ≤ 100 → r ≤ 100 → p ≤ 100 → g ≤ 100 → f ≤ 100 → aqsBps s r p g f ≤ 10000) ∧
  (∀ bestScore candScore : Nat, shouldKeep false bestScore candScore = false) ∧
  (∀ gates bestScore candScore, shouldKeep gates bestScore candScore = true ↔ gates = true ∧ bestScore < candScore) ∧
  (∀ gates bestScore candScore, bestScore ≤ updateBest gates bestScore candScore) ∧
  (∀ a : Int, metricDelta a a = 0) ∧
  (∀ a b : Int, metricDelta a b = - metricDelta b a)

def M6_LayerGradientMarginInvariants : Prop :=
  allSubstrates.length = 8 ∧
  allLayers.length = 7 ∧
  (∀ s : SubstrateClass, s ∈ allSubstrates) ∧
  (∀ l : AbstractionLayer, layerIndex l ≤ 6) ∧
  (∀ d t : Int, 1 ≤ d → d ≤ 10 → 1 ≤ t → t ≤ 10 →
    -9 ≤ hardnessTractGradient d t ∧ hardnessTractGradient d t ≤ 9) ∧
  (∀ c t : Int, 0 ≤ c → c ≤ 10000 → 0 ≤ t → t ≤ 1000 →
    -10000 ≤ cssTitanMarginBps c t ∧ cssTitanMarginBps c t ≤ 10000) ∧
  (∀ cp deg : Nat, cp ≤ deg → bridgeMarginBps cp deg ≤ 10000) ∧
  (∀ adj crossSD bps : Nat, classifyMarginRole adj crossSD bps = .apexKeystone ↔ adj ≥ 3)

def M7_NonVacuityCertificate : Prop :=
  (cssBps 100 100 55 40 = 8700 ∧ ageScoreCentis 299 < 10000) ∧
  (classifyQuadrant 8 7 = .Q1 ∧ classifyQuadrant 8 6 = .Q2 ∧
   classifyQuadrant 7 7 = .Q3 ∧ classifyQuadrant 7 6 = .Q4) ∧
  (computeEra (-500) = .antiquity ∧ computeEra 2000 = .twentyFirstC) ∧
  (sumNat (sampleVertices.map (fun x => degreeOf x sampleEdges)) = 2 * sampleEdges.length ∧
   crossPillarCount sampleSuperdomain sampleEdges = 2) ∧
  (shouldKeep true 8026 8026 = false ∧ shouldKeep true 8026 8193 = true ∧
   shouldKeep true 9559 9799 = true ∧ shouldKeep false 9799 10000 = false) ∧
  (classifyMarginRole 3 5 4000 = .apexKeystone ∧
   classifyMarginRole 2 3 3000 = .transPillarMargin ∧
   classifyMarginRole 2 3 2999 = .intraPillarBridge ∧
   classifyMarginRole 0 0 0 = .coreSpecialist)

def M8_AdversarialRefutations : Prop :=
  (¬ (∀ d c a t : Nat, d ≤ 100 → c ≤ 100 → a ≤ 100 → cssBps d c a t < 10000)) ∧
  (¬ (∀ age : Nat, 299 ≤ age → ageScoreCentis age = 10000)) ∧
  (¬ (∀ d i r degT : Nat, 1 ≤ d → d ≤ 10 → 1 ≤ i → i ≤ 10 → 1 ≤ r → r ≤ 10 → degT ≤ 100 →
      titanCentis d i r degT < 1000)) ∧
  (¬ (∀ imp tr : Nat, classifyQuadrant imp tr = .Q1 → 57 ≤ leverageTenths imp tr)) ∧
  (¬ (∀ imp tr : Nat, classifyQuadrant imp tr = .Q2 → 56 ≤ leverageTenths imp tr)) ∧
  (¬ (allSuperdomains.length = 27)) ∧
  (¬ (∀ (vs : List Nat), vs.Nodup → ∀ (es : List (Edge Nat)),
      (∀ e ∈ es, e.u ∈ vs ∧ e.v ∈ vs) →
      sumNat (vs.map (fun x => degreeOf x es)) = 3 * es.length)) ∧
  (¬ (∃ best cand : Nat, shouldKeep false best cand = true)) ∧
  (¬ (∀ adj crossSD bps : Nat, adj ≥ 2 → classifyMarginRole adj crossSD bps = .apexKeystone)) ∧
  (¬ (∀ adj crossSD bps : Nat, adj ≥ 1 → bps ≥ 2999 → classifyMarginRole adj crossSD bps = .transPillarMargin))

def AllMegaAtlasInvariants : Prop :=
  M1_ScoringInvariants ∧
  M2_QuadrantAndEraInvariants ∧
  M3_TaxonomyInvariants ∧
  M4_GraphAndDedupInvariants ∧
  M5_AutoResearchRatchetInvariants ∧
  M6_LayerGradientMarginInvariants ∧
  M7_NonVacuityCertificate ∧
  M8_AdversarialRefutations

end

end MegaAtlasProofs.Challenge
