module
-- SPDX-License-Identifier: Apache-2.0
-- Copyright (c) 2026 Alexander Stephen Donahue
/-
  MegaAtlasProofs/Taxonomy.lean
  Pure Lean 4.35.0 (zero Mathlib, zero sorry) formal invariants for the
  8-Macro-Pillar x 28-Superdomain hierarchical taxonomy matching `src/v2_schema.py`:
    - Exact cardinalities (8 Macro-Pillars, 28 Superdomains)
    - Surjectivity of `pillarOf : Superdomain -> MacroPillar`
    - Exact partition sum: 5 + 3 + 3 + 3 + 3 + 4 + 4 + 3 = 28
    - Cross-pillar separation strictly implies cross-superdomain separation

  Author: Alexander Stephen Donahue (Independent Researcher, ORCID 0009-0006-8168-9648)
-/

namespace MegaAtlasProofs.Taxonomy

@[expose] public section

inductive MacroPillar where
  | pureMath
  | logicStatsCS
  | physicsCosmos
  | matterChem
  | lifeMindMed
  | aiQuantumHWSys
  | engDesignEarthEnergy
  | philSocialHum
  deriving DecidableEq, Repr

inductive Superdomain where
  -- 1. Pure Mathematics (5)
  | numberTheory
  | algebraGroupsCat
  | geomTopo
  | analysisPDEsDyn
  | combinatoricsGraphs
  -- 2. Logic, Statistics & Computing (3)
  | mathLogicSetComp
  | probStochStats
  | csComplexityCrypto
  -- 3. Fundamental Physics & Cosmos (3)
  | qmQftParticles
  | spacetimeGravityHolo
  | astroCosmoSeti
  -- 4. Matter, Materials & Chemistry (3)
  | condensedMatter
  | fluidsGasesPlasmas
  | chemistryCatalysis
  -- 5. Life, Mind & Medicine (3)
  | biologyEvolution
  | neuroConsciousness
  | medicineLongevity
  -- 6. AI, Quantum Tech, Hardware & Systems (4)
  | aiMlSimulations
  | quantumComputing
  | electronicsPhotonics
  | systemsControlRobotics
  -- 7. Engineering, Design, Earth & Energy (4)
  | mechAeroStructCivil
  | archUrbanErgonomics
  | geologyEarthClimate
  | energyFoodSustain
  -- 8. Philosophy, Social & Humanities (3)
  | philMetaEthics
  | econGameSocial
  | lingArchHistoryLaw
  deriving DecidableEq, Repr

def pillarOf : Superdomain → MacroPillar
  | .numberTheory | .algebraGroupsCat | .geomTopo | .analysisPDEsDyn | .combinatoricsGraphs =>
      .pureMath
  | .mathLogicSetComp | .probStochStats | .csComplexityCrypto =>
      .logicStatsCS
  | .qmQftParticles | .spacetimeGravityHolo | .astroCosmoSeti =>
      .physicsCosmos
  | .condensedMatter | .fluidsGasesPlasmas | .chemistryCatalysis =>
      .matterChem
  | .biologyEvolution | .neuroConsciousness | .medicineLongevity =>
      .lifeMindMed
  | .aiMlSimulations | .quantumComputing | .electronicsPhotonics | .systemsControlRobotics =>
      .aiQuantumHWSys
  | .mechAeroStructCivil | .archUrbanErgonomics | .geologyEarthClimate | .energyFoodSustain =>
      .engDesignEarthEnergy
  | .philMetaEthics | .econGameSocial | .lingArchHistoryLaw =>
      .philSocialHum

def allPillars : List MacroPillar :=
  [ .pureMath, .logicStatsCS, .physicsCosmos, .matterChem,
    .lifeMindMed, .aiQuantumHWSys, .engDesignEarthEnergy, .philSocialHum ]

def allSuperdomains : List Superdomain :=
  [ .numberTheory, .algebraGroupsCat, .geomTopo, .analysisPDEsDyn, .combinatoricsGraphs,
    .mathLogicSetComp, .probStochStats, .csComplexityCrypto,
    .qmQftParticles, .spacetimeGravityHolo, .astroCosmoSeti,
    .condensedMatter, .fluidsGasesPlasmas, .chemistryCatalysis,
    .biologyEvolution, .neuroConsciousness, .medicineLongevity,
    .aiMlSimulations, .quantumComputing, .electronicsPhotonics, .systemsControlRobotics,
    .mechAeroStructCivil, .archUrbanErgonomics, .geologyEarthClimate, .energyFoodSustain,
    .philMetaEthics, .econGameSocial, .lingArchHistoryLaw ]

def superdomainsIn (p : MacroPillar) : List Superdomain :=
  allSuperdomains.filter (fun s => pillarOf s == p)

theorem pillar_count_eq_8 : allPillars.length = 8 := by
  rfl

theorem superdomain_count_eq_28 : allSuperdomains.length = 28 := by
  rfl

theorem pillar_partition_sizes :
    allPillars.map (fun p => (superdomainsIn p).length) = [5, 3, 3, 3, 3, 4, 4, 3] := by
  rfl

theorem pillar_partition_sum_28 :
    (allPillars.map (fun p => (superdomainsIn p).length)).foldl (· + ·) 0 = 28 := by
  rfl

theorem allSuperdomains_complete (s : Superdomain) : s ∈ allSuperdomains := by
  cases s <;> simp [allSuperdomains]

theorem allPillars_complete (p : MacroPillar) : p ∈ allPillars := by
  cases p <;> simp [allPillars]

theorem pillarOf_surjective (p : MacroPillar) : ∃ s : Superdomain, pillarOf s = p := by
  cases p with
  | pureMath => exact ⟨.numberTheory, rfl⟩
  | logicStatsCS => exact ⟨.mathLogicSetComp, rfl⟩
  | physicsCosmos => exact ⟨.qmQftParticles, rfl⟩
  | matterChem => exact ⟨.condensedMatter, rfl⟩
  | lifeMindMed => exact ⟨.biologyEvolution, rfl⟩
  | aiQuantumHWSys => exact ⟨.aiMlSimulations, rfl⟩
  | engDesignEarthEnergy => exact ⟨.mechAeroStructCivil, rfl⟩
  | philSocialHum => exact ⟨.philMetaEthics, rfl⟩

/-- Any cross-pillar edge is necessarily a cross-superdomain edge. -/
theorem cross_pillar_implies_cross_superdomain (s₁ s₂ : Superdomain)
    (h : pillarOf s₁ ≠ pillarOf s₂) : s₁ ≠ s₂ := by
  intro heq
  subst heq
  exact h rfl

end

end MegaAtlasProofs.Taxonomy
