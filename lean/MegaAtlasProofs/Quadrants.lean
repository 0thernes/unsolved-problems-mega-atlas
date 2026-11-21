/-
  MegaAtlasProofs/Quadrants.lean
  Pure Lean 4.35.0 (zero Mathlib, zero sorry) formal invariants for:
    1. Strategic 4-Quadrant Classifier (exhaustiveness, mutual exclusivity,
       boundary monotonicity, and Q1 minimum leverage bound >= 5.6)
    2. Historical Era Classifier (totality and exact year-order monotonicity)

  Author: Alexander Stephen Donahue (0thernes LLC, ORCID 0009-0006-8168-9648)
-/

import MegaAtlasProofs.Scoring

namespace MegaAtlasProofs.Quadrants

/-- The four strategic quadrants matching `classify_quadrant` in `src/v2_loader.py`. -/
inductive Quadrant where
  | Q1 -- Near-Term Civilizational Levers (impact >= 8, tract >= 7)
  | Q2 -- Grand Centuries-Scale Titans (impact >= 8, tract < 7)
  | Q3 -- Targeted Technical Frontiers (impact < 8, tract >= 7)
  | Q4 -- Deep Foundational & Formal Enigmas (impact < 8, tract < 7)
  deriving DecidableEq, Repr

/-- Exact quadrant classification matching `src/v2_loader.py`. -/
def classifyQuadrant (impact tract : Nat) : Quadrant :=
  if impact ≥ 8 then
    if tract ≥ 7 then .Q1 else .Q2
  else
    if tract ≥ 7 then .Q3 else .Q4

def isHighImpact : Quadrant → Bool
  | .Q1 | .Q2 => true
  | .Q3 | .Q4 => false

def isHighTract : Quadrant → Bool
  | .Q1 | .Q3 => true
  | .Q2 | .Q4 => false

theorem classify_eq_Q1_iff (imp tr : Nat) :
    classifyQuadrant imp tr = .Q1 ↔ imp ≥ 8 ∧ tr ≥ 7 := by
  unfold classifyQuadrant
  by_cases hi : imp ≥ 8 <;> by_cases ht : tr ≥ 7 <;> simp [hi, ht]

theorem classify_eq_Q2_iff (imp tr : Nat) :
    classifyQuadrant imp tr = .Q2 ↔ imp ≥ 8 ∧ tr < 7 := by
  unfold classifyQuadrant
  by_cases hi : imp ≥ 8 <;> by_cases ht : tr ≥ 7 <;> simp [hi, ht] <;> omega

theorem classify_eq_Q3_iff (imp tr : Nat) :
    classifyQuadrant imp tr = .Q3 ↔ imp < 8 ∧ tr ≥ 7 := by
  unfold classifyQuadrant
  by_cases hi : imp ≥ 8 <;> by_cases ht : tr ≥ 7 <;> simp [hi, ht] <;> omega

theorem classify_eq_Q4_iff (imp tr : Nat) :
    classifyQuadrant imp tr = .Q4 ↔ imp < 8 ∧ tr < 7 := by
  unfold classifyQuadrant
  by_cases hi : imp ≥ 8
  · by_cases ht : tr ≥ 7
    · simp only [hi, ht, ↓reduceIte, reduceCtorEq, false_iff, not_and]
      intro hlt; omega
    · simp only [hi, ht, ↓reduceIte, reduceCtorEq, false_iff, not_and]
      intro hlt; omega
  · by_cases ht : tr ≥ 7
    · simp only [hi, ht, ↓reduceIte, reduceCtorEq, false_iff, not_and]
      intro _ htr; omega
    · simp only [hi, ht, ↓reduceIte, true_iff]
      constructor <;> omega

theorem classify_exhaustive (imp tr : Nat) :
    classifyQuadrant imp tr = .Q1 ∨
    classifyQuadrant imp tr = .Q2 ∨
    classifyQuadrant imp tr = .Q3 ∨
    classifyQuadrant imp tr = .Q4 := by
  cases h : classifyQuadrant imp tr <;> simp

theorem highImpact_preserved {i₁ i₂ tr : Nat}
    (h : isHighImpact (classifyQuadrant i₁ tr) = true) (hle : i₁ ≤ i₂) :
    isHighImpact (classifyQuadrant i₂ tr) = true := by
  unfold classifyQuadrant isHighImpact at *
  by_cases h1 : i₁ ≥ 8
  · have h2 : i₂ ≥ 8 := by omega
    by_cases ht : tr ≥ 7 <;> simp [h1, h2, ht] at h ⊢
  · by_cases ht : tr ≥ 7 <;> simp [h1, ht] at h

theorem highTract_preserved {imp t₁ t₂ : Nat}
    (h : isHighTract (classifyQuadrant imp t₁) = true) (hle : t₁ ≤ t₂) :
    isHighTract (classifyQuadrant imp t₂) = true := by
  unfold classifyQuadrant isHighTract at *
  by_cases ht1 : t₁ ≥ 7
  · have ht2 : t₂ ≥ 7 := by omega
    by_cases hi : imp ≥ 8 <;> simp [hi, ht1, ht2] at h ⊢
  · by_cases hi : imp ≥ 8 <;> simp [hi, ht1] at h

/-- Every Q1 Near-Term Civilizational Lever has Near-Term Leverage >= 5.6 (56 tenths). -/
theorem Q1_leverage_ge_56 {imp tr : Nat} (h : classifyQuadrant imp tr = .Q1) :
    56 ≤ MegaAtlasProofs.Scoring.leverageTenths imp tr := by
  have ⟨hi, ht⟩ := (classify_eq_Q1_iff imp tr).mp h
  unfold MegaAtlasProofs.Scoring.leverageTenths
  exact Nat.mul_le_mul hi ht

-- ==================== HISTORICAL ERA CLASSIFIER ====================

/-- The 6 historical eras matching `compute_era` in `src/v2_schema.py`. -/
inductive Era where
  | antiquity     -- year < 500
  | earlyModern   -- 500 <= year < 1800
  | nineteenthC   -- 1800 <= year < 1900
  | earlyMid20thC -- 1900 <= year < 1970
  | late20thC     -- 1970 <= year < 2000
  | twentyFirstC  -- year >= 2000
  deriving DecidableEq, Repr

def computeEra (year : Int) : Era :=
  if year < 500 then .antiquity
  else if year < 1800 then .earlyModern
  else if year < 1900 then .nineteenthC
  else if year < 1970 then .earlyMid20thC
  else if year < 2000 then .late20thC
  else .twentyFirstC

def eraRank : Era → Nat
  | .antiquity     => 0
  | .earlyModern   => 1
  | .nineteenthC   => 2
  | .earlyMid20thC => 3
  | .late20thC     => 4
  | .twentyFirstC  => 5

theorem computeEra_mono {y₁ y₂ : Int} (h : y₁ ≤ y₂) :
    eraRank (computeEra y₁) ≤ eraRank (computeEra y₂) := by
  unfold computeEra
  repeat (first | split | simp [eraRank] | omega)

theorem computeEra_ancient_sample : computeEra (-500) = .antiquity := by
  rfl

theorem computeEra_nov2026_sample : computeEra 2026 = .twentyFirstC := by
  rfl

end MegaAtlasProofs.Quadrants
