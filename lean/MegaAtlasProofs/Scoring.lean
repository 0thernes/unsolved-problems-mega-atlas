module
-- SPDX-License-Identifier: Apache-2.0
-- Copyright (c) 2026 Alexander Stephen Donahue
/-
  MegaAtlasProofs/Scoring.lean
  Pure Lean 4.35.0 (zero Mathlib, zero sorry) formal invariants for the
  Mega-Atlas scoring functions:
    1. 0thernes Composite Severity Score (CSS, basis points in [0, 10000])
    2. Antiquity Age Saturation Function (300-year cap)
    3. Composite Titan Index (centi-units in [90, 1000])
    4. Near-Term Leverage Score (tenths in [1, 100])

  Author: Alexander Stephen Donahue (Independent Researcher, ORCID 0009-0006-8168-9648)
-/

namespace MegaAtlasProofs.Scoring

@[expose] public section

/-- Antiquity-capped age score in centi-points (0..10000 representing 0.00..100.00).
    Matches `min(100.0, max(0.0, age_years / 3.0))` in Python `v2_loader.py`
    and `0thernes/unsolved-mathematics/docs/methodology/RANKING.md`. -/
def ageScoreCentis (ageYears : Nat) : Nat :=
  min 10000 ((ageYears * 100) / 3)

/-- 0thernes Composite Severity Score (CSS) in integer basis points (0..10000 = 0.00..100.00).
    Inputs `diff100`, `cent100`, `age100`, `tract100` live in `[0, 100]`:
      `CSS = 0.40 * diff + 0.30 * centrality + 0.20 * age + 0.10 * (100 - tractability)` -/
def cssBps (diff100 cent100 age100 tract100 : Nat) : Nat :=
  40 * diff100 + 30 * cent100 + 20 * age100 + 10 * (100 - tract100)

/-- Composite Titan Index in integer centi-units (90..1000 = 0.90..10.00).
    Inputs `diff`, `impact`, `interdisc` in `[1, 10]` and `degTermTenths` in `[0, 100]`
    representing `min(10.0, 2.5 * ln(1 + deg)) * 10`:
      `Titan = 0.35 * diff + 0.35 * impact + 0.20 * interdisc + 0.10 * degTerm` -/
def titanCentis (diff impact interdisc degTermTenths : Nat) : Nat :=
  35 * diff + 35 * impact + 20 * interdisc + degTermTenths

/-- Near-Term Leverage Score in integer tenths (`(impact * tract) / 10` * 10 = `impact * tract`). -/
def leverageTenths (impact tract : Nat) : Nat :=
  impact * tract

-- ==================== 1. AGE SATURATION INVARIANTS ====================

theorem ageScoreCentis_le_cap (ageYears : Nat) :
    ageScoreCentis ageYears ≤ 10000 := by
  unfold ageScoreCentis
  exact Nat.min_le_left 10000 ((ageYears * 100) / 3)

theorem ageScoreCentis_zero :
    ageScoreCentis 0 = 0 := by
  rfl

theorem ageScoreCentis_saturates_at_300 (ageYears : Nat) (h : 300 ≤ ageYears) :
    ageScoreCentis ageYears = 10000 := by
  unfold ageScoreCentis
  have hge : 10000 ≤ (ageYears * 100) / 3 := by omega
  omega

theorem ageScoreCentis_mono {a₁ a₂ : Nat} (h : a₁ ≤ a₂) :
    ageScoreCentis a₁ ≤ ageScoreCentis a₂ := by
  unfold ageScoreCentis
  have hdiv : (a₁ * 100) / 3 ≤ (a₂ * 100) / 3 := by omega
  omega

-- ==================== 2. CSS INVARIANTS ====================

theorem css_weights_sum : 40 + 30 + 20 + 10 = 100 := by
  rfl

theorem cssBps_le_max {d c a t : Nat}
    (hd : d ≤ 100) (hc : c ≤ 100) (ha : a ≤ 100) :
    cssBps d c a t ≤ 10000 := by
  unfold cssBps
  omega

