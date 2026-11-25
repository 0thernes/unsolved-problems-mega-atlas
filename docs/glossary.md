# Glossary (`docs/glossary.md`)

- **0thernes Composite Severity Score (`CSS`, 0–100):** Weighted severity index combining editorial difficulty, civilizational impact, interdisciplinarity, historical longevity (capped at 300 years), and inverse tractability; formally bounded in `MegaAtlasProofs.Scoring`.
- **Composite Titan Index (0.90–10.00):** Secondary multi-factor ranking index contrasting against `CSS` via the `css_titan_margin`.
- **Hardness–Tractability Gradient (`D − T ∈ [-9, +9]`):** Difference between `difficulty_score` and `tractability_2050`.
- **Biconnected Connectome:** Undirected dependency graph with `1` connected component, `0` articulation points, and `0` bridges (`1,900` nodes, `5,808` edges).
- **Atlas Quality Score (`AQS`):** Immutable 5-axis composite quality metric evaluated by `autoresearch/evaluate.py` (`97.99` with `100.0% MRR@5`).
- **Ten Finding Classes (Build Standard `R7`):**
  - `bug`: defect in program logic vs. spec.
  - `error`: wrong number, claim, doc, config, version, build, or command.
  - `issue`: works and is not wrong, but unclear, inconsistent, or fragile.
  - `problem`: external obstacle (network, account, toolchain, entity status).
  - `concern`: risk that has not caused harm yet.
  - `dilemma`: trade-off between valid options; owner decides.
  - `conflict`: two requirements or rules contradict each other.
  - `gap`: something required or expected is missing.
  - `hole`: missing check or safeguard allowing defects to pass unnoticed.
  - `blindspot`: unexamined user, platform, failure mode, or assumption.
