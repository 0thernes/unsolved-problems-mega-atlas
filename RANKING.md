# Master Ranking — Unsolved Problems Mega-Atlas (V2.3.0)

> **Atlas `v2.3.0`** · **1,900 deduplicated problems** across **8 Macro-Pillars × 28 Superdomains** · Ranked hardest + most central + oldest + least tractable by the **0thernes Composite Severity Score (`CSS`, 0–100)**, alongside the **Composite Titan Index (0–10)**.
> **Author / Curator:** Alexander Stephen Donahue (0thernes LLC, Spokane, WA, USA, ORCID [`0009-0006-8168-9648`](https://orcid.org/0009-0006-8168-9648)) · **Reference Year:** `2026` (frozen for deterministic reproducibility).

## Formula & Honesty Clause

```text
CSS = 0.40 * (difficulty * 10)
    + 0.30 * (0.50 * (impact * 10) + 0.50 * min(100, 25 * ln(1 + graph_degree)))
    + 0.20 * min(100, max(0, (2026 - year_formulated) / 3))
    + 0.10 * (100 - tractability_2050 * 10)
```

- **Formally Verified Formula Invariants:** Exact bounds, monotonicity, weight normalization, and 300-year antiquity saturation are machine-checked in pure **Lean 4.35.0** (`lean/MegaAtlasProofs/Scoring.lean`, zero `sorry`, axioms strictly within `[propext, Quot.sound]`).
- **Epistemic Honesty Clause:** Input scores (`difficulty`, `impact`, `tractability_2050`, `interdisciplinarity`) are **curated AI-assisted editorial estimates**, not peer-reviewed consensus measurements. Treat this ranking as a **falsifiable argument**: disagree with a score? Edit the source entry in `src/v2_data/`, rebuild, and argue from the diff. See [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) and [`VERIFICATION.md`](VERIFICATION.md).

## Top 250 Problems Overall (Ranked by 0thernes CSS)

| Rank | ID | Problem | Macro-Pillar | Posed | CSS | Titan | Diff | Tract | Imp | Deg | Status (Nov 2026) | Verification Flag |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1 | `PHIL-004` | **The Is–Ought Gap, Meta-Ethical Moral Realism & Normative Convergence** | Philosophy | 1739 | **92.97** | 9.72 | 10 | 2 | 10 | 17 | Completely Open | `primary-registry-indexed` |
| 2 | `PHIL-003` | **Free Will, Determinism, Indeterminism & Moral Responsibility** | Philosophy | 300 BCE | **90.13** | 9.23 | 10 | 2 | 9 | 9 | Completely Open | `primary-registry-indexed` |
| 3 | `PHIL-001` | **The Mind–Body Problem & Metaphysics of Mental Causation (Exclusion Problem)** | Philosophy | 1641 | **89.90** | 8.96 | 10 | 2 | 8 | 13 | Completely Open | `primary-registry-indexed` |
| 4 | `PHIL-006` | **Why Is There Something Rather Than Nothing? (Ultimate Primordial Existence)** | Philosophy | 1714 | **86.80** | 8.24 | 10 | 1 | 7 | 6 | Completely Open | `primary-registry-indexed` |
| 5 | `PHIL-002` | **The Problem of Induction & Goodman's New Riddle ('Grue')** | Philosophy | 1739 | **85.76** | 8.66 | 9 | 2 | 8 | 16 | Completely Open | `primary-registry-indexed` |
| 6 | `GR-001` | **Quantum Gravity (Unification of General Relativity & Quantum Mechanics)** | Fundamental Physics | 1930 | **83.40** | 10.00 | 10 | 3 | 10 | 57 | Completely Open | `primary-registry-indexed` |
| 7 | `ANL-001` | **3D Navier–Stokes Existence and Smoothness** | Pure Mathematics | 1822 | **82.98** | 9.31 | 10 | 7 | 9 | 30 | AI Proof Claim (Fall/Nov 2026) — Under Verification | `ai-claim-under-audit-nov2026` |
| 8 | `ANL-002` | **3D Incompressible Euler Equations Finite-Time Blowup (Smooth Boundaryless ℝ³)** | Pure Mathematics | 1757 | **82.83** | 8.56 | 10 | 7 | 8 | 13 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 9 | `GEOM-003` | **Sphere Packing Optimal Density in General Dimensions (d ≠ 1, 2, 3, 8, 24)** | Pure Mathematics | 1611 | **82.07** | 7.45 | 9 | 5 | 6 | 24 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 10 | `NT-001` | **Riemann Hypothesis** | Pure Mathematics | 1859 | **81.97** | 9.34 | 10 | 6 | 9 | 34 | AI Proof Claim (Fall/Nov 2026) — Under Verification | `ai-claim-under-audit-nov2026` |
| 11 | `QM-006` | **Thermodynamic Arrow of Time & Origin of the Past Hypothesis** | Fundamental Physics | 1877 | **81.81** | 9.16 | 10 | 3 | 8 | 30 | Completely Open | `ai-assisted-editorial-synthesis` |
| 12 | `CS-001` | **P versus NP Problem** | Logic | 1971 | **81.67** | 10.00 | 10 | 2 | 10 | 67 | Completely Open | `primary-registry-indexed` |
| 13 | `PHIL-044` | **Infinite Ethics, St. Petersburg Fanaticism & Pascal's Mugging in Expected-Value Theory** | Philosophy | 1713 | **81.30** | 8.24 | 9 | 4 | 8 | 6 | Completely Open | `ai-assisted-editorial-synthesis` |
| 14 | `BIO-001` | **Abiogenesis: Origin of Life & RNA-to-Ribosome Genetic Code Transition** | Life | 1871 | **81.27** | 9.55 | 10 | 6 | 9 | 35 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 15 | `PHIL-024` | **External-World Skepticism, Brain-in-a-Vat & Epistemic Closure Paradoxes** | Philosophy | 1641 | **81.22** | 7.65 | 9 | 2 | 7 | 5 | Completely Open | `primary-registry-indexed` |
| 16 | `PHIL-023` | **Agrippa's Trilemma (Münchhausen Trilemma) & Foundations of Epistemic Justification** | Philosophy | 100 | **80.54** | 7.60 | 9 | 2 | 7 | 4 | Completely Open | `primary-registry-indexed` |
| 17 | `PHIL-008` | **Problem of Universals, Mathematical Platonism & Benacerraf's Epistemological Dilemma** | Philosophy | 380 BCE | **80.30** | 7.34 | 9 | 2 | 6 | 6 | Completely Open | `primary-registry-indexed` |
| 18 | `PHIL-027` | **Semantic Paradoxes (Liar & Curry Paradoxes) & Unified Formal Theory of Truth** | Philosophy | 350 BCE | **80.24** | 7.20 | 9 | 3 | 6 | 8 | Completely Open | `primary-registry-indexed` |
| 19 | `QM-001` | **Quantum Measurement Problem & Wavefunction Collapse** | Fundamental Physics | 1927 | **80.20** | 9.59 | 10 | 4 | 9 | 42 | Completely Open | `primary-registry-indexed` |
| 20 | `PHIL-057` | **The Problem of Evil, Divine Hiddenness & Skeptical Theism in Philosophy of Religion** | Philosophy | 300 BCE | **80.04** | 7.05 | 9 | 1 | 6 | 4 | Completely Open | `primary-registry-indexed` |
| 21 | `SUB-050` | **Exact Classification of Ancient & Modern Diophantine Irrationality Measures (ζ(3), π, e, Catalan G)** | Pure Mathematics | 450 BCE | **79.54** | 6.65 | 10 | 4 | 5 | 4 | Completely Open | `primary-registry-indexed` |
| 22 | `CS-002` | **Unconditional Existence of One-Way Functions (Impagliazzo's Five Worlds)** | Logic | 1976 | **79.17** | 9.52 | 10 | 3 | 10 | 39 | Completely Open | `ai-assisted-editorial-synthesis` |
| 23 | `FLD-001` | **Universal Statistical Theory of Fluid Turbulence & Intermittency Closure** | Matter | 1941 | **79.17** | 9.45 | 10 | 5 | 9 | 73 | Completely Open | `ai-assisted-editorial-synthesis` |
| 24 | `HUM-044` | **International Law Without a Sovereign: Sovereignty, Jus Cogens & Cyber/Space Treaty Architecture** | Philosophy | 1625 | **78.72** | 8.55 | 8 | 5 | 10 | 5 | Experimental Tension / Crisis | `ai-assisted-editorial-synthesis` |
| 25 | `PHIL-007` | **Personal Identity Over Time (Ship of Theseus, Teletransportation & Fission Paradoxes)** | Philosophy | 1689 | **78.30** | 7.89 | 8 | 3 | 8 | 6 | Completely Open | `primary-registry-indexed` |
| 26 | `NEURO-001` | **The Hard Problem of Consciousness (Explanatory Gap & Subjective Qualia)** | Life | 1995 | **78.29** | 9.88 | 10 | 2 | 10 | 33 | Completely Open | `ai-assisted-editorial-synthesis` |
| 27 | `CS-009` | **Classical Complexity of Integer Factorization & Discrete Logarithm** | Logic | 1801 | **77.80** | 8.39 | 9 | 4 | 9 | 6 | Completely Open | `ai-assisted-editorial-synthesis` |
| 28 | `NT-003` | **Goldbach's Strong Conjecture** | Pure Mathematics | 1742 | **77.75** | 6.32 | 9 | 4 | 5 | 11 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 29 | `NT-071` | **Irrationality of Odd Zeta Values (zeta(5), zeta(7), ...) & Catalan's Constant** | Pure Mathematics | 1735 | **77.62** | 7.25 | 9 | 5 | 7 | 5 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 30 | `GR-004` | **Dimensionality & Signature of Spacetime (Why 3+1 Dimensions?)** | Fundamental Physics | 1917 | **77.11** | 8.62 | 10 | 3 | 8 | 17 | Completely Open | `ai-assisted-editorial-synthesis` |
| 31 | `NT-041` | **Congruent Number Problem (Unconditional Effective Characterization)** | Pure Mathematics | 972 | **76.72** | 6.70 | 9 | 5 | 6 | 5 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 32 | `NT-070` | **Irrationality & Transcendence of the Euler-Mascheroni Constant (gamma)** | Pure Mathematics | 1734 | **76.69** | 6.35 | 9 | 3 | 5 | 5 | Completely Open | `primary-registry-indexed` |
| 33 | `NT-002` | **Generalized & Grand Riemann Hypotheses (GRH)** | Pure Mathematics | 1884 | **76.62** | 8.58 | 10 | 5 | 8 | 14 | AI Proof Claim (Fall/Nov 2026) — Under Verification | `ai-claim-under-audit-nov2026` |
| 34 | `PHIL-026` | **The Sorites Paradox & Formal Logic of Higher-Order Vagueness** | Philosophy | 350 BCE | **76.24** | 7.05 | 8 | 3 | 6 | 8 | Completely Open | `primary-registry-indexed` |
| 35 | `GEO-001` | **Deterministic Short-Term Earthquake Prediction** | Engineering | 1906 | **76.23** | 9.00 | 9 | 4 | 10 | 19 | Completely Open | `primary-registry-indexed` |
| 36 | `QM-002` | **Yang–Mills Existence and Mass Gap** | Fundamental Physics | 1954 | **76.16** | 8.72 | 10 | 3 | 8 | 26 | AI Proof Claim (Fall/Nov 2026) — Under Verification | `ai-claim-under-audit-nov2026` |
| 37 | `CM-003` | **Ambient-Pressure Room-Temperature Superconductivity (T_c ≥ 295 K, 1 atm)** | Matter | 1911 | **75.96** | 9.09 | 10 | 4 | 10 | 6 | Completely Open | `primary-registry-indexed` |
| 38 | `LOG-001` | **Continuum Hypothesis (CH) & Ultimate Foundations of Set Theory** | Logic | 1878 | **75.76** | 7.66 | 10 | 3 | 6 | 13 | Independent / Undecidable Suspected | `primary-registry-indexed` |
| 39 | `NT-008` | **Arithmetic Langlands Program (Global Functoriality & Reciprocity)** | Pure Mathematics | 1967 | **75.66** | 9.53 | 10 | 5 | 9 | 33 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 40 | `XNT-026` | **Gauss Circle Problem Exact Error Exponent (θ = 1/4)** | Pure Mathematics | 1837 | **74.90** | 7.49 | 10 | 4 | 6 | 6 | Partially Solved / Special Cases | `ai-assisted-editorial-synthesis` |
| 41 | `PHIL-012` | **Nature of Causation, Counterfactual Dependence & Preemption Paradoxes** | Philosophy | 1748 | **74.83** | 8.09 | 8 | 5 | 8 | 6 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 42 | `CM-051` | **Atomic-Scale Tribology: Origin of Macroscopic Friction, Superlubricity & Wear Laws** | Matter | 1699 | **74.80** | 8.04 | 8 | 8 | 9 | 6 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 43 | `ENG-008` | **First-Principles Tribology: Predicting Macroscopic Friction, Wear & Structural Superlubricity** | Engineering | 1493 | **74.80** | 8.04 | 8 | 8 | 9 | 6 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 44 | `AI-001` | **AI Alignment, Scalable Oversight & Value Specification for Superhuman Agents** | AI | 2001 | **74.77** | 9.94 | 10 | 6 | 10 | 42 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 45 | `QM-050` | **Origin of the Fine-Structure Constant (α ≈ 1/137.036) & Fundamental Dimensionless Ratios** | Fundamental Physics | 1916 | **74.63** | 8.39 | 10 | 2 | 8 | 6 | Completely Open | `ai-assisted-editorial-synthesis` |
| 46 | `CHEM-001` | **Many-Body Electronic Structure & Exponential Wall of Quantum Chemistry** | Matter | 1929 | **74.48** | 9.38 | 9 | 7 | 10 | 41 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 47 | `BIO-031` | **Mechanisms of Complete Whole-Body & Limb Regeneration (Planaria & Salamanders vs. Mammalian Scarring)** | Life | 1768 | **74.44** | 8.65 | 8 | 8 | 10 | 8 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 48 | `NT-081` | **Infinitude of Kummer-Regular, Sophie Germain, Fermat & Non-Wieferich Primes** | Pure Mathematics | 1640 | **74.30** | 5.87 | 8 | 3 | 5 | 7 | Completely Open | `primary-registry-indexed` |
| 49 | `SUB-046` | **First-Principles Multiscale Law of Dry Friction, Wear & Structural Superlubricity (Tribology)** | Engineering | 1493 | **74.22** | 8.00 | 8 | 8 | 9 | 5 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 50 | `PHIL-019` | **Problem of Other Minds & Epistemic Access to Alien / Synthetic Subjectivity** | Philosophy | 1865 | **74.03** | 8.82 | 9 | 4 | 9 | 7 | Experimental Tension / Crisis | `primary-registry-indexed` |
| 51 | `CS-003` | **BQP vs. NP, PH & Exact Boundaries of Quantum Computational Power** | Logic | 1993 | **73.74** | 9.19 | 10 | 3 | 9 | 18 | Partially Solved / Special Cases | `ai-assisted-editorial-synthesis` |
| 52 | `NT-052` | **Gauss's Class Number Problem for Real Quadratic Fields** | Pure Mathematics | 1801 | **73.72** | 6.50 | 9 | 3 | 6 | 5 | Completely Open | `primary-registry-indexed` |
| 53 | `ANL-005` | **Global Regularity vs. Shock/Implosion Classification for 3D Compressible Navier–Stokes & Euler** | Pure Mathematics | 1848 | **73.66** | 8.04 | 10 | 6 | 7 | 6 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 54 | `ALG-061` | **Grothendieck's Standard Conjectures on Algebraic Cycles** | Pure Mathematics | 1968 | **73.61** | 8.80 | 10 | 2 | 9 | 8 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 55 | `PHIL-018` | **Panpsychism, Cosmopsychism & the Combination Problem of Micro-Experiences** | Philosophy | 1890 | **73.60** | 8.15 | 10 | 2 | 7 | 4 | Completely Open | `primary-registry-indexed` |
| 56 | `ENG-002` | **High-Thrust Non-Chemical Space Propulsion Beyond the Tsiolkovsky Rocket Tyranny** | Engineering | 1903 | **73.45** | 8.95 | 9 | 7 | 9 | 29 | Completely Open | `primary-registry-indexed` |
| 57 | `HUM-001` | **Evolutionary Origin of Human Language (Glottogony)** | Philosophy | 1866 | **73.40** | 8.35 | 9 | 5 | 7 | 19 | Completely Open | `primary-registry-indexed` |
| 58 | `ECON-003` | **Global Collective Action & Tragedy of the Commons Without a World Sovereign** | Philosophy | 1968 | **73.22** | 9.61 | 9 | 6 | 10 | 45 | Experimental Tension / Crisis | `ai-assisted-editorial-synthesis` |
| 59 | `ECON-001` | **Unified Micro-to-Macro Non-Equilibrium Economic Theory (Beyond Representative-Agent DSGE)** | Philosophy | 1936 | **73.22** | 9.26 | 9 | 6 | 10 | 25 | Completely Open | `primary-registry-indexed` |
| 60 | `CS-010` | **Super-Linear Explicit Boolean Circuit Lower Bounds & Natural Proofs Barrier** | Logic | 1949 | **73.13** | 8.30 | 10 | 3 | 8 | 10 | Completely Open | `primary-registry-indexed` |
| 61 | `GEOM-001` | **Hodge Conjecture** | Pure Mathematics | 1950 | **73.11** | 7.74 | 10 | 2 | 6 | 18 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 62 | `ANL-007` | **Global Classical Solutions of the Full Boltzmann Equation Far from Equilibrium** | Pure Mathematics | 1872 | **72.99** | 8.55 | 10 | 6 | 8 | 5 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 63 | `NT-006` | **Birch and Swinnerton-Dyer Conjecture (BSD)** | Pure Mathematics | 1965 | **72.91** | 8.62 | 10 | 4 | 8 | 17 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 64 | `XNT-027` | **Dirichlet Divisor Problem Exact Error Exponent (Δ(x) = O(x^{1/4 + ε}))** | Pure Mathematics | 1849 | **72.84** | 7.00 | 10 | 4 | 6 | 4 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 65 | `GR-018` | **Resolution of Spacetime Singularities (Black Hole Cores & Big Bang t = 0)** | Fundamental Physics | 1965 | **72.81** | 8.80 | 10 | 3 | 9 | 8 | Completely Open | `ai-assisted-editorial-synthesis` |
| 66 | `AI-003` | **The Simulation Hypothesis & Empirical Testability of Computational Reality** | AI | 2003 | **72.67** | 9.23 | 10 | 1 | 9 | 9 | Completely Open | `primary-registry-indexed` |
| 67 | `NT-068` | **Schanuel's Conjecture** | Pure Mathematics | 1966 | **72.63** | 8.28 | 10 | 2 | 8 | 9 | Completely Open | `primary-registry-indexed` |
| 68 | `FLD-054` | **Universal Variational Principle for Far-From-Equilibrium Steady States (Beyond Minimum Entropy Production)** | Matter | 1945 | **72.53** | 9.23 | 10 | 5 | 9 | 9 | Completely Open | `ai-assisted-editorial-synthesis` |
| 69 | `NT-007` | **abc Conjecture (Oesterlé-Masser)** | Pure Mathematics | 1985 | **72.49** | 8.48 | 10 | 4 | 8 | 22 | Disputed Human Claim / Under Peer Review | `disputed-human-claim` |
| 70 | `NT-076` | **Erdős-Turán Conjecture on Arithmetic Progressions** | Pure Mathematics | 1936 | **72.49** | 7.75 | 10 | 3 | 7 | 10 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 71 | `MED-001` | **Root Cause, Prevention & Curative Reversal of Neurodegenerative Diseases (Alzheimer's, Parkinson's, ALS)** | Life | 1906 | **72.42** | 9.21 | 9 | 8 | 10 | 20 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 72 | `NT-075` | **Grothendieck & Kontsevich-Zagier Period Conjectures** | Pure Mathematics | 1966 | **72.24** | 8.65 | 10 | 2 | 8 | 8 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 73 | `COMB-002` | **Exact Ramsey Numbers (R(5, 5) and Diagonal Asymptotic Growth Rate)** | Pure Mathematics | 1930 | **72.16** | 7.78 | 10 | 5 | 6 | 22 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 74 | `NEURO-055` | **Biological Root Etiology & Mechanistic Circuit Biotypes of Severe Psychiatric Disorders** | Life | 1899 | **72.09** | 9.09 | 9 | 7 | 10 | 12 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 75 | `AI-002` | **True Out-of-Distribution Causal Reasoning, Continual Lifelong Learning & AGI** | AI | 1950 | **72.08** | 9.38 | 9 | 8 | 10 | 41 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 76 | `XNT-043` | **Unconditional Rubinstein–Sarnak Prime Number Races & Chebyshev Bias Density** | Pure Mathematics | 1853 | **72.07** | 6.65 | 10 | 3 | 5 | 4 | Partially Solved / Special Cases | `ai-assisted-editorial-synthesis` |
| 77 | `NT-080` | **Existence of Odd Perfect Numbers & Infinitude of Mersenne Primes** | Pure Mathematics | 300 BCE | **72.04** | 5.20 | 8 | 2 | 4 | 4 | Completely Open | `primary-registry-indexed` |
| 78 | `NT-045` | **Tate Conjecture on Algebraic Cycles** | Pure Mathematics | 1963 | **71.94** | 8.80 | 10 | 4 | 9 | 8 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 79 | `NT-042` | **Vojta's Conjecture** | Pure Mathematics | 1987 | **71.90** | 8.77 | 10 | 2 | 9 | 7 | Completely Open | `primary-registry-indexed` |
| 80 | `STAT-005` | **Rigorous Kinetic & Hydrodynamic Limits Beyond Classical Hard Spheres (Post-2025 Hilbert's 6th)** | Logic | 1900 | **71.70** | 8.79 | 10 | 6 | 8 | 6 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 81 | `GEOM-002` | **Smooth 4-Dimensional Poincaré Conjecture (SPC4)** | Pure Mathematics | 1961 | **71.55** | 7.81 | 10 | 4 | 6 | 25 | Completely Open | `primary-registry-indexed` |
| 82 | `SYS-001` | **High-Dimensional Nonlinear & Stochastic Optimal Control (Breaking Bellman's Curse)** | AI | 1957 | **71.46** | 9.06 | 9 | 7 | 9 | 45 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 83 | `NT-004` | **Twin Prime & Polignac's Conjectures** | Pure Mathematics | 1849 | **71.46** | 6.38 | 9 | 4 | 5 | 14 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 84 | `COMB-001` | **Hadwiger's Conjecture (Graph Coloring and Clique Minors)** | Pure Mathematics | 1943 | **71.45** | 7.59 | 10 | 5 | 6 | 23 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 85 | `AI-004` | **Whole-Brain Emulation (WBE) & High-Fidelity Biological Digital Twins** | AI | 2008 | **71.19** | 9.60 | 10 | 4 | 10 | 10 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 86 | `ANL-014` | **Strong and Weak Cosmic Censorship Conjectures (PDE Formulation of Einstein's Equations)** | Pure Mathematics | 1969 | **71.12** | 8.72 | 10 | 4 | 8 | 11 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 87 | `NT-065` | **Perfect Cuboid (Perfect Euler Brick) Problem** | Pure Mathematics | 1719 | **71.04** | 5.40 | 8 | 3 | 4 | 4 | Completely Open | `primary-registry-indexed` |
| 88 | `GR-032` | **The Problem of Time in Quantum Gravity (Frozen Wheeler–DeWitt Formalism)** | Fundamental Physics | 1967 | **70.93** | 8.70 | 10 | 4 | 8 | 10 | Completely Open | `ai-assisted-editorial-synthesis` |
| 89 | `ASTRO-004` | **The Fermi Paradox & Search for Extraterrestrial Life / Technosignatures** | Fundamental Physics | 1950 | **70.91** | 9.37 | 9 | 6 | 10 | 17 | Completely Open | `primary-registry-indexed` |
| 90 | `STAT-008` | **Rigorous Scaling Limit & Conformal Invariance of the 3D Critical Ising Model** | Logic | 1925 | **70.87** | 8.33 | 10 | 5 | 7 | 9 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 91 | `XNT-028` | **Piltz Higher-Order Divisor Problem Exponent (Δ_k(x) = O(x^{(k-1)/(2k) + ε}), k ≥ 3)** | Pure Mathematics | 1881 | **70.87** | 6.75 | 10 | 3 | 6 | 3 | Completely Open | `ai-assisted-editorial-synthesis` |
| 92 | `ENG-001` | **First-Principles Multiscale Prediction of Structural Fatigue, Creep & Stress-Corrosion Failure** | Engineering | 1860 | **70.78** | 8.36 | 8 | 8 | 9 | 25 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 93 | `GR-002` | **Black Hole Information Paradox, Firewalls & Interior Reconstruction** | Fundamental Physics | 1975 | **70.63** | 8.85 | 10 | 6 | 8 | 19 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 94 | `QM-021` | **Constructive Non-Perturbative 4D Interacting Quantum Field Theory (Hilbert's 6th Quantum Extension)** | Fundamental Physics | 1956 | **70.49** | 8.17 | 10 | 4 | 7 | 11 | Completely Open | `primary-registry-indexed` |
| 95 | `ANL-050` | **Hilbert's 16th Problem (Part II: Limit Cycles of Planar Polynomial Vector Fields)** | Pure Mathematics | 1900 | **70.44** | 7.20 | 10 | 3 | 6 | 4 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 96 | `GR-003` | **Quantum Holography Beyond AdS (dS/CFT & Celestial Flat-Space Holography)** | Fundamental Physics | 1993 | **70.43** | 8.65 | 10 | 5 | 8 | 19 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 97 | `ASTRO-002` | **Dark Energy & Cosmological Constant Problem (10^120 Discrepancy & DESI Evolving w(z))** | Fundamental Physics | 1998 | **70.21** | 9.17 | 10 | 6 | 9 | 17 | Experimental Tension / Crisis | `ai-assisted-editorial-synthesis` |
| 98 | `GEO-002` | **Equilibrium Climate Sensitivity (ECS) Tight Constraint & Cloud–Aerosol Feedback Physics** | Engineering | 1979 | **70.09** | 9.45 | 9 | 9 | 10 | 53 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 99 | `GR-065` | **Multiverse Realities: Empirical Testability of Bubble Collisions, Brane Worlds & Parallel Branches** | Fundamental Physics | 1983 | **70.09** | 9.10 | 10 | 3 | 9 | 5 | Completely Open | `primary-registry-indexed` |
| 100 | `FLD-002` | **Burning Fusion Plasma Confinement, Disruption Prediction & ELM Control** | Matter | 1951 | **70.07** | 9.25 | 9 | 8 | 10 | 24 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 101 | `NT-061` | **Hilbert's 10th Problem over the Rational Numbers Q** | Pure Mathematics | 1900 | **70.03** | 8.33 | 9 | 5 | 8 | 9 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 102 | `NT-067` | **Effective Roth's Theorem & Effective Mordell's Theorem** | Pure Mathematics | 1955 | **70.03** | 7.99 | 10 | 4 | 8 | 6 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 103 | `NT-079` | **Waring's Problem Exact Thresholds G(k), Ideal g(k) & Mahler's 3/2 Problem** | Pure Mathematics | 1770 | **69.86** | 5.84 | 8 | 4 | 5 | 6 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 104 | `XNT-029` | **Mertens Function Optimal Growth Rate & Unboundedness of M(x) / √x** | Pure Mathematics | 1897 | **69.80** | 6.95 | 10 | 3 | 6 | 3 | Completely Open | `primary-registry-indexed` |
| 105 | `GR-035` | **Nature of the Present Moment ('Now'): Block Universe vs. Dynamical Becoming** | Fundamental Physics | 1905 | **69.79** | 8.40 | 9 | 3 | 8 | 5 | Completely Open | `ai-assisted-editorial-synthesis` |
| 106 | `XNT-039` | **Infinitude of Wilson Primes** | Pure Mathematics | 1770 | **69.77** | 5.15 | 9 | 3 | 3 | 3 | Completely Open | `ai-assisted-editorial-synthesis` |
| 107 | `GEOM-055` | **Kissing Number Problem in General Dimensions (d ≥ 5, d ≠ 8, 24)** | Pure Mathematics | 1694 | **69.72** | 5.85 | 8 | 5 | 4 | 5 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 108 | `PHIL-058` | **Meaning of Life, Axiology of Suffering & Anti-Natalism vs. Pro-Natalism Debates** | Philosophy | 1851 | **69.70** | 7.60 | 8 | 2 | 8 | 4 | Completely Open | `primary-registry-indexed` |
| 109 | `BIO-002` | **Fundamental Evolutionary & Mechanistic Cause of Biological Aging (Senescence)** | Life | 1952 | **69.69** | 9.23 | 9 | 8 | 10 | 22 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 110 | `ASTRO-010` | **Ultimate Fate of the Universe (Heat Death, Big Rip, Big Crunch or Vacuum Decay)** | Fundamental Physics | 1922 | **69.65** | 8.90 | 9 | 5 | 10 | 5 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 111 | `SUB-030` | **Computational Complexity & Curse of Dimensionality in Wasserstein & Gromov–Wasserstein Transport** | Logic | 1781 | **69.63** | 7.89 | 8 | 8 | 8 | 6 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 112 | `CS-007` | **NP vs. coNP & Infinite Strictness of the Polynomial Hierarchy (PH)** | Logic | 1973 | **69.57** | 8.10 | 10 | 2 | 8 | 4 | Completely Open | `ai-assisted-editorial-synthesis` |
| 113 | `ALG-001` | **Inverse Galois Problem** | Pure Mathematics | 1892 | **69.57** | 7.93 | 9 | 6 | 8 | 9 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 114 | `MED-002` | **Zero-Failure In Silico Drug Design & Accurate Human In Vivo Toxicity/Efficacy Prediction** | Life | 1990 | **69.50** | 9.39 | 9 | 8 | 10 | 42 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 115 | `ALG-062` | **Bloch-Beilinson Conjecture on Mixed Motives & Chow Filtration** | Pure Mathematics | 1982 | **69.47** | 8.65 | 10 | 3 | 9 | 4 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 116 | `NT-036` | **Finiteness of Tate-Shafarevich Groups (Sha Conjecture)** | Pure Mathematics | 1957 | **69.32** | 7.95 | 10 | 4 | 8 | 5 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 117 | `NEURO-002` | **The Neural Code & Compositional Representation of Meaning in Cortex** | Life | 1968 | **69.29** | 9.03 | 9 | 8 | 9 | 40 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 118 | `COMB-041` | **Prime Power Conjecture for Finite Projective Planes** | Pure Mathematics | 1906 | **69.22** | 6.90 | 10 | 3 | 5 | 5 | Partially Solved / Special Cases | `ai-assisted-editorial-synthesis` |
| 119 | `NT-043` | **Bombieri-Lang Conjecture** | Pure Mathematics | 1974 | **69.19** | 8.15 | 10 | 3 | 8 | 5 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 120 | `QM-022` | **Exact Dynamical Mechanism of Quark Color Confinement & Chiral Symmetry Breaking** | Fundamental Physics | 1973 | **69.19** | 8.03 | 10 | 5 | 7 | 14 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 121 | `NT-027` | **Ramanujan-Petersson Conjecture for Maass Forms & General GL_n** | Pure Mathematics | 1916 | **69.13** | 7.87 | 9 | 4 | 8 | 7 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 122 | `ASTRO-001` | **Nature of Dark Matter** | Fundamental Physics | 1933 | **69.12** | 8.86 | 9 | 8 | 9 | 20 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 123 | `ENR-001` | **Economically Viable Net-Electricity Commercial Nuclear Fusion (Q_eng > 10)** | Engineering | 1951 | **68.84** | 9.37 | 9 | 8 | 10 | 17 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 124 | `CS-005` | **P vs. PSPACE, L vs. P & NC vs. P (Time, Space & Parallelism Hierarchy)** | Logic | 1973 | **68.83** | 8.19 | 10 | 4 | 8 | 6 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 125 | `HUM-046` | **Computational Aesthetics, Universals of Beauty & Why Music Evokes Deep Emotion** | Philosophy | 500 BCE | **68.80** | 7.19 | 7 | 7 | 7 | 6 | Completely Open | `ai-assisted-editorial-synthesis` |
| 126 | `NT-031` | **Bloch-Kato Tamagawa Number Conjecture** | Pure Mathematics | 1990 | **68.70** | 8.39 | 10 | 3 | 8 | 6 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 127 | `ENG-003` | **Carbon-Negative, Self-Healing, 500-Year Durable Civil Infrastructure Materials (Beyond Portland Cement)** | Engineering | 1824 | **68.70** | 8.30 | 7 | 9 | 10 | 19 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 128 | `STAT-034` | **Optimal Transport Regularity for General Non-Quadratic Costs (MTW Curvature Frontier)** | Logic | 1781 | **68.63** | 6.99 | 8 | 6 | 6 | 6 | Partially Solved / Special Cases | `ai-assisted-editorial-synthesis` |
| 129 | `PHIL-055` | **Philosophy of Punishment: Retributivism, Deterrence & Restorative Justice Without Libertarian Free Will** | Philosophy | 1764 | **68.50** | 7.45 | 7 | 5 | 8 | 4 | Completely Open | `primary-registry-indexed` |
| 130 | `NT-020` | **Landau's Fourth Problem & Bunyakovsky Conjecture (n^2 + 1 Primes)** | Pure Mathematics | 1857 | **68.49** | 6.15 | 9 | 3 | 5 | 5 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 131 | `COMB-023` | **Turán's Hypergraph Conjecture (Exact Turán Density of K₄⁽³⁾ = 5/9)** | Pure Mathematics | 1941 | **68.46** | 7.12 | 10 | 4 | 6 | 7 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 132 | `GR-044` | **Emergent Spacetime from Quantum Entanglement (It from Qubit & Bulk Reconstruction)** | Fundamental Physics | 2006 | **68.45** | 9.29 | 10 | 6 | 9 | 12 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 133 | `GR-006` | **String Landscape Vacuum Selection & The Swampland Program** | Fundamental Physics | 2003 | **68.43** | 8.56 | 10 | 5 | 8 | 13 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 134 | `XNT-045` | **Breaking the Burgess q^{1/4} Character-Sum Barrier Unconditionally** | Pure Mathematics | 1957 | **68.40** | 7.44 | 10 | 4 | 7 | 6 | Completely Open | `primary-registry-indexed` |
| 135 | `ANL-038` | **Invariant Subspace Problem for Separable Hilbert Spaces** | Pure Mathematics | 1935 | **68.36** | 6.97 | 10 | 3 | 5 | 7 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 136 | `NEURO-003` | **Objective Detection of Sentience in Non-Human Animals, Organoids & AI** | Life | 2020 | **68.32** | 9.44 | 9 | 5 | 10 | 23 | Completely Open | `ai-assisted-editorial-synthesis` |
| 137 | `COMB-037` | **Van der Waerden Numbers W(k, r) Tight Asymptotic Bounds** | Pure Mathematics | 1927 | **68.32** | 7.25 | 10 | 4 | 6 | 5 | Partially Solved / Special Cases | `ai-assisted-editorial-synthesis` |
| 138 | `STAT-023` | **3D Stochastic Navier–Stokes: Uniqueness in Law, Ergodicity & Anomalous Dissipation** | Logic | 1973 | **68.25** | 8.55 | 10 | 4 | 8 | 5 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 139 | `QC-001` | **Scalable Fault-Tolerant Quantum Computer (1,000+ Logical Qubits at <10^-12 Error)** | AI | 1995 | **68.17** | 9.39 | 9 | 9 | 10 | 42 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 140 | `ANL-006` | **Global Regularity of 3D Magnetohydrodynamics (MHD) and Hall-MHD Equations** | Pure Mathematics | 1942 | **68.14** | 7.95 | 10 | 4 | 7 | 4 | Completely Open | `ai-assisted-editorial-synthesis` |
| 141 | `PHIL-009` | **Philosophy of Time: Presentism, Growing Block & Eternalism (McTaggart's A/B-Series)** | Philosophy | 1908 | **68.09** | 8.05 | 9 | 3 | 7 | 5 | Completely Open | `primary-registry-indexed` |
| 142 | `PHIL-016` | **Strong Emergence vs. Microphysical Reductionism & Downward Causation** | Philosophy | 1925 | **68.03** | 8.44 | 9 | 4 | 8 | 6 | Completely Open | `primary-registry-indexed` |
| 143 | `PHIL-041` | **Population Ethics: Parfit's Repugnant Conclusion & Arrhenius Impossibility Theorems** | Philosophy | 1984 | **67.93** | 8.68 | 9 | 3 | 9 | 9 | Completely Open | `ai-assisted-editorial-synthesis` |
| 144 | `CS-019` | **Superpolynomial Proof Complexity Lower Bounds for Frege & Extended Frege Systems** | Logic | 1979 | **67.93** | 7.84 | 10 | 3 | 7 | 6 | Completely Open | `ai-assisted-editorial-synthesis` |
| 145 | `GR-022` | **Microscopic Origin of Bekenstein–Hawking Entropy for Generic Kerr Black Holes** | Fundamental Physics | 1972 | **67.90** | 8.39 | 10 | 5 | 8 | 6 | Partially Solved / Special Cases | `ai-assisted-editorial-synthesis` |
| 146 | `PHIL-020` | **Metaphysics of Quantum Reality: Wavefunction Realism, Primitive Ontology & Relationalism** | Philosophy | 1927 | **67.90** | 8.12 | 9 | 3 | 7 | 7 | Completely Open | `primary-registry-indexed` |
| 147 | `ANL-018` | **Prandtl Boundary Layer Equations and the Inviscid Limit of 2D/3D Navier–Stokes** | Pure Mathematics | 1904 | **67.85** | 8.00 | 9 | 5 | 8 | 5 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 148 | `XNT-033` | **Irrationality of Brun's Twin-Prime Constant B_2** | Pure Mathematics | 1919 | **67.83** | 6.20 | 10 | 2 | 5 | 3 | Completely Open | `ai-assisted-editorial-synthesis` |
| 149 | `ALG-025` | **Whitehead's Asphericity Conjecture** | Pure Mathematics | 1941 | **67.80** | 7.58 | 9 | 3 | 7 | 9 | Completely Open | `primary-registry-indexed` |
| 150 | `FLD-046` | **Lightning Initiation Paradox, Stepped-Leader Propagation & Terrestrial Gamma-Ray Flashes** | Matter | 1752 | **67.80** | 7.25 | 8 | 9 | 7 | 4 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 151 | `GEO-024` | **Lightning Initiation Paradox, Runaway Relativistic Electron Avalanches & Terrestrial Gamma-Ray Flashes** | Engineering | 1752 | **67.80** | 7.25 | 8 | 9 | 7 | 4 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 152 | `ANL-039` | **Free Group Factor Isomorphism Problem (L(F₂) ≅ L(F₃)?)** | Pure Mathematics | 1967 | **67.73** | 7.32 | 10 | 3 | 6 | 7 | Completely Open | `ai-assisted-editorial-synthesis` |
| 153 | `LOG-055` | **Physical Church–Turing Thesis & Hypercomputation Bounds in Relativistic Spacetimes** | Logic | 1936 | **67.72** | 8.40 | 9 | 3 | 8 | 5 | Completely Open | `ai-assisted-editorial-synthesis` |
| 154 | `BIO-046` | **Biological Mechanisms of Extreme Anhydrobiosis, Cryptobiosis & Radiotolerance (Tardigrades & Bdelloids)** | Life | 1702 | **67.72** | 7.30 | 7 | 9 | 8 | 5 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 155 | `SUB-012` | **Molecular Glass-Transition Mechanism of Anhydrobiosis in Tardigrades & Extremophiles** | Life | 1702 | **67.72** | 7.30 | 7 | 9 | 8 | 5 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 156 | `XALG-016` | **Existence of Infinite Finitely Presented Torsion Groups (Finitely Presented Burnside Problem)** | Pure Mathematics | 1964 | **67.67** | 7.35 | 10 | 3 | 7 | 4 | Completely Open | `primary-registry-indexed` |
| 157 | `ECON-004` | **Dynamics of Extreme Wealth Inequality, AI Labor Displacement & Optimal Distributive Equilibrium** | Philosophy | 1896 | **67.66** | 8.70 | 8 | 7 | 10 | 10 | Experimental Tension / Crisis | `ai-assisted-editorial-synthesis` |
| 158 | `NT-032` | **Beilinson's Conjectures on Special Values of L-Functions** | Pure Mathematics | 1984 | **67.60** | 8.04 | 10 | 3 | 7 | 6 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 159 | `CHEM-003` | **Ambient-Condition Catalytic Nitrogen Fixation (Artificial Nitrogenase)** | Matter | 1913 | **67.57** | 8.64 | 8 | 8 | 10 | 18 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 160 | `GEOM-019` | **Hopf–Chern Sign Conjecture for Euler Characteristic of Positively Curved Manifolds** | Pure Mathematics | 1931 | **67.55** | 6.70 | 10 | 3 | 5 | 5 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 161 | `GEO-003` | **Exact Thresholds & Early Warnings of Planetary Climate Tipping Points (AMOC, Ice Sheets, Permafrost)** | Engineering | 2008 | **67.53** | 9.54 | 9 | 8 | 10 | 34 | Experimental Tension / Crisis | `ai-assisted-editorial-synthesis` |
| 162 | `ANL-065` | **Berry–Tabor and Bohigas–Giannoni–Schmit (BGS) Quantum Chaos Spectral Conjectures** | Pure Mathematics | 1977 | **67.49** | 8.20 | 10 | 3 | 7 | 5 | Partially Solved / Special Cases | `ai-assisted-editorial-synthesis` |
| 163 | `XALG-030` | **Drinfeld–Ihara Conjecture on the Grothendieck–Teichmüller Group (GT̂ ≅ Gal(ℚ̄/ℚ))** | Pure Mathematics | 1990 | **67.44** | 8.30 | 10 | 3 | 8 | 4 | Partially Solved / Special Cases | `ai-assisted-editorial-synthesis` |
| 164 | `NT-054` | **Hilbert's 12th Problem (Explicit Class Field Theory & General Stark Conjectures)** | Pure Mathematics | 1900 | **67.44** | 7.55 | 9 | 5 | 8 | 4 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 165 | `BIO-004` | **Quantitative Genotype-to-Phenotype Mapping & Non-Coding Regulatory Grammar** | Life | 2008 | **67.42** | 9.33 | 9 | 8 | 10 | 33 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 166 | `AI-055` | **Moral Status, Welfare Indicators & Operational Sentience Detection Tests for Frontier Digital Minds** | AI | 2023 | **67.42** | 9.10 | 10 | 3 | 9 | 5 | Completely Open | `ai-assisted-editorial-synthesis` |
| 167 | `COMB-053` | **Combinatorial Interpretation of Kronecker Coefficients (Murnaghan–Stanley Problem)** | Pure Mathematics | 1938 | **67.40** | 7.95 | 10 | 5 | 7 | 4 | Partially Solved / Special Cases | `ai-assisted-editorial-synthesis` |
| 168 | `COMB-056` | **Exact Connective Constant and Scaling Limit of Self-Avoiding Walks on ℤ² and ℤ³** | Pure Mathematics | 1949 | **67.35** | 8.20 | 10 | 5 | 7 | 5 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 169 | `CM-002` | **The Glass Transition & Nature of Amorphous Solids** | Matter | 1948 | **67.33** | 8.04 | 9 | 7 | 7 | 28 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 170 | `CM-001` | **Microscopic Mechanism of High-Temperature Superconductivity (Cuprates & Nickelates)** | Matter | 1986 | **67.24** | 8.70 | 9 | 7 | 9 | 24 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 171 | `HUM-004` | **Deep Language Family Prehistory & Monogenesis vs. Polygenesis Beyond the 10,000-Year Horizon** | Philosophy | 1786 | **67.22** | 6.60 | 8 | 5 | 5 | 5 | Completely Open | `ai-assisted-editorial-synthesis` |
| 172 | `SYS-002` | **Formal Runtime Safety & Zero-Fatality Verification for Learning-Enabled Autonomous Systems** | AI | 2015 | **67.17** | 9.35 | 9 | 8 | 10 | 35 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 173 | `ANL-017` | **Uniqueness of Unforced 3D Leray–Hopf Weak Solutions to Navier–Stokes** | Pure Mathematics | 1934 | **67.17** | 8.10 | 10 | 7 | 8 | 4 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 174 | `COMB-040` | **Hadamard Matrix Conjecture** | Pure Mathematics | 1893 | **67.16** | 7.14 | 9 | 4 | 6 | 6 | Partially Solved / Special Cases | `ai-assisted-editorial-synthesis` |
| 175 | `STAT-001` | **3D Percolation Critical Behavior & Continuous Phase Transition** | Logic | 1957 | **67.12** | 7.23 | 9 | 5 | 5 | 41 | Completely Open | `ai-assisted-editorial-synthesis` |
| 176 | `NT-053` | **Kummer-Vandiver Conjecture** | Pure Mathematics | 1849 | **67.10** | 6.19 | 8 | 3 | 6 | 6 | Completely Open | `primary-registry-indexed` |
| 177 | `NT-050` | **Grothendieck's Section Conjecture (Anabelian Geometry)** | Pure Mathematics | 1983 | **67.09** | 7.80 | 10 | 3 | 7 | 5 | Completely Open | `primary-registry-indexed` |
| 178 | `BIO-005` | **Complete Predictive Whole-Cell Simulation & Rational Minimal-Cell Design** | Life | 2012 | **67.05** | 9.52 | 9 | 8 | 10 | 32 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 179 | `COMB-054` | **Combinatorial Interpretation of Plethysm Coefficients (Stanley's Problem 9)** | Pure Mathematics | 1936 | **67.04** | 7.40 | 10 | 4 | 6 | 4 | Partially Solved / Special Cases | `ai-assisted-editorial-synthesis` |
| 180 | `ANL-019` | **Large-Data Global Regularity and Splash/Wave-Breaking Taxonomy for 3D Water Waves** | Pure Mathematics | 1847 | **66.97** | 7.05 | 9 | 6 | 6 | 4 | Partially Solved / Special Cases | `ai-assisted-editorial-synthesis` |
| 181 | `NEURO-014` | **Neural Basis of Affective Valence (Pleasure vs. Suffering Qualia) & Emotional Feelings** | Life | 1884 | **66.96** | 8.35 | 8 | 7 | 9 | 10 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 182 | `QM-004` | **Electroweak Hierarchy & Naturalness Problem** | Fundamental Physics | 1976 | **66.96** | 8.06 | 9 | 5 | 8 | 16 | Experimental Tension / Crisis | `primary-registry-indexed` |
| 183 | `GEOM-018` | **Hopf Conjecture on Positive Sectional Curvature of S² × S²** | Pure Mathematics | 1931 | **66.87** | 6.65 | 10 | 3 | 5 | 4 | Completely Open | `primary-registry-indexed` |
| 184 | `HUM-017` | **Decipherment & Linguistic Status of the Indus Valley (Harappan) Script** | Philosophy | 1875 | **66.86** | 7.89 | 9 | 7 | 7 | 6 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 185 | `XNT-019` | **Oppermann's Conjecture on Primes Between Squares and Oblongs** | Pure Mathematics | 1882 | **66.82** | 5.95 | 9 | 3 | 5 | 5 | Completely Open | `primary-registry-indexed` |
| 186 | `NT-018` | **Legendre's Conjecture** | Pure Mathematics | 1798 | **66.74** | 5.55 | 8 | 4 | 5 | 4 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 187 | `BIO-024` | **Predicting Cancer Clonal Evolution, Extrachromosomal DNA (ecDNA), Metastatic Awakening & Plasticity** | Life | 1976 | **66.73** | 9.14 | 9 | 8 | 10 | 15 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 188 | `ENR-005` | **Safe Governance, Risk Modeling & Termination-Shock Physics of Solar Radiation Geoengineering** | Engineering | 1974 | **66.71** | 9.20 | 9 | 6 | 10 | 8 | Experimental Tension / Crisis | `ai-assisted-editorial-synthesis` |
| 189 | `GEOM-011` | **Bloch–Beilinson Conjectures on Chow Groups and Motives** | Pure Mathematics | 1982 | **66.65** | 7.25 | 10 | 2 | 6 | 5 | Completely Open | `ai-assisted-editorial-synthesis` |
| 190 | `XANL-022` | **Global Regularity of Large-Data 3D Vlasov–Poisson–Landau Kinetic Equations** | Pure Mathematics | 1936 | **66.54** | 7.75 | 10 | 6 | 7 | 4 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 191 | `CHEM-002` | **Origin of Biological Homochirality (L-Amino Acids & D-Sugars)** | Matter | 1848 | **66.52** | 7.73 | 8 | 8 | 7 | 14 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 192 | `NT-037` | **Boundedness vs. Unboundedness of Elliptic Curve Ranks over Q** | Pure Mathematics | 1922 | **66.47** | 7.00 | 9 | 3 | 7 | 4 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 193 | `GR-040` | **Cosmological Measure Problem in Eternal Inflation & Boltzmann Brain Paradox** | Fundamental Physics | 1993 | **66.42** | 8.00 | 10 | 3 | 7 | 5 | Completely Open | `ai-assisted-editorial-synthesis` |
| 194 | `PHIL-005` | **Digital Minds, Moral Circle Expansion & Ethics of Creating Artificial Sentience** | Philosophy | 2019 | **66.36** | 9.31 | 9 | 5 | 10 | 13 | Experimental Tension / Crisis | `primary-registry-indexed` |
| 195 | `NT-046` | **Fontaine-Mazur Conjecture (Higher Dimension & General Number Fields)** | Pure Mathematics | 1995 | **66.36** | 8.19 | 10 | 5 | 8 | 6 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 196 | `BIO-022` | **Morphogenesis, Developmental Pattern Formation & Bioelectric Anatomical Target Memory** | Life | 1952 | **66.33** | 8.76 | 9 | 8 | 9 | 13 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 197 | `GR-005` | **Non-Perturbative Formulation of M-Theory & 11-Dimensional Microphysics** | Fundamental Physics | 1995 | **66.29** | 8.00 | 10 | 3 | 7 | 5 | Completely Open | `ai-assisted-editorial-synthesis` |
| 198 | `GEOM-034` | **Smooth 4-Dimensional Schoenflies Conjecture** | Pure Mathematics | 1959 | **66.26** | 6.74 | 10 | 3 | 5 | 6 | Completely Open | `primary-registry-indexed` |
| 199 | `QM-036` | **Flavor Puzzle: Three Fermion Generations & Yukawa Mass Hierarchy** | Fundamental Physics | 1936 | **66.24** | 7.00 | 9 | 3 | 6 | 8 | Completely Open | `ai-assisted-editorial-synthesis` |
| 200 | `QC-002` | **The Quantum PCP Conjecture (Macroscopic Room-Temperature Entanglement Hardness)** | AI | 2006 | **66.23** | 8.44 | 10 | 6 | 7 | 15 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 201 | `LOG-024` | **Modern Hilbert's Second Problem: Constructive Consistency Beyond Gentzen** | Logic | 1900 | **66.12** | 6.90 | 9 | 4 | 6 | 5 | Independent / Undecidable Suspected | `primary-registry-indexed` |
| 202 | `XALG-001` | **Existence of Non-Sofic Groups (Gromov–Weiss Problem)** | Pure Mathematics | 1999 | **66.10** | 7.87 | 10 | 4 | 7 | 7 | Completely Open | `primary-registry-indexed` |
| 203 | `NT-009` | **Lindelöf Hypothesis** | Pure Mathematics | 1908 | **66.09** | 7.05 | 9 | 5 | 7 | 5 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 204 | `STAT-025` | **Global Gauge-Invariant 3D & 4D Stochastic Yang–Mills Measure via Langevin Dynamics** | Logic | 1981 | **66.04** | 8.50 | 10 | 5 | 8 | 4 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 205 | `XGEOM-007` | **Gluck Twist Conjecture on Smooth 4-Spheres from Knotted 2-Spheres** | Pure Mathematics | 1962 | **65.97** | 7.10 | 10 | 4 | 7 | 3 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 206 | `XNT-038` | **Infinitude of Wolstenholme Primes** | Pure Mathematics | 1862 | **65.97** | 5.55 | 9 | 3 | 4 | 4 | Completely Open | `ai-assisted-editorial-synthesis` |
| 207 | `CM-027` | **Spin Glass Replica Symmetry Breaking vs. Droplet Picture in Three Dimensions (Edwards–Anderson)** | Matter | 1975 | **65.94** | 8.15 | 10 | 4 | 7 | 4 | Completely Open | `ai-assisted-editorial-synthesis` |
| 208 | `STAT-014` | **Edwards–Anderson 3D Short-Range Spin Glass: RSB vs. Droplet Ground States** | Logic | 1975 | **65.94** | 7.95 | 10 | 4 | 7 | 4 | Completely Open | `ai-assisted-editorial-synthesis` |
| 209 | `CHEM-004` | **Exact Universal Exchange–Correlation Functional in Density Functional Theory (DFT)** | Matter | 1964 | **65.93** | 8.59 | 9 | 5 | 9 | 6 | Completely Open | `primary-registry-indexed` |
| 210 | `ALG-031` | **Baum-Connes Conjecture (Without Coefficients)** | Pure Mathematics | 1982 | **65.93** | 8.15 | 9 | 4 | 8 | 10 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 211 | `AI-051` | **AI-Driven Self-Improvement Stability, Recursive Optimization Limits & Intelligence Explosion Dynamics** | AI | 1965 | **65.79** | 9.10 | 9 | 6 | 10 | 5 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 212 | `STAT-006` | **Random Band Matrix Localization–Delocalization Transition & 3D Anderson Extended States** | Logic | 1958 | **65.75** | 8.20 | 10 | 6 | 7 | 5 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 213 | `NT-010` | **Landau-Siegel Zero Exclusion Conjecture** | Pure Mathematics | 1918 | **65.74** | 7.00 | 9 | 4 | 7 | 4 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 214 | `ECON-002` | **Optimal Collective Social Choice & Post-Arrow Democratic Mechanism Design** | Philosophy | 1951 | **65.73** | 8.50 | 8 | 6 | 9 | 19 | Completely Open | `ai-assisted-editorial-synthesis` |
| 215 | `ARC-002` | **Net-Positive, Regenerative, Affordable High-Density Urban Systems (Science of Cities)** | Engineering | 1961 | **65.69** | 9.12 | 8 | 8 | 10 | 26 | Experimental Tension / Crisis | `ai-assisted-editorial-synthesis` |
| 216 | `HUM-038` | **Counterfactual Causality in Historiography: Structural Forces vs. Individual Contingency** | Philosophy | 1869 | **65.69** | 7.50 | 8 | 4 | 7 | 5 | Completely Open | `ai-assisted-editorial-synthesis` |
| 217 | `CS-012` | **Valiant's Algebraic Complexity Conjecture: VP vs. VNP (Permanent vs. Determinant)** | Logic | 1979 | **65.67** | 7.95 | 10 | 4 | 7 | 4 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 218 | `HUM-002` | **The Symbol Grounding Problem & Formal Theory of Semantic Meaning & Pragmatics** | Philosophy | 1990 | **65.63** | 8.70 | 9 | 6 | 8 | 19 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 219 | `ANL-037` | **Fatou's Hyperbolicity Density Conjecture (Complex Polynomials and Rational Maps)** | Pure Mathematics | 1920 | **65.60** | 6.65 | 10 | 5 | 5 | 4 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 220 | `NT-017` | **Hardy-Littlewood Prime k-Tuples Conjecture** | Pure Mathematics | 1923 | **65.59** | 6.50 | 9 | 3 | 6 | 5 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 221 | `MED-007` | **Complete Functional Spinal Cord Regeneration & Long-Distance CNS Axon Regrowth After Trauma** | Life | 1928 | **65.57** | 8.85 | 9 | 8 | 10 | 4 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 222 | `XALG-017` | **Existence of a Finitely Presented Group of Intermediate Word Growth** | Pure Mathematics | 1984 | **65.52** | 7.05 | 10 | 3 | 6 | 5 | Completely Open | `primary-registry-indexed` |
| 223 | `GEOM-006` | **Resolution of Singularities in Positive Characteristic (dim ≥ 4)** | Pure Mathematics | 1944 | **65.50** | 7.00 | 10 | 5 | 6 | 4 | Partially Solved / Special Cases | `ai-assisted-editorial-synthesis` |
| 224 | `XGEOM-031` | **Existence of an Integrable Complex Structure on the 6-Sphere S^6 (Hopf Problem)** | Pure Mathematics | 1947 | **65.47** | 7.15 | 10 | 4 | 6 | 3 | Completely Open | `ai-assisted-editorial-synthesis` |
| 225 | `NT-085` | **Furstenberg's ×2, ×3 Conjecture** | Pure Mathematics | 1967 | **65.43** | 7.80 | 9 | 4 | 7 | 10 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 226 | `CS-004` | **Matrix Multiplication Exponent (Is ω = 2?)** | Logic | 1969 | **65.42** | 8.19 | 9 | 6 | 8 | 12 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 227 | `PHIL-043` | **Objective Measurement of Subjective Welfare & Interpersonal Utility Comparisons** | Philosophy | 1932 | **65.40** | 8.53 | 8 | 5 | 9 | 9 | Completely Open | `primary-registry-indexed` |
| 228 | `LOG-039` | **Collapse of Bounded Arithmetic (S¹₂ vs. T¹₂) & Polynomial Hierarchy Mirrors** | Logic | 1986 | **65.39** | 7.45 | 10 | 3 | 6 | 5 | Completely Open | `ai-assisted-editorial-synthesis` |
| 229 | `ANL-056` | **Global Arnold Diffusion in Generic Nearly-Integrable Hamiltonian Systems (n ≥ 3 DOF)** | Pure Mathematics | 1964 | **65.35** | 8.00 | 10 | 6 | 7 | 5 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 230 | `NT-072` | **Borel's Conjecture on Normality of Algebraic Irrationals, pi, and e** | Pure Mathematics | 1909 | **65.34** | 6.30 | 9 | 2 | 5 | 4 | Completely Open | `primary-registry-indexed` |
| 231 | `ALG-022` | **Bounded Burnside Problem for Small Exponents (B(2, 5) & B(2, 8))** | Pure Mathematics | 1902 | **65.30** | 6.45 | 9 | 4 | 6 | 4 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 232 | `NEURO-019` | **Extreme Sample Efficiency, Local Credit Assignment & 20-Watt Power Budget of Biological Intelligence** | Life | 1986 | **65.29** | 9.29 | 9 | 8 | 10 | 12 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 233 | `XNT-011` | **Catalan–Dickson Conjecture on Aliquot Sequence Termination** | Pure Mathematics | 1888 | **65.24** | 5.75 | 9 | 2 | 4 | 4 | Completely Open | `ai-assisted-editorial-synthesis` |
| 234 | `FLD-003` | **Multiscale Dynamic Fracture Mechanics & Crack-Branching Instability** | Matter | 1921 | **65.22** | 8.01 | 8 | 8 | 8 | 25 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 235 | `LOG-023` | **Proof-Theoretic Ordinal Analysis of Π¹₂-Comprehension & Full Second-Order Arithmetic** | Logic | 1936 | **65.22** | 6.50 | 10 | 5 | 5 | 5 | Partially Solved / Special Cases | `ai-assisted-editorial-synthesis` |
| 236 | `QM-009` | **Origin of the Born Rule in Deterministic Quantum Interpretations** | Fundamental Physics | 1926 | **65.20** | 7.60 | 9 | 4 | 7 | 4 | Completely Open | `primary-registry-indexed` |
| 237 | `GR-063` | **Unimodular Gravity & Topological Sequestering of Vacuum Energy** | Fundamental Physics | 1919 | **65.17** | 7.75 | 9 | 6 | 8 | 4 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 238 | `GR-045` | **ER = EPR Conjecture: Microscopic Equivalence of Wormholes & Bell Entanglement** | Fundamental Physics | 2013 | **65.16** | 8.59 | 10 | 5 | 8 | 6 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 239 | `ALG-037` | **Period-Index Conjecture for Brauer Groups of Fields (d >= 3)** | Pure Mathematics | 1939 | **65.10** | 7.32 | 9 | 5 | 7 | 7 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 240 | `SUB-049` | **Universal Cognitive & Acoustic Foundations of Musical Consonance, Rhythm & Emotional Valence** | Philosophy | 500 BCE | **65.04** | 6.55 | 7 | 8 | 6 | 4 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 241 | `GR-043` | **Discrete vs. Continuous Spacetime & Generalized Uncertainty Principle (Minimum Length/Time)** | Fundamental Physics | 1947 | **64.99** | 8.00 | 9 | 5 | 8 | 5 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 242 | `MED-003` | **Safe, Controllable Human Biological Age Reversal & Healthspan Extension** | Life | 2006 | **64.95** | 9.09 | 9 | 7 | 10 | 12 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 243 | `MED-030` | **True Curative Eradication of Glioblastoma Multiforme (GBM) & Diffuse Intrinsic Pontine Glioma (DIPG)** | Life | 1926 | **64.89** | 8.55 | 9 | 8 | 9 | 5 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 244 | `ENG-021` | **Hydrogen Embrittlement Prevention in High-Strength Pipeline Steels & Cryogenic Aerospace Alloys** | Engineering | 1875 | **64.86** | 8.04 | 8 | 8 | 9 | 6 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 245 | `ANL-012` | **Vanishing-Viscosity Selection Principle and Uniqueness for Weak Solutions of Incompressible Euler** | Pure Mathematics | 1949 | **64.85** | 8.00 | 9 | 5 | 8 | 5 | Active Breakthroughs / Frontier | `ai-assisted-editorial-synthesis` |
| 246 | `PHIL-052` | **Distributive Justice Foundations: Rawlsian Difference Principle vs. Luck Egalitarianism & Capabilities** | Philosophy | 1971 | **64.80** | 8.33 | 8 | 3 | 9 | 9 | Completely Open | `primary-registry-indexed` |
| 247 | `XCOMB-014` | **Brown–Erdős–Sós Conjecture on Sparse 3-Uniform Hypergraphs (f^{(3)}(n; k+3, k) = o(n^2))** | Pure Mathematics | 1973 | **64.75** | 7.60 | 10 | 6 | 7 | 5 | Active Breakthroughs / Frontier | `primary-registry-indexed` |
| 248 | `SYS-020` | **Self-Reconfiguring Modular Robotics & Autonomous Physical Self-Repair / Self-Replication** | AI | 1948 | **64.74** | 8.50 | 9 | 6 | 9 | 4 | Completely Open | `ai-assisted-editorial-synthesis` |
| 249 | `CS-048` | **Network Information Theory: Exact Multi-User Channel Capacity Regions** | Logic | 1961 | **64.63** | 7.84 | 9 | 5 | 8 | 6 | Partially Solved / Special Cases | `primary-registry-indexed` |
| 250 | `QM-005` | **Matter–Antimatter Asymmetry (Baryogenesis)** | Fundamental Physics | 1967 | **64.57** | 8.13 | 9 | 6 | 8 | 9 | Completely Open | `ai-assisted-editorial-synthesis` |

## Top 5 Flagship Problems per Macro-Pillar

### Pure Mathematics (`n = 514` · Mean CSS `59.90`)

| Pillar Rank | ID | Problem | Superdomain | Posed | CSS | Titan | Verification Flag |
|---:|---|---|---|---:|---:|---:|---|
| 1 | `ANL-001` | **3D Navier–Stokes Existence and Smoothness** | Analysis, Calculus, PDEs & Dynamics | 1822 | **82.98** | 9.31 | `ai-claim-under-audit-nov2026` |
| 2 | `ANL-002` | **3D Incompressible Euler Equations Finite-Time Blowup (Smooth Boundaryless ℝ³)** | Analysis, Calculus, PDEs & Dynamics | 1757 | **82.83** | 8.56 | `primary-registry-indexed` |
| 3 | `GEOM-003` | **Sphere Packing Optimal Density in General Dimensions (d ≠ 1, 2, 3, 8, 24)** | Geometry & Topology | 1611 | **82.07** | 7.45 | `primary-registry-indexed` |
| 4 | `NT-001` | **Riemann Hypothesis** | Number Theory & Arithmetic | 1859 | **81.97** | 9.34 | `ai-claim-under-audit-nov2026` |
| 5 | `SUB-050` | **Exact Classification of Ancient & Modern Diophantine Irrationality Measures (ζ(3), π, e, Catalan G)** | Number Theory & Arithmetic | 450 BCE | **79.54** | 6.65 | `primary-registry-indexed` |

### Logic, Statistics & Computing (`n = 185` · Mean CSS `57.27`)

| Pillar Rank | ID | Problem | Superdomain | Posed | CSS | Titan | Verification Flag |
|---:|---|---|---|---:|---:|---:|---|
| 1 | `CS-001` | **P versus NP Problem** | Computer Science, Complexity, Crypto & Info Theory | 1971 | **81.67** | 10.00 | `primary-registry-indexed` |
| 2 | `CS-002` | **Unconditional Existence of One-Way Functions (Impagliazzo's Five Worlds)** | Computer Science, Complexity, Crypto & Info Theory | 1976 | **79.17** | 9.52 | `ai-assisted-editorial-synthesis` |
| 3 | `CS-009` | **Classical Complexity of Integer Factorization & Discrete Logarithm** | Computer Science, Complexity, Crypto & Info Theory | 1801 | **77.80** | 8.39 | `ai-assisted-editorial-synthesis` |
| 4 | `LOG-001` | **Continuum Hypothesis (CH) & Ultimate Foundations of Set Theory** | Mathematical Logic, Set Theory & Computability | 1878 | **75.76** | 7.66 | `primary-registry-indexed` |
| 5 | `CS-003` | **BQP vs. NP, PH & Exact Boundaries of Quantum Computational Power** | Computer Science, Complexity, Crypto & Info Theory | 1993 | **73.74** | 9.19 | `ai-assisted-editorial-synthesis` |

### Fundamental Physics & Cosmos (`n = 201` · Mean CSS `56.47`)

| Pillar Rank | ID | Problem | Superdomain | Posed | CSS | Titan | Verification Flag |
|---:|---|---|---|---:|---:|---:|---|
| 1 | `GR-001` | **Quantum Gravity (Unification of General Relativity & Quantum Mechanics)** | Spacetime, Gravity, Time, Dimensions & Holography | 1930 | **83.40** | 10.00 | `primary-registry-indexed` |
| 2 | `QM-006` | **Thermodynamic Arrow of Time & Origin of the Past Hypothesis** | Quantum Mechanics, QFT & Particle Physics | 1877 | **81.81** | 9.16 | `ai-assisted-editorial-synthesis` |
| 3 | `QM-001` | **Quantum Measurement Problem & Wavefunction Collapse** | Quantum Mechanics, QFT & Particle Physics | 1927 | **80.20** | 9.59 | `primary-registry-indexed` |
| 4 | `GR-004` | **Dimensionality & Signature of Spacetime (Why 3+1 Dimensions?)** | Spacetime, Gravity, Time, Dimensions & Holography | 1917 | **77.11** | 8.62 | `ai-assisted-editorial-synthesis` |
| 5 | `QM-002` | **Yang–Mills Existence and Mass Gap** | Quantum Mechanics, QFT & Particle Physics | 1954 | **76.16** | 8.72 | `ai-claim-under-audit-nov2026` |

### Matter, Materials & Chemistry (`n = 196` · Mean CSS `55.46`)

| Pillar Rank | ID | Problem | Superdomain | Posed | CSS | Titan | Verification Flag |
|---:|---|---|---|---:|---:|---:|---|
| 1 | `FLD-001` | **Universal Statistical Theory of Fluid Turbulence & Intermittency Closure** | Fluids, Gases, Plasmas & Non-Equilibrium Matter | 1941 | **79.17** | 9.45 | `ai-assisted-editorial-synthesis` |
| 2 | `CM-003` | **Ambient-Pressure Room-Temperature Superconductivity (T_c ≥ 295 K, 1 atm)** | Condensed Matter, Solid-State & Quantum Materials | 1911 | **75.96** | 9.09 | `primary-registry-indexed` |
| 3 | `CM-051` | **Atomic-Scale Tribology: Origin of Macroscopic Friction, Superlubricity & Wear Laws** | Condensed Matter, Solid-State & Quantum Materials | 1699 | **74.80** | 8.04 | `primary-registry-indexed` |
| 4 | `CHEM-001` | **Many-Body Electronic Structure & Exponential Wall of Quantum Chemistry** | Chemistry, Catalysis & Molecular Sciences | 1929 | **74.48** | 9.38 | `ai-assisted-editorial-synthesis` |
| 5 | `FLD-054` | **Universal Variational Principle for Far-From-Equilibrium Steady States (Beyond Minimum Entropy Production)** | Fluids, Gases, Plasmas & Non-Equilibrium Matter | 1945 | **72.53** | 9.23 | `ai-assisted-editorial-synthesis` |

### Life, Mind & Medicine (`n = 224` · Mean CSS `55.97`)

| Pillar Rank | ID | Problem | Superdomain | Posed | CSS | Titan | Verification Flag |
|---:|---|---|---|---:|---:|---:|---|
| 1 | `BIO-001` | **Abiogenesis: Origin of Life & RNA-to-Ribosome Genetic Code Transition** | Biology, Evolution, Origin of Life & Ecology | 1871 | **81.27** | 9.55 | `primary-registry-indexed` |
| 2 | `NEURO-001` | **The Hard Problem of Consciousness (Explanatory Gap & Subjective Qualia)** | Neuroscience, Consciousness & Sentience | 1995 | **78.29** | 9.88 | `ai-assisted-editorial-synthesis` |
| 3 | `BIO-031` | **Mechanisms of Complete Whole-Body & Limb Regeneration (Planaria & Salamanders vs. Mammalian Scarring)** | Biology, Evolution, Origin of Life & Ecology | 1768 | **74.44** | 8.65 | `ai-assisted-editorial-synthesis` |
| 4 | `MED-001` | **Root Cause, Prevention & Curative Reversal of Neurodegenerative Diseases (Alzheimer's, Parkinson's, ALS)** | Medicine, Pharmacology, Longevity & Bioengineering | 1906 | **72.42** | 9.21 | `primary-registry-indexed` |
| 5 | `NEURO-055` | **Biological Root Etiology & Mechanistic Circuit Biotypes of Severe Psychiatric Disorders** | Neuroscience, Consciousness & Sentience | 1899 | **72.09** | 9.09 | `primary-registry-indexed` |

### AI, Quantum Tech, Hardware & Systems (`n = 203` · Mean CSS `55.54`)

| Pillar Rank | ID | Problem | Superdomain | Posed | CSS | Titan | Verification Flag |
|---:|---|---|---|---:|---:|---:|---|
| 1 | `AI-001` | **AI Alignment, Scalable Oversight & Value Specification for Superhuman Agents** | Artificial Intelligence, ML & Digital Simulations | 2001 | **74.77** | 9.94 | `ai-assisted-editorial-synthesis` |
| 2 | `AI-003` | **The Simulation Hypothesis & Empirical Testability of Computational Reality** | Artificial Intelligence, ML & Digital Simulations | 2003 | **72.67** | 9.23 | `primary-registry-indexed` |
| 3 | `AI-002` | **True Out-of-Distribution Causal Reasoning, Continual Lifelong Learning & AGI** | Artificial Intelligence, ML & Digital Simulations | 1950 | **72.08** | 9.38 | `primary-registry-indexed` |
| 4 | `SYS-001` | **High-Dimensional Nonlinear & Stochastic Optimal Control (Breaking Bellman's Curse)** | Systems, Control, Robotics & Cybernetics | 1957 | **71.46** | 9.06 | `primary-registry-indexed` |
| 5 | `AI-004` | **Whole-Brain Emulation (WBE) & High-Fidelity Biological Digital Twins** | Artificial Intelligence, ML & Digital Simulations | 2008 | **71.19** | 9.60 | `primary-registry-indexed` |

### Engineering, Design, Earth & Energy (`n = 202` · Mean CSS `54.64`)

| Pillar Rank | ID | Problem | Superdomain | Posed | CSS | Titan | Verification Flag |
|---:|---|---|---|---:|---:|---:|---|
| 1 | `GEO-001` | **Deterministic Short-Term Earthquake Prediction** | Geology, Geophysics, Earth, Ocean & Climate | 1906 | **76.23** | 9.00 | `primary-registry-indexed` |
| 2 | `ENG-008` | **First-Principles Tribology: Predicting Macroscopic Friction, Wear & Structural Superlubricity** | Mechanical, Aerospace, Structural & Civil Engineering | 1493 | **74.80** | 8.04 | `primary-registry-indexed` |
| 3 | `SUB-046` | **First-Principles Multiscale Law of Dry Friction, Wear & Structural Superlubricity (Tribology)** | Mechanical, Aerospace, Structural & Civil Engineering | 1493 | **74.22** | 8.00 | `ai-assisted-editorial-synthesis` |
| 4 | `ENG-002` | **High-Thrust Non-Chemical Space Propulsion Beyond the Tsiolkovsky Rocket Tyranny** | Mechanical, Aerospace, Structural & Civil Engineering | 1903 | **73.45** | 8.95 | `primary-registry-indexed` |
| 5 | `ENG-001` | **First-Principles Multiscale Prediction of Structural Fatigue, Creep & Stress-Corrosion Failure** | Mechanical, Aerospace, Structural & Civil Engineering | 1860 | **70.78** | 8.36 | `primary-registry-indexed` |

### Philosophy, Social & Humanities (`n = 175` · Mean CSS `59.90`)

| Pillar Rank | ID | Problem | Superdomain | Posed | CSS | Titan | Verification Flag |
|---:|---|---|---|---:|---:|---:|---|
| 1 | `PHIL-004` | **The Is–Ought Gap, Meta-Ethical Moral Realism & Normative Convergence** | Philosophy, Metaphysics, Epistemology & Ethics | 1739 | **92.97** | 9.72 | `primary-registry-indexed` |
| 2 | `PHIL-003` | **Free Will, Determinism, Indeterminism & Moral Responsibility** | Philosophy, Metaphysics, Epistemology & Ethics | 300 BCE | **90.13** | 9.23 | `primary-registry-indexed` |
| 3 | `PHIL-001` | **The Mind–Body Problem & Metaphysics of Mental Causation (Exclusion Problem)** | Philosophy, Metaphysics, Epistemology & Ethics | 1641 | **89.90** | 8.96 | `primary-registry-indexed` |
| 4 | `PHIL-006` | **Why Is There Something Rather Than Nothing? (Ultimate Primordial Existence)** | Philosophy, Metaphysics, Epistemology & Ethics | 1714 | **86.80** | 8.24 | `primary-registry-indexed` |
| 5 | `PHIL-002` | **The Problem of Induction & Goodman's New Riddle ('Grue')** | Philosophy, Metaphysics, Epistemology & Ethics | 1739 | **85.76** | 8.66 | `primary-registry-indexed` |

## November 20, 2026 AI Proof-Claim Watchlist (12 Problems — All Officially Unretired)

| ID | Problem | Superdomain | CSS | Titan | Nov 20, 2026 Audit Summary |
|---|---|---|---:|---:|---|
| `ANL-001` | **3D Navier–Stokes Existence and Smoothness** | Analysis, Calculus, PDEs & Dynamics | 82.98 | 9.31 | HIGH-ALERT NOV 2026 AUDIT: On Sept 8, 2026, OpenAI announced an AI-generated finite-time blowup proof claim produced across ~10,000 parallel reasoning instances over 88 hours. The announcement triggered intense attribution controversy over uncredited human PDE blowup frameworks, a public joint statement by 28 Fields Medalists demanding rigorous peer review and attribution norms, and ongoing Cambridge & King's College London (KCL) Lean-to-prose verification audits inspecting subtle statement-fidelity and analytic-estimate gaps. As of Nov 20, 2026, the Clay Mathematics Institute (CMI) officially lists 3D Navier–Stokes as UNRESOLVED pending formal peer-reviewed publication and the mandatory two-year refereeing window. |
| `NT-001` | **Riemann Hypothesis** | Number Theory & Arithmetic | 81.97 | 9.34 | Nov 20, 2026: Levent Alpöge (Anthropic/Claude) multi-million-line Lean 4 proof compiles in Lean kernel (Andrew Sutherland confirms kernel check); same-day rival human draft by Alessandro Masullo (Stanford); statement fidelity & peer verification pending (Clay CMI officially open) |
| `NT-002` | **Generalized & Grand Riemann Hypotheses (GRH)** | Number Theory & Arithmetic | 76.62 | 8.58 | Nov 20, 2026: Covered by both Levent Alpöge (Anthropic/Claude) Lean 4 proof claim (kernel-compiled by Andrew Sutherland) and Alessandro Masullo's independent Stanford human draft; pending formal fidelity audit & peer verification |
| `QM-002` | **Yang–Mills Existence and Mass Gap** | Quantum Mechanics, QFT & Particle Physics | 76.16 | 8.72 | Fall 2026 AI/LLM constructive QFT proof claims remain unverified by formal proof assistants (Lean 4/Rocq) or peer review; Clay CMI officially lists Yang–Mills as Open |
| `CS-018` | **Fine-Grained Complexity: ETH, SETH & 3SUM Tightness Hypotheses** | Computer Science, Complexity, Crypto & Info Theory | 62.91 | 8.10 | Under active audit (Nov 2026) — Fall 2026 AI-targeted proof claims on 3SUM/ETH fine-grained reductions & bounds currently under skeptical peer verification & formalization audit |
| `NT-023` | **Chowla's Conjecture on Möbius Autocorrelations** | Number Theory & Arithmetic | 61.60 | 7.20 | Sept/Oct 2026: OpenAI preprint claims proof of ordinary 2-point Chowla & binary corrected Elliott theorem via divisor-graph methods; under community peer verification; general k >= 3 remains open |
| `ALG-045` | **Auslander-Reiten Conjecture** | Algebra, Group & Category Theory | 60.62 | 7.05 | Sept/Oct 2026: OpenAI released a Lean 4 counterexample for noncommutative finite-dimensional algebras (under community audit); commutative Noetherian local ring case remains completely open |
| `ALG-010` | **Alperin's Weight Conjecture (AWC)** | Algebra, Group & Category Theory | 60.41 | 7.15 | Oct 2026: OpenAI circulated a manuscript claiming a proof of blockwise Alperin's Weight Conjecture; undergoing independent human verification by representation theorists |
| `CS-017` | **Fine-Grained Complexity: All-Pairs Shortest Paths (APSP) Hypothesis & Sub-Cubic Barrier** | Computer Science, Complexity, Crypto & Info Theory | 59.86 | 7.49 | Under active audit (Nov 2026) — Fall 2026 AI-generated proof claim cataloged at ProofAtlas #243 targeting APSP sub-cubic barriers undergoing independent line-by-line & Lean statement-fidelity audit |
| `ALG-011` | **Donovan's Conjecture on Morita Equivalence of Blocks** | Algebra, Group & Category Theory | 59.29 | 7.05 | Sept/Oct 2026: OpenAI released two manuscripts claiming resolution of Donovan's conjecture over fields and complete DVRs via CFSG; undergoing rigorous human auditing |
| `NT-060` | **Artin's Primitive Root Conjecture** | Number Theory & Arithmetic | 58.32 | 6.35 | Oct 6, 2026: OpenAI (openai/math) preprint claims unconditional quantitative infinitude for admissible bases; under peer verification; exact Artin density formula remains open unconditionally (linked to GRH Nov 2026 claims) |
| `ALG-048` | **Lech's Multiplicity Conjecture** | Algebra, Group & Category Theory | 55.70 | 6.19 | Oct 2026: OpenAI math release (Result Family 194) posted a preprint & Lean formalization claiming full proof across all dimensions and characteristics; human verification ongoing |
