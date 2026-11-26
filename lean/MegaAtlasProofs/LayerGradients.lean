module
-- SPDX-License-Identifier: Apache-2.0
-- Copyright (c) 2026 Alexander Stephen Donahue

public import MegaAtlasProofs.Scoring

/-
  MegaAtlasProofs/LayerGradients.lean
  Pure Lean 4.35.0 (zero Mathlib, zero sorry) formal invariants for the
  Multi-Layer Substrate, Spectrum, Gradient, Margin & Adjacent Framework:
    1. 8-Substrate & 7-Abstraction-Layer (`L0..L6`) totality & ordinal bounds
    2. Hardness-Tractability Gradient (`d - t in [-9, 9]`): exact bounds,
       monotonicity in difficulty, anti-monotonicity in tractability, zero iff equal
    3. CSS-vs-Titan Signed Margin (`cssBps - 10 * titanCentis in [-10000, 10000]`)
    4. Trans-Pillar Bridge Margin Ratio (`crossPillar <= deg -> ratioBps <= 10000`)
    5. Adjacent Pillars Bound (`adjPillars <= 7` strictly < 8 total Macro-Pillars)
    6. Margin Role 4-Class Partition exhaustiveness & mutual exclusivity

  Author: Alexander Stephen Donahue (Independent Researcher, ORCID 0009-0006-8168-9648)
-/

namespace MegaAtlasProofs.LayerGradients

open MegaAtlasProofs.Scoring

@[expose] public section

/-- Eight canonical substrates spanning formal, quantum, material, biological, synthetic & cosmic reality. -/
inductive SubstrateClass where
  | abstractFormal
  | quantumField
  | condensedSolid
  | fluidPlasma
  | molecularChemical
  | biologicalNeural
  | siliconCyberAI
  | planetaryCosmicSocial
  deriving DecidableEq, Repr

/-- Seven-layer abstraction hierarchy (`L0` axiomatic bedrock -> `L6` normative/semantic layer). -/
inductive AbstractionLayer where
  | L0_FormalAxiomatic
  | L1_QuantumSpacetime
  | L2_AtomicMaterialContinuum
  | L3_LivingEcologicalNeural
  | L4_ComputationalAICyber
  | L5_EngineeredPlanetaryCosmic
  | L6_NormativeEconomicSemantic
  deriving DecidableEq, Repr

def allSubstrates : List SubstrateClass :=
  [ .abstractFormal, .quantumField, .condensedSolid, .fluidPlasma,
    .molecularChemical, .biologicalNeural, .siliconCyberAI, .planetaryCosmicSocial ]

def allLayers : List AbstractionLayer :=
  [ .L0_FormalAxiomatic, .L1_QuantumSpacetime, .L2_AtomicMaterialContinuum,
    .L3_LivingEcologicalNeural, .L4_ComputationalAICyber,
    .L5_EngineeredPlanetaryCosmic, .L6_NormativeEconomicSemantic ]

def layerIndex : AbstractionLayer → Nat
  | .L0_FormalAxiomatic          => 0
  | .L1_QuantumSpacetime         => 1
  | .L2_AtomicMaterialContinuum  => 2
  | .L3_LivingEcologicalNeural   => 3
  | .L4_ComputationalAICyber     => 4
  | .L5_EngineeredPlanetaryCosmic => 5
  | .L6_NormativeEconomicSemantic => 6

/-- Signed Hardness-Tractability Gradient (`difficulty - tractability_2050`). -/
def hardnessTractGradient (diff tract : Int) : Int :=
  diff - tract

/-- Signed CSS-vs-Titan Margin in integer basis points (`cssBps - 10 * titanCentis`). -/
def cssTitanMarginBps (cssBpsVal titanCentisVal : Int) : Int :=
  cssBpsVal - 10 * titanCentisVal

/-- Trans-Pillar Bridge Margin Ratio in basis points (`(crossPillar * 10000) / degree`). -/
def bridgeMarginBps (crossPillar deg : Nat) : Nat :=
  if deg = 0 then 0 else (crossPillar * 10000) / deg

/-- Four-class structural margin role matching `classify_margin_role` in `src/v2_loader.py`. -/
inductive MarginRole where
  | apexKeystone      -- adjacent_pillars >= 3
  | transPillarMargin -- adjacent_pillars >= 1 (and < 3) and bridgeRatio >= 30%
  | intraPillarBridge -- cross_superdomain >= 1 (or adjacent_pillars in {1,2} with low ratio)
  | coreSpecialist    -- purely intra-superdomain
  deriving DecidableEq, Repr