theorem cssBps_ge_valid_min {d c a t : Nat}
    (hd : 10 ≤ d) (hc : 5 ≤ c) :
    550 ≤ cssBps d c a t := by
  unfold cssBps
  omega

theorem cssBps_mono_diff {d₁ d₂ c a t : Nat} (h : d₁ ≤ d₂) :
    cssBps d₁ c a t ≤ cssBps d₂ c a t := by
  unfold cssBps
  omega

theorem cssBps_mono_cent {d c₁ c₂ a t : Nat} (h : c₁ ≤ c₂) :
    cssBps d c₁ a t ≤ cssBps d c₂ a t := by
  unfold cssBps
  omega

theorem cssBps_mono_age {d c a₁ a₂ t : Nat} (h : a₁ ≤ a₂) :
    cssBps d c a₁ t ≤ cssBps d c a₂ t := by
  unfold cssBps
  omega

theorem cssBps_anti_tract {d c a t₁ t₂ : Nat} (h : t₁ ≤ t₂) :
    cssBps d c a t₂ ≤ cssBps d c a t₁ := by
  unfold cssBps
  omega

theorem cssBps_extreme_max : cssBps 100 100 100 0 = 10000 := by
  rfl

theorem cssBps_extreme_min : cssBps 0 0 0 100 = 0 := by
  rfl

-- ==================== 3. TITAN INDEX INVARIANTS ====================

theorem titan_weights_sum : 35 + 35 + 20 + 10 = 100 := by
  rfl

theorem titanCentis_bounds {d i r degT : Nat}
    (hd1 : 1 ≤ d) (hd2 : d ≤ 10)
    (hi1 : 1 ≤ i) (hi2 : i ≤ 10)
    (hr1 : 1 ≤ r) (hr2 : r ≤ 10)
    (hdeg : degT ≤ 100) :
    90 ≤ titanCentis d i r degT ∧ titanCentis d i r degT ≤ 1000 := by
  unfold titanCentis
  constructor <;> omega

theorem titanCentis_mono_diff {d₁ d₂ i r degT : Nat} (h : d₁ ≤ d₂) :
    titanCentis d₁ i r degT ≤ titanCentis d₂ i r degT := by
  unfold titanCentis
  omega

theorem titanCentis_mono_impact {d i₁ i₂ r degT : Nat} (h : i₁ ≤ i₂) :
    titanCentis d i₁ r degT ≤ titanCentis d i₂ r degT := by
  unfold titanCentis
  omega

theorem titanCentis_mono_interdisc {d i r₁ r₂ degT : Nat} (h : r₁ ≤ r₂) :
    titanCentis d i r₁ degT ≤ titanCentis d i r₂ degT := by
  unfold titanCentis
  omega

theorem titanCentis_mono_deg {d i r deg₁ deg₂ : Nat} (h : deg₁ ≤ deg₂) :
    titanCentis d i r deg₁ ≤ titanCentis d i r deg₂ := by
  unfold titanCentis
  omega

-- ==================== 4. NEAR-TERM LEVERAGE INVARIANTS ====================

theorem leverageTenths_bounds {imp tr : Nat}
    (hi1 : 1 ≤ imp) (hi2 : imp ≤ 10)
    (ht1 : 1 ≤ tr) (ht2 : tr ≤ 10) :
    1 ≤ leverageTenths imp tr ∧ leverageTenths imp tr ≤ 100 := by
  unfold leverageTenths
  constructor
  · exact Nat.mul_pos hi1 ht1
  · exact Nat.mul_le_mul hi2 ht2

theorem leverageTenths_comm (imp tr : Nat) :
    leverageTenths imp tr = leverageTenths tr imp := by
  unfold leverageTenths
  exact Nat.mul_comm imp tr

theorem leverageTenths_mono {i₁ i₂ t₁ t₂ : Nat} (hi : i₁ ≤ i₂) (ht : t₁ ≤ t₂) :
    leverageTenths i₁ t₁ ≤ leverageTenths i₂ t₂ := by
  unfold leverageTenths
  exact Nat.mul_le_mul hi ht

end

end MegaAtlasProofs.Scoring
