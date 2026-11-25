# Philosophy & Epistemic Ethic

> *Why this Mega-Atlas exists, what it refuses to claim, and the verification discipline that governs a solo human + AI-assisted research instrument.*

## The Premise

Humanity's unsolved problems live in isolated silos. Number theorists track `ProofAtlas.ai` and `erdosproblems.com`; topologists consult Kirby's list; physicists monitor cosmological tensions; engineers track NAE Grand Challenges and DOE Earthshots; philosophers debate PhilPapers apories. Yet the deepest bottlenecks of the 21st century—quantum gravity, fluid turbulence, abiogenesis, consciousness, AI alignment, post-Moore compute, climate tipping points—**do not respect departmental walls**.

This Mega-Atlas maps **1,855 unsolved, open, and hard problems** across **all 8 Macro-Pillars and 28 Superdomains of human knowledge** into **one connected 5,597-edge graph**, while holding strictly to the institutional standards of **Independent Researcher (0thernes)** (matching its sibling pure-mathematics deep-dive atlas, [`0thernes/unsolved-mathematics`](https://github.com/0thernes/unsolved-mathematics)).

## Five Non-Negotiable Principles

### 1. Honesty Over Hype (Especially in November 2026)
Fall–November 2026 brought an unprecedented surge of frontier AI mathematical proof claims (OpenAI's Sept 8 Navier–Stokes blowup claim, Oct 6 722-manuscript bulk release, and Nov 20 Alpöge/Claude multi-million-line Lean 4 Riemann Hypothesis & GRH archive alongside Stanford's Masullo draft). Our policy is absolute:
- **No problem is retired as "solved" until independent human fidelity auditing and community consensus settle it.** All 12 AI-claimed problems carry `verification_flag = "ai-claim-under-audit-nov2026"` and remain officially open.
- **No editorial score is disguised as objective physics or peer review.** Every record carries an explicit `verification_flag` and transparent scoring formula.
- **No formal proof scope is ever inflated.** Our 46 Pure Lean 4.35.0 theorems verify mathematical invariants of the *atlas's own scoring, quadrant, taxonomy, and graph equations*—not solutions to any of the 1,855 open problems.

### 2. Solo Human + AI-Assisted Means *Stricter* Verification, Not Looser
Working as an independent solo researcher with AI assistance removes institutional gatekeeping—which means we must **build our own adversarial guardrails directly into the repository**:
- Formal JSON Schema Draft 2020-12 validation on all 1,855 records,
- Pure Lean 4.35.0 machine-checked invariants (`zero sorry`, `zero native_decide`, strictly constructive `[propext, Quot.sound]` axioms),
- Automated `pytest` regression tests + cross-format parity checks (CSV, TSV, JSON, JSONL, SQLite+FTS5, XLSX, XLS),
- Byte-exact SHA-256 cryptographic checksums (`CHECKSUMS.sha256`) enforced on every GitHub Actions CI push.

### 3. Structure Reveals Hidden Coupling
Forcing 1,855 problems across mathematics, physics, biology, neuroscience, AI, engineering, design, and philosophy into a single typed schema exposes structural truths invisible inside any single discipline: **34.6% of all knowledge-graph couplings cross superdomains** and **17.6% cross entire Macro-Pillars**, unifying all 1,855 problems into **1 single connected component**.

### 4. Dual-Audience Infrastructure (Humans + Offline AI/RAG)
Humans inspect charts, side-by-side comparators, PDF monographs, and `RANKING.md`. Research agents and pipelines query structured schemas, JSONL streams, and our zero-API **SQLite FTS5 BM25 + graph-hop RAG engine** (`rag/query.py`)—always returning exact Problem IDs, formulas, and provenance flags rather than ungrounded prose.

### 5. Every Ranking Is a Falsifiable Argument
Ordering 1,855 questions across all human inquiry is inherently contestable. Both our **0thernes Composite Severity Score (`CSS`, 0–100)** and **Composite Titan Index (0–10)** are deterministic, transparent functions of committed source modules. Disagree with where a problem sits? Edit its attributes in `src/v2_data/`, run `python src/v2_export_all.py`, verify via `pytest`, and argue from the git diff.

## What This Atlas Is Not
- It is **not** a claim to have proved or solved any open problem.
- It is **not** human-peer-reviewed consensus (until external specialists formally review entries via [`docs/ACADEMIC_REVIEW.md`](docs/ACADEMIC_REVIEW.md)).
- It is **not** a static encyclopedia—it is a reproducible, cryptographically audited, version-controlled scientific instrument.
