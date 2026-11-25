# Operations, Backups & Offsite Mirror (`docs/operations.md`)

## 1. Cryptographic Integrity & Manifests

All 54+ frozen artifacts across `outputs/`, charts, schemas, and FAIR metadata are tracked in both `CHECKSUMS.sha256` and `data/MANIFEST.sha256`. Sync and verify via:

```bash
python3 scripts/generate_fair_metadata.py
python3 scripts/audit_atlas.py --sync-checksums
```

Every `v*` tag triggers `.github/workflows/release.yml`, generating `SHA256SUMS`, Sigstore SLSA build-provenance attestations (`actions/attest-build-provenance@v2`), and a GitHub Release.

## 2. Offline Git Bundle Backup

Create and verify a complete single-file archival backup of all branches and tags:

```bash
git bundle create unsolved-problems-mega-atlas-$(cat VERSION).bundle --all
git bundle verify unsolved-problems-mega-atlas-$(cat VERSION).bundle
sha256sum unsolved-problems-mega-atlas-$(cat VERSION).bundle
```

## 3. Offsite Mirrors & Archival Preservation

- **Master Research Archive mirror:** Pinned as submodule `0TH-BUILD-007` in [`0thernes/0thernes-research-archive`](https://github.com/0thernes/0thernes-research-archive).
- **Zenodo & Software Heritage:** Offline dry-run manifest verified via `python3 scripts/publish_zenodo.py --dry-run`; see [`docs/PRESERVATION.md`](PRESERVATION.md) for Zenodo deposition and Software Heritage (`swh:1:rev:`) preservation instructions.
- **Secondary Git remote mirror:** `git remote add mirror <url> && git push --mirror mirror`.