def classifyMarginRole (adjPillars crossSD bridgeBps : Nat) : MarginRole :=
  if adjPillars ≥ 3 then .apexKeystone
  else if adjPillars ≥ 1 ∧ bridgeBps ≥ 3000 then .transPillarMargin
  else if crossSD ≥ 1 ∨ adjPillars ≥ 1 then .intraPillarBridge
  else .coreSpecialist

-- ==================== 1. SUBSTRATE & LAYER INVARIANTS ====================

theorem substrate_count_eq_8 : allSubstrates.length = 8 := by
  rfl

theorem layer_count_eq_7 : allLayers.length = 7 := by
  rfl

theorem allSubstrates_complete (s : SubstrateClass) : s ∈ allSubstrates := by
  cases s <;> simp [allSubstrates]

theorem layerIndex_le_6 (l : AbstractionLayer) : layerIndex l ≤ 6 := by
  cases l <;> simp [layerIndex]

-- ==================== 2. GRADIENT & MARGIN INVARIANTS ====================

theorem hardnessTractGradient_bounds {d t : Int}
    (hd1 : 1 ≤ d) (hd2 : d ≤ 10) (ht1 : 1 ≤ t) (ht2 : t ≤ 10) :
    -9 ≤ hardnessTractGradient d t ∧ hardnessTractGradient d t ≤ 9 := by
  unfold hardnessTractGradient
  constructor <;> omega

theorem hardnessTractGradient_zero_iff (d t : Int) :
    hardnessTractGradient d t = 0 ↔ d = t := by
  unfold hardnessTractGradient
  constructor <;> intro h <;> omega

theorem hardnessTractGradient_mono_diff {d₁ d₂ t : Int} (h : d₁ ≤ d₂) :
    hardnessTractGradient d₁ t ≤ hardnessTractGradient d₂ t := by
  unfold hardnessTractGradient
  omega

theorem hardnessTractGradient_anti_tract {d t₁ t₂ : Int} (h : t₁ ≤ t₂) :
    hardnessTractGradient d t₂ ≤ hardnessTractGradient d t₁ := by
  unfold hardnessTractGradient
  omega

theorem cssTitanMarginBps_bounds {c t : Int}
    (hc1 : 0 ≤ c) (hc2 : c ≤ 10000) (ht1 : 0 ≤ t) (ht2 : t ≤ 1000) :
    -10000 ≤ cssTitanMarginBps c t ∧ cssTitanMarginBps c t ≤ 10000 := by
  unfold cssTitanMarginBps
  constructor <;> omega

-- ==================== 3. BRIDGE RATIO, ADJACENT PILLARS & MARGIN ROLE ====================

theorem bridgeMarginBps_le_10000 {cp deg : Nat} (h : cp ≤ deg) :
    bridgeMarginBps cp deg ≤ 10000 := by
  unfold bridgeMarginBps
  split
  · exact Nat.zero_le 10000
  · rename_i hne
    have hpos : 0 < deg := Nat.pos_of_ne_zero hne
    have hmul : cp * 10000 ≤ deg * 10000 := Nat.mul_le_mul_right 10000 h
    have hdiv : (cp * 10000) / deg ≤ (deg * 10000) / deg := Nat.div_le_div_right hmul
    rw [Nat.mul_div_cancel_left 10000 hpos] at hdiv
    exact hdiv

theorem bridgeMarginBps_zero_when_no_cross (deg : Nat) :
    bridgeMarginBps 0 deg = 0 := by
  unfold bridgeMarginBps
  split <;> simp

/-- Since there are 8 Macro-Pillars and a problem cannot be adjacent to its own pillar,
    distinct adjacent pillars is strictly bounded above by 7. -/
theorem adjacent_pillars_lt_8 {adj : Nat} (h : adj ≤ 7) : adj < 8 := by
  omega

theorem marginRole_exhaustive (adj crossSD bps : Nat) :
    classifyMarginRole adj crossSD bps = .apexKeystone ∨
    classifyMarginRole adj crossSD bps = .transPillarMargin ∨
    classifyMarginRole adj crossSD bps = .intraPillarBridge ∨
    classifyMarginRole adj crossSD bps = .coreSpecialist := by
  cases h : classifyMarginRole adj crossSD bps <;> simp

theorem apexKeystone_requires_3_adjacent (adj crossSD bps : Nat) :
    classifyMarginRole adj crossSD bps = .apexKeystone ↔ adj ≥ 3 := by
  unfold classifyMarginRole
  split
  · rename_i h; simp [h]
  · rename_i h
    split
    · simp [h]
    · split <;> simp [h]

end

end MegaAtlasProofs.LayerGradients
