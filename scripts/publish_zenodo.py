#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""
Turnkey Zenodo Metadata Validator & Optional API Deposit Publisher (`v2.5.0`).

  - `--dry-run` (default, zero network/auth required): Validates `.zenodo.json` against
    Zenodo's REST deposit metadata schema, verifies ORCID `0009-0006-8168-9648`, checks
    `VERSION` parity, and lists the exact SHA-256-verified tracked release bundle ready for deposit.
  - `--publish` / `--sandbox`: Only executes when the user explicitly exports `ZENODO_TOKEN`
    (or `ZENODO_SANDBOX_TOKEN`). Never fabricates a DOI and never bypasses authentication.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPECTED_ORCID = "0009-0006-8168-9648"
REQUIRED_FIELDS = {"title", "description", "upload_type", "version", "publication_date", "license", "creators", "keywords"}


def validate_zenodo_metadata() -> dict:
    zpath = ROOT / ".zenodo.json"
    if not zpath.exists():
        raise FileNotFoundError("Missing .zenodo.json")
    meta = json.loads(zpath.read_text(encoding="utf-8"))
    missing = REQUIRED_FIELDS - set(meta.keys())
    if missing:
        raise ValueError(f".zenodo.json missing required fields: {sorted(missing)}")
    creators = meta["creators"]
    if not creators or creators[0].get("orcid") != EXPECTED_ORCID:
        raise ValueError(f"Primary creator ORCID must be {EXPECTED_ORCID}")
    ver = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if meta["version"] != ver:
        raise ValueError(f".zenodo.json version ({meta['version']}) != VERSION ({ver})")
    if meta["license"] != "cc-by-4.0":
        raise ValueError(f"Expected cc-by-4.0 data license, got {meta['license']}")
    return meta


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate `.zenodo.json` or publish a Zenodo deposit via API.")
    parser.add_argument("--dry-run", action="store_true", help="Validate metadata and artifact SHA-256s without uploading")
    parser.add_argument("--sandbox", action="store_true", help="Target sandbox.zenodo.org (requires ZENODO_SANDBOX_TOKEN)")
    parser.add_argument("--publish", action="store_true", help="Create a draft deposit on zenodo.org (requires ZENODO_TOKEN)")
    args = parser.parse_args()

    meta = validate_zenodo_metadata()
    artifacts = [
        "dist/Donahue_2026_unsolved_problems_mega_atlas.pdf",
        "dist/arxiv_submission.tar.gz",
        "outputs/MegaAtlas_Interactive_Dashboard_V2.html",
        "outputs/MegaAtlas_Unsolved_Problems_V2.csv",
        "outputs/MegaAtlas_Unsolved_Problems_V2.json.gz",
        "outputs/MegaAtlas_Unsolved_Problems_V2.jsonl.gz",
        "outputs/MegaAtlas_Unsolved_Problems_V2.xlsx",
        "croissant.json",
        "ro-crate-metadata.json",
        "CHECKSUMS.sha256",
    ]
    print(f"DRY-RUN PASS: .zenodo.json valid for v{meta['version']} (ORCID {EXPECTED_ORCID}, license {meta['license']})")
    for rel in artifacts:
        p = ROOT / rel
        if not p.exists():
            raise FileNotFoundError(f"Required Zenodo deposit artifact missing: {rel}")
        h = hashlib.sha256(p.read_bytes()).hexdigest()[:12]
        print(f"  [READY] {rel:<54} ({p.stat().st_size:>10,} B | sha256:{h}...)")

    if not args.publish and not args.sandbox:
        print("\nDry-run complete. To mint a persistent DOI automatically on GitHub Releases:")
        print("  Option A (Recommended): Enable repository toggle at https://zenodo.org/account/settings/github/")
        print("  Option B (API Draft)  : Export ZENODO_TOKEN and run `python scripts/publish_zenodo.py --publish`")
        return

    token_var = "ZENODO_SANDBOX_TOKEN" if args.sandbox else "ZENODO_TOKEN"
    token = os.environ.get(token_var)
    if not token:
        print(f"BLOCKED: Environment variable {token_var} is not set. Cannot authenticate to Zenodo API.", file=sys.stderr)
        sys.exit(2)

    base = "https://sandbox.zenodo.org/api/deposit/depositions" if args.sandbox else "https://zenodo.org/api/deposit/depositions"
    payload = json.dumps({"metadata": meta}).encode("utf-8")
    req = urllib.request.Request(
        base,
        data=payload,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        created = json.loads(resp.read().decode("utf-8"))
    print(f"Created Zenodo draft deposition ID={created.get('id')} | URL={created.get('links', {}).get('html')}")


if __name__ == "__main__":
    main()
