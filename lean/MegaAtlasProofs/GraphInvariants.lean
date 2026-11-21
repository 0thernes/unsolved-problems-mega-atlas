/-
  MegaAtlasProofs/GraphInvariants.lean
  Pure Lean 4.35.0 (zero Mathlib, zero sorry) formal invariants for the
  Mega-Atlas undirected cross-domain knowledge graph & deduplication pipeline:
    1. Finite Undirected Handshaking Lemma: sum_{v in V} deg(v) = 2 * |E|
    2. Exact Cross-Partition Hierarchy: cross_pillar_edges <= cross_superdomain_edges <= |E|
    3. Deduplication Cardinality Bound: |dedup(xs)| <= |xs|

  Author: Alexander Stephen Donahue (0thernes LLC, ORCID 0009-0006-8168-9648)
-/

import MegaAtlasProofs.Taxonomy

namespace MegaAtlasProofs.GraphInvariants

open MegaAtlasProofs.Taxonomy

/-- An undirected edge between two vertices `u` and `v`. -/
structure Edge (V : Type) where
  u : V
  v : V
  deriving DecidableEq, Repr

/-- Incidence contribution of one edge `e` to vertex `x`. -/
def edgeIncidence {V : Type} [DecidableEq V] (x : V) (e : Edge V) : Nat :=
  (if e.u = x then 1 else 0) + (if e.v = x then 1 else 0)

/-- Degree of vertex `x` over an edge list `es`. -/
def degreeOf {V : Type} [DecidableEq V] (x : V) : List (Edge V) → Nat
  | [] => 0
  | e :: es => edgeIncidence x e + degreeOf x es

/-- Sum of a list of natural numbers. -/
def sumNat : List Nat → Nat
  | [] => 0
  | n :: ns => n + sumNat ns

private theorem sumNat_map_add {α : Type} (xs : List α) (f g : α → Nat) :
    sumNat (xs.map (fun x => f x + g x)) = sumNat (xs.map f) + sumNat (xs.map g) := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
    simp only [List.map, sumNat, ih]
    omega

