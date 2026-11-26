# Long-Term Scholarly Preservation & Archival Playbook (`Options 1, 2, 3`)

**Author:** Alexander Stephen Donahue (`Independent Researcher, Spokane, WA, USA`, ORCID [`0009-0006-8168-9648`](https://orcid.org/0009-0006-8168-9648))  
**Canonical Repository:** https://github.com/0thernes/unsolved-problems-mega-atlas  
**Master Research Archive:** `0TH-BUILD-007` in https://github.com/0thernes/0thernes-research-archive

---

## Option 1 — Zenodo Persistent DOI Auto-Minting (Turnkey Ready)

- **Metadata Status:** [`.zenodo.json`](../.zenodo.json) is committed, schema-validated via `python scripts/publish_zenodo.py --dry-run` and `pytest`, and synchronized with `VERSION`, `CITATION.cff`, `croissant.json`, and `ro-crate-metadata.json`.
- **Automated Publication Paths (No Fabricated DOIs):**
  1. **Zero-CLI GitHub–Zenodo Webhook (Recommended):** Sign in at [https://zenodo.org/account/settings/github/](https://zenodo.org/account/settings/github/) and flip the toggle for `0thernes/unsolved-problems-mega-atlas`. Every subsequent GitHub Release automatically archives the repo tarball and mints a persistent Concept + Version DOI linked to ORCID `0009-0006-8168-9648`.
  2. **API Draft Upload:** Export `ZENODO_TOKEN` in your shell and run `python scripts/publish_zenodo.py --publish` (or `--sandbox` with `ZENODO_SANDBOX_TOKEN`).

## Option 2 — Software Heritage Permanent SWHID Preservation

- **Why Automated API Submission Is Blocked:** Software Heritage gates `POST /api/1/origin/save/git/url/...` behind an **Anubis Proof-of-Work anti-bot challenge**. Per strict integrity and safety rules, we **never** solve or bypass anti-bot/PoW gates programmatically.
- **One-Click Manual Browser Submission:** Open the pre-filled Save Code Now URL in any normal browser session:
  - [https://archive.softwareheritage.org/save/#origin_url=https://github.com/0thernes/unsolved-problems-mega-atlas](https://archive.softwareheritage.org/save/#origin_url=https://github.com/0thernes/unsolved-problems-mega-atlas)
- Once ingested, record the minted `swh:1:rev:...` SWHID in `EVIDENCE.md` and `0thernes-research-archive`.

## Option 3 — Autonomous Research Loops (`autoresearch/` Track A & Track B)

- **Track A (Infrastructure, Retrieval, Graph Resilience & Formal Invariants):** Executed and empirically logged in [`autoresearch/results.tsv`](../autoresearch/results.tsv) (`baseline 80.26` → `H-001 discard` → `H-001b keep 81.93` → `H-002 keep 95.59` → `H-003/H-004 v2.3.0`).
- **Track B (Open-Problem Frontier Exploration & Adversarial Falsification):** First reproducible pilot live under [`research/runs/LOG-002_antihydra_pilot/`](../research/runs/LOG-002_antihydra_pilot/README.md), analyzing the exact big-integer Antihydra Collatz-like dynamics governing Busy Beaver `BB(6)` with explicit negative/honest verification boundaries.
