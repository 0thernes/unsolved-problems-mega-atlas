# Operations, Deployment, Backup & Restore Runbook

Per **Build Standard for LLMs v1.2.0 (A35, A36)**, this runbook documents how the static web atlas, Lean Proof Blueprint, release artifacts, and offsite git backups are deployed, rolled back, backed up, and verified.

## 1. Deployment (GitHub Pages & Releases)

- **Live Web Atlas & Lean Proof Blueprint:** Automatically deployed on every push to `main` via `.github/workflows/pages.yml` to `https://0thernes.github.io/unsolved-problems-mega-atlas/` (serving `outputs/MegaAtlas_Interactive_Dashboard_V2.html` as `index.html`, all 30 files in `outputs/charts/`, `blueprint/index.html`, `llms.txt`, `llms-full.txt`, `croissant.json`, and `ro-crate-metadata.json`).
- **Release Bundles:** Pushing an annotated or lightweight tag `v*` triggers `.github/workflows/release.yml`, packaging deterministic archives and attaching verified build outputs alongside `SHA256SUMS`.

## 2. Rollback Procedure

1. Identify the last known-good release tag (e.g., `v2.3.0`) via `git tag -l`.
2. To roll back `main` cleanly without rewriting history:
   ```bash
   git revert --no-commit <bad-commit>..HEAD
   git commit -m "revert: roll back to verified state"
   git push origin main
   ```
3. `.github/workflows/pages.yml` automatically redeploys the reverted static site within ~60 seconds.
4. For release downloads, previous GitHub Release assets (`v2.3.0`, `v2.2.0`, `v2.1.0`) remain permanently immutable and downloadable.

## 3. Offsite Backup & Tested Restore Procedure (A35)

Because `git` history + source modules deterministically regenerate every derived artifact (`just reproduce`), our backup strategy maintains **three independent copies**:
1. **Local ReFS Dev Drive working repo:** `Z:\unsolved-problems-mega-atlas`
2. **GitHub remote + pinned master archive submodule:** `https://github.com/0thernes/unsolved-problems-mega-atlas` and `https://github.com/0thernes/0thernes-research-archive` (`0TH-BUILD-007`)
3. **Periodic portable git bundle backup** created via:
   ```bash
   git bundle create <offsite-dir>/unsolved-problems-mega-atlas-v2.4.0.bundle --all
   ```

### Tested Restore Verification Log

| Date (UTC) | Backup Artifact | Restore Command Tested | Verification Check | Result |
|---|---|---|---|---|
| 2026-11-25 | Local `git bundle` (`--all`) + clean clone into isolated temp directory | `git clone <bundle> <restore-dir> && python scripts/audit_atlas.py` | Verified `HEAD` commit parity, `1,900` problems, `5,808` edges, `92` Lean theorems, `sha256` manifest, and `pytest` green | **PASS** (recorded in `REPLICATION.md`) |