private theorem sumNat_indicator_not_mem {V : Type} [DecidableEq V]
    (y : V) (vs : List V) (hnot : y ∉ vs) :
    sumNat (vs.map (fun x => if y = x then 1 else 0)) = 0 := by
  induction vs with
  | nil => rfl
  | cons v vs ih =>
    have hne : y ≠ v := fun heq => hnot (by simp [heq])
    have hnot' : y ∉ vs := fun hmem => hnot (by simp [hmem])
    simp only [List.map, sumNat, hne, ↓reduceIte, ih hnot']

private theorem sumNat_indicator_nodup {V : Type} [DecidableEq V]
    (y : V) (vs : List V) (hnd : vs.Nodup) (hmem : y ∈ vs) :
    sumNat (vs.map (fun x => if y = x then 1 else 0)) = 1 := by
  induction vs with
  | nil => cases hmem
  | cons v vs ih =>
    have ⟨hvnot, hnd'⟩ := List.nodup_cons.mp hnd
    by_cases heq : y = v
    · subst heq
      have hrest := sumNat_indicator_not_mem y vs hvnot
      simp only [List.map, sumNat, ↓reduceIte, hrest]
    · have hmem' : y ∈ vs := by
        cases List.mem_cons.mp hmem with
        | inl h => exact absurd h heq
        | inr h => exact h
      simp only [List.map, sumNat, heq, ↓reduceIte, ih hnd' hmem', Nat.zero_add]

private theorem sumNat_zeros {V : Type} (vs : List V) :
    sumNat (vs.map (fun _ => 0)) = 0 := by
  induction vs with
  | nil => rfl
  | cons _ xs ih => simp [List.map, sumNat, ih]

private theorem sumNat_edgeIncidence {V : Type} [DecidableEq V]
    (vs : List V) (hnd : vs.Nodup) (e : Edge V) (hu : e.u ∈ vs) (hv : e.v ∈ vs) :
    sumNat (vs.map (fun x => edgeIncidence x e)) = 2 := by
  unfold edgeIncidence
  rw [sumNat_map_add]
  rw [sumNat_indicator_nodup e.u vs hnd hu]
  rw [sumNat_indicator_nodup e.v vs hnd hv]

/-- **Handshaking Lemma:** For any finite nodup vertex list `vs` containing all endpoints
    of an edge list `es`, the sum of vertex degrees equals `2 * es.length`. -/
theorem handshaking_lemma {V : Type} [DecidableEq V]
    (vs : List V) (hnd : vs.Nodup) (es : List (Edge V))
    (hclosed : ∀ e ∈ es, e.u ∈ vs ∧ e.v ∈ vs) :
    sumNat (vs.map (fun x => degreeOf x es)) = 2 * es.length := by
  induction es with
  | nil =>
    simpa [degreeOf] using sumNat_zeros vs
  | cons e es ih =>
    have ⟨hu, hv⟩ := hclosed e (List.mem_cons_self)
    have hclosed' : ∀ e' ∈ es, e'.u ∈ vs ∧ e'.v ∈ vs :=
      fun e' hm => hclosed e' (List.mem_cons_of_mem e hm)
    simp only [degreeOf]
    rw [sumNat_map_add]
    rw [sumNat_edgeIncidence vs hnd e hu hv]
    rw [ih hclosed']
    simp only [List.length_cons]
    omega

-- ==================== CROSS-PARTITION EDGE HIERARCHY ====================

def crossSuperdomainCount {V : Type} (sd : V → Superdomain) : List (Edge V) → Nat
  | [] => 0
  | e :: es => (if sd e.u ≠ sd e.v then 1 else 0) + crossSuperdomainCount sd es

def crossPillarCount {V : Type} (sd : V → Superdomain) : List (Edge V) → Nat
  | [] => 0
  | e :: es => (if pillarOf (sd e.u) ≠ pillarOf (sd e.v) then 1 else 0) + crossPillarCount sd es

/-- Cross-pillar bridge edges can never exceed cross-superdomain edges. -/
theorem cross_pillar_le_cross_superdomain {V : Type} (sd : V → Superdomain) (es : List (Edge V)) :
    crossPillarCount sd es ≤ crossSuperdomainCount sd es := by
  induction es with
  | nil => exact Nat.le_refl 0
  | cons e es ih =>
    unfold crossPillarCount crossSuperdomainCount
    split
    · rename_i hp
      have hs : sd e.u ≠ sd e.v := cross_pillar_implies_cross_superdomain (sd e.u) (sd e.v) hp
      split
      · omega
      · contradiction
    · split <;> omega

/-- Cross-superdomain edges can never exceed total edge count. -/
theorem cross_superdomain_le_total {V : Type} (sd : V → Superdomain) (es : List (Edge V)) :
    crossSuperdomainCount sd es ≤ es.length := by
  induction es with
  | nil => exact Nat.le_refl 0
  | cons e es ih =>
    unfold crossSuperdomainCount
    simp only [List.length_cons]
    split <;> omega

/-- Complete edge hierarchy: `cross_pillar <= cross_superdomain <= total_edges`. -/
theorem edge_hierarchy {V : Type} (sd : V → Superdomain) (es : List (Edge V)) :
    crossPillarCount sd es ≤ crossSuperdomainCount sd es ∧
    crossSuperdomainCount sd es ≤ es.length :=
  ⟨cross_pillar_le_cross_superdomain sd es, cross_superdomain_le_total sd es⟩

-- ==================== DEDUPLICATION BOUND ====================

/-- First-occurrence-preserving deduplication model matching `v2_loader.py`. -/
def dedupBy {α β : Type} [DecidableEq β] (key : α → β) : List β → List α → List α
  | _, [] => []
  | seen, x :: xs =>
    if key x ∈ seen then dedupBy key seen xs
    else x :: dedupBy key (key x :: seen) xs

/-- Deduplication never inflates dataset cardinality (`|dedup| <= |raw|`). -/
theorem dedupBy_length_le {α β : Type} [DecidableEq β] (key : α → β)
    (seen : List β) (xs : List α) :
    (dedupBy key seen xs).length ≤ xs.length := by
  induction xs generalizing seen with
  | nil => exact Nat.le_refl 0
  | cons x xs ih =>
    unfold dedupBy
    split
    · have h := ih seen
      simp only [List.length_cons]
      omega
    · have h := ih (key x :: seen)
      simp only [List.length_cons]
      omega

end MegaAtlasProofs.GraphInvariants
