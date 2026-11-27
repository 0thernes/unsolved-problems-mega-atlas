# Operations, Deployment, Backup & Restore Runbook

Per **Build Standard for LLMs v1.2.0 (A35, A36)**, this runbook documents how the static web atlas, Lean Proof Blueprint, release artifacts, and offsite git backups are deployed, rolled back, backed up, and verified.

## 1. Deployment (GitHub Pages & Releases)

- **Live Web Atlas, Left to Solve 62k Mirror, Daily Registry Feeds & Lean Proof Blueprint:** Automatically deployed on every push to `main` AND daily at `06:15 UTC` via `.github/workflows/pages.yml` to `https://0thernes.github.io/unsolved-problems-mega-atlas/` (serving `outputs/MegaAtlas_Interactive_Dashboard_V2.html` as `index.html`, all 30 files in `outputs/charts/`, `blueprint/index.html`, `external/lefttosolve/index.html` (`62,790`-target mirror across `26` live fronts & `291` crosswalk matches), live daily JSON feeds `daily_registries.json`, `lefttosolve_programs.json`, `daily_registry_history.jsonl`, plus `llms.txt`, `llms-full.txt`, `croissant.json`, and `ro-crate-metadata.json`).
- **Automated Daily External Registry Sync:** `.github/workflows/daily-registry-sync.yml` runs daily at `06:00 UTC` (`cron: "0 6 * * *"` + `workflow_dispatch`), polling all **16** live open-problem trackers and all live Left to Solve fronts (`lefttosolve.com/programs`), verifying the full `pytest tests/` suite before writing `data/external/lefttosolve/`, `results/daily_registries.json`, `results/lefttosolve_programs.json`, `results/daily_registry_history.jsonl`, `docs/lefttosolve-programs.md`, and `docs/DAILY_REGISTRY_TRACKER.md` straight to `main` strictly outside frozen `CHECKSUMS.sha256` timestamps.
- **Release Bundles:** Pushing an annotated or lightweight tag `v*` triggers `.github/workflows/release.yml`, packaging deterministic archives and attaching verified build outputs (including `build/MegaAtlas_Unsolved_Problems_V2_Legacy.xls` and daily JSON feeds) alongside `SHA256SUMS`.

## 2. Rollback Procedure

1. Identify the last known-good release tag (e.g., `v2.10.0`) via `git tag -l`.
2. To roll back `main` cleanly without rewriting history:
   ```bash
   git revert --no-commit <bad-commit>..HEAD
   git commit -m "revert: roll back to verified state"
   git push origin main
   ```
3. `.github/workflows/pages.yml` automatically redeploys the reverted static site within ~60 seconds.
4. For release downloads, previous GitHub Release assets (`v2.10.0`, `v2.9.0`, `v2.8.0`, `v2.7.0`, `v2.6.0`, `v2.5.0`, `v2.4.0`, `v2.3.1`, `v2.3.0`) remain permanently immutable and downloadable.

## 3. Offsite Backup & Tested Restore Procedure (A35)

Because `git` history + source modules deterministically regenerate every derived artifact (`just reproduce`), our backup strategy maintains **three independent copies**:
1. **Local workstation working copy:** `<local-workspace>/unsolved-problems-mega-atlas`
2. **GitHub remote + pinned master archive submodule:** `https://github.com/0thernes/unsolved-problems-mega-atlas` and `https://github.com/0thernes/0thernes-research-archive` (`0TH-BUILD-007`)
3. **Periodic portable git bundle backup** created via:
   ```bash
   git bundle create <offsite-dir>/unsolved-problems-mega-atlas-v2.11.0.bundle --all
   ```

### Tested Restore Verification Log

| Date (UTC) | Backup Artifact | Restore Command Tested | Verification Check | Result |
|---|---|---|---|---|
| 2026-11-25 | Local `git bundle` (`--all`) + clean clone into isolated temp directory (`v2.4.0`) | `git clone <bundle> <restore-dir> && python scripts/audit_atlas.py` | Verified `HEAD` commit parity, `1,900` problems, `5,808` edges, `92` Lean theorems, `sha256` manifest, and `pytest` green | **PASS** (recorded in `REPLICATION.md`) |
| 2026-11-26 | Local `git bundle` (`--all`) + clean clone into isolated temp directory (`v2.5.0` & `v2.6.0`) | `git clone <bundle> <restore-dir> && python scripts/audit_atlas.py --check-lean && pytest tests/ -v` | Verified `HEAD` parity, `1,900` problems, `5,808` edges, `103` Lean theorems + live negative rejection, `CHECKSUMS.sha256` + RFC 3161 `.tsr`, `6/6` mutants, and `pytest` 100% green | **PASS** (recorded in `REPLICATION.md`) |
| 2026-11-27 | Local `git bundle` (`--all`) + clean clone into isolated temp directory (`v2.9.0`, `7b75aaf`) | `git clone <bundle> <restore-dir> && python scripts/stamp_timestamps.py --verify && python scripts/audit_atlas.py --check-lean && pytest tests/ -q` | Verified `HEAD` parity, `78/78` SHA-256 checksums + dual `.tsr`/`.ots`, `2,000` problems, `6,108` edges, `103` Lean theorems + live negative rejection, `10/10` mutants, `AQS=98.35`, `11`-page PDF (`0` overfull), `Audit-Repo.ps1` `100.0%`, and `83/83` `pytest` green | **PASS** (recorded in `REPLICATION.md`) |
| 2026-11-27 | Local `git bundle` (`--all`) + clean clone into isolated temp directory (`v2.10.0`, `54948ad`) | `git clone <bundle> <restore-dir> && python scripts/stamp_timestamps.py --verify && python scripts/audit_atlas.py --check-lean && pytest tests/ -q` | Verified `HEAD` parity, `78/78` SHA-256 checksums + dual `.tsr`/`.ots`, `2,000` problems, `6,108` edges, `100/100` verbatim LTS mirror parity (`290` crosswalk matches), `103` Lean theorems + live negative rejection, `12/12` mutants, `AQS=98.35`, `11`-page PDF (`0` overfull), `Audit-Repo.ps1` `98.6%` (`72/73`, sole FAIL `A23` declared in `DEVIATIONS.md`), and `99/99` `pytest` green | **PASS** (recorded in `REPLICATION.md`) |
| 2026-11-27 | Local `git bundle` (`--all`) + clean clone into isolated temp directory (`v2.11.0`, `f2ed786`) | `git clone <bundle> <restore-dir> && python scripts/stamp_timestamps.py --verify && python scripts/audit_atlas.py --check-lean && pytest tests/ -q` | Verified `HEAD` parity, `78/78` SHA-256 checksums + dual `.tsr` (`Nov 27 19:08:34 2026 GMT`)/`.ots`, `2,000` problems, `6,108` edges, `62,790`-target / `26`-front mirror (`291` crosswalk matches), `103` Lean theorems + live negative rejection, `AQS=98.35`, `Audit-Repo.ps1` `98.6%` (`72/73`, sole FAIL `A23` declared in `DEVIATIONS.md`), and **`115/115`** `pytest` green in `69.81s` | **PASS** (recorded in `REPLICATION.md`) |
