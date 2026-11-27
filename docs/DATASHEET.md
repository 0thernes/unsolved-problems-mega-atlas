# Datasheet for the Unsolved Problems Mega-Atlas (`v2.10.0`)

> Structured according to Gebru et al. (2021), *"Datasheets for Datasets"*, Communications of the ACM 64(12).

---

## 1. Motivation

- **For what purpose was the dataset created?** To unify humanity's fragmented open-problem lists (spanning pure mathematics, logic/CS, fundamental physics, matter/chemistry, biology/neuroscience/medicine, AI/quantum/hardware/systems, engineering/design/earth/energy, and philosophy/economics/humanities — plus all 25 mathematical fronts on `https://lefttosolve.com/programs` backed by a daily-synced `59,396`-target mirror and `290` curated crosswalk matches) into a single schema-validated, biconnected, cross-linked multi-layer knowledge graph with transparent dual ranking (`0thernes CSS` + `Titan Index`), quantitative substrate/layer/gradient/margin/spectrum layers, `100% MRR@5` offline RAG & 13-tool MCP tooling (incl. rubric sensitivity diffing, live registry tracker & Left to Solve mirror explorer), a Lean 4.35.0 software-model invariant suite, 3 exact finite Track B probes (`LOG-002`, `NT-005`, `COMB-002`), and automated daily syncing across 16 global trackers & 25 Left to Solve fronts.
- **Who created and funded the dataset?** Independent researcher **Alexander Stephen Donahue** (`Independent Researcher, Spokane, WA, USA`; ORCID [`0009-0006-8168-9648`](https://orcid.org/0009-0006-8168-9648)), self-funded with zero external corporate or government sponsorship, utilizing disclosed frontier AI assistance under continuous human architectural direction and automated verification gates.

## 2. Composition

- **What do the instances represent?** Each of the **2,000 instances** represents a distinct unsolved, open, hard, or actively contested scientific, mathematical, engineering, or philosophical problem, enriched with **48 typed fields** (taxonomic lineage, formulation year/era/age, originator, status, explicit `verification_flag`, Nov 2026 AI verification notes, formal expression, 4 editorial 1–10 ratings, derived `css_score`, `titan_index`, `near_term_leverage_score`, strategic quadrant, NetworkX centralities, bottlenecks, approaches, 2026 progress, affected industries, cross-problem graph links, plus 8 multi-layer fields: `substrate_class`, `abstraction_layer`, `epistemic_spectrum_score`, `hardness_tractability_gradient`, `css_titan_margin`, `bridge_margin_ratio`, `adjacent_pillars_count`, `margin_role`).
- **Companion Relational Tables:** `edges` (6,108 biconnected undirected knowledge-graph couplings), `substrate_summary` (8 physical/formal substrates), `ai_audit_nov2026` (6 landmark Fall/Nov 2026 AI verification dossiers), `registries_nov2026` (16 global open-problem trackers), `lefttosolve_programs` (all 25 live fronts on `lefttosolve.com/programs`), `author_frontier_contributions` (`20` companion archive rows covering all `27` other audited entries in `0thernes-research-archive` Cycle-3 `RESULTS.md` [`94` results across `28` entries; `R85` = this repo] with explicit COI & parent-OPEN flags), `benchmarks` (20 resolved historical problems 1995–2026 paired with still-open twins), `contrasts` (15 deep pairwise cross-domain contrasts), `pillar_summary` (8 rows), `superdomain_summary` (28 rows), and `metadata` (run/version stats).
- **Does the dataset contain confidential, personally identifiable, or offensive content?** **No.** All records concern public scientific, mathematical, engineering, and philosophical research questions; person names refer exclusively to public historical and academic originators/researchers.
- **Are there missing values or known gaps?** Zero nulls in required schema fields (enforced by `schema/problem.schema.json`). Completeness is bounded: no finite list captures every open question in existence; `v2.3.0` closed 9 forensically identified blindspots via `m11_substrates_margins_adjacents.py` (`+52` problems) and `v2.9.0` integrated `100` strictly non-duplicate open conjectures across all `25` fronts of `lefttosolve.com/programs` via `m12_lefttosolve_programs.py` into an iteratively extensible 2,000-problem baseline.

## 3. Collection & Curation Process

- **How was the data acquired and compiled?** Twelve modular Python source files (`src/v2_data/m01..m12.py`, totaling `2,012` raw authored entries) were compiled under human direction with frontier AI assistance, benchmarked against named public registries (`Left to Solve` / `google-deepmind/formal-conjectures`, `ProofAtlas.ai`, `erdosproblems.com`, Clay CMI, Kourovka Notebook, Kirby's List, OEIS, Ben Green's 100, Open Quantum Problems, Hilbert's 23, Smale's 18, Brass–Moser–Pach, SEP/PhilPapers, NAE 14 Grand Challenges, DARPA/DOE Earthshots, IPCC, WHO, IRDS) and audited for Fall–November 2026 AI proof claims.
- **Provenance Labeling:** Every record carries an explicit `verification_flag`: `primary-registry-indexed` (`1,035`, `51.8%`), `ai-assisted-editorial-synthesis` (`942`, `47.1%`), `ai-claim-under-audit-nov2026` (`12`, `0.6%`), or `disputed-human-claim` (`11`, `0.6%`).

## 4. Preprocessing, Deduplication & Verification

- **Deduplication & Alias Redirection:** `src/v2_loader.py` enforces exact `id`, normalized title (`_norm_name`), and explicit cross-field duplicate uniqueness (`2,012 → 2,000`, `12` overlaps merged) while routing every incoming cross-reference through `dedup_alias_map` so **`unresolved_raw_links_count == 0`** and the connectome is audited by Python/NetworkX as strictly **2-vertex-connected (`0` articulation points, `0` bridges)**.
- **Formal & Automated Checks:**
  - **103 audited Lean 4.35.0 software-model theorems** (of `117` declarations in `lean/`, zero Mathlib, `0` `sorry`, per-theorem `#print axioms ⊆ [propext, Quot.sound]`, including `12` concrete NonVacuity witnesses, `10` constructive AdversarialTests refutations, and `9` Palomar targets checked by `6` kernel checks across `5` distinct implementations via `scripts/verify_lean_six_kernels.sh`). No Lean statement references the 2,000-row data or 6,108-edge graph.
  - **JSON Schema Draft 2020-12** (`schema/problem.schema.json`) validated on all 2,000 × 48 records.
  - **Deep Verification Ladder:** 50-digit `Decimal` reference oracle (`reference/scoring_oracle.py`), 1,000-example Hypothesis property suite, 2,000+ differential cases, `12/12` (100%) mutation-kill audit, `99` `pytest` checks, forensic auditor (`scripts/forensic_audit.py`), immutable **AutoResearch evaluator (`autoresearch/evaluate.py`, `AQS = 98.35`, `100% MRR@5`)**, and byte-exact **SHA-256 manifests (`CHECKSUMS.sha256`, `data/MANIFEST.sha256`, `croissant.json`, `ro-crate-metadata.json`)**.

## 5. Uses & Out-of-Scope Warnings

- **Recommended Uses:** Cross-disciplinary research mapping, R&D funding portfolio prioritization, bibliometric / knowledge-graph analytics, offline grounded RAG & MCP research agents, autonomous research benchmarking (`autoresearch/`), and educational exploration.
- **Explicit Out-of-Scope / Prohibited Misuses:**
  - Do **NOT** treat editorial 1–10 rubric ratings, `CSS`, `Titan Index`, or derived gradients/margins as peer-reviewed objective truth.
  - Do **NOT** treat any `ai-claim-under-audit-nov2026` entry as resolved or retired.
  - Do **NOT** represent the Lean 4.35.0 software-model proofs (or Track B finite probes) as formal proofs of any cataloged open conjecture.

## 6. Distribution & Maintenance

- **Distribution:** GitHub (`https://github.com/0thernes/unsolved-problems-mega-atlas`), GitHub Releases (`v2.10.0`), Live GitHub Pages (`https://0thernes.github.io/unsolved-problems-mega-atlas/`), 11-page AMS-LaTeX White Paper (`dist/Donahue_2026_unsolved_problems_mega_atlas.pdf`), structurally verified DigiCert RFC 3161 (`CHECKSUMS.sha256.tsr`) + 3-calendar Bitcoin OpenTimestamps v1 (`CHECKSUMS.sha256.ots`), Master Archive (`0TH-BUILD-007` in `0thernes/0thernes-research-archive`), plus Zenodo (`.zenodo.json` + `scripts/publish_zenodo.py`), MLCommons Croissant (`croissant.json`), W3C RO-Crate (`ro-crate-metadata.json`), and Software Heritage manual preservation (`docs/PRESERVATION.md`).
- **Licensing:** Dual-licensed — Data/Prose/Charts/White Paper under **CC BY 4.0** (`LICENSE`); Code/Schemas/RAG/MCP/Lean under **Apache-2.0** (`LICENSE-CODE`).
- **Maintenance:** Maintained by Alexander Stephen Donahue (`0_0@0thernes.art`) via semantic versioning (`CHANGELOG.md`), structured 10-class GitHub Issue templates, and community academic review (`docs/ACADEMIC_REVIEW.md`).
