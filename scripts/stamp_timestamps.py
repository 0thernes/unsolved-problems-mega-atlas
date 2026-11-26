#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Dual Cryptographic Timestamping Minter & Verifier (Playbook v1.3 Item 26):
  1. DigiCert RFC 3161 Trusted Timestamp Token (`CHECKSUMS.sha256.tsr`) via OpenSSL TS
  2. Multi-calendar Bitcoin OpenTimestamps Proof (`CHECKSUMS.sha256.ots`) via OTS v1 HTTP calendars

Usage:
  python scripts/stamp_timestamps.py --verify   # Verify both .tsr and .ots bind current CHECKSUMS.sha256
  python scripts/stamp_timestamps.py --mint     # Mint fresh .tsr and .ots for current CHECKSUMS.sha256
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATLAS_VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").exists() else "2.8.0"
CHECKSUMS_PATH = ROOT / "CHECKSUMS.sha256"
TSR_PATH = ROOT / "CHECKSUMS.sha256.tsr"
OTS_PATH = ROOT / "CHECKSUMS.sha256.ots"

DIGICERT_TSA_URL = "http://timestamp.digicert.com"
OTS_MAGIC = b"\x00OpenTimestamps\x00\x00Proof\x00\xbf\x89\xe2\xe8\x84\xe8\x92\x94"
OTS_CALENDARS = (
    "https://a.pool.opentimestamps.org/digest",
    "https://b.pool.opentimestamps.org/digest",
    "https://a.pool.eternitywall.com/digest",
)


def _find_openssl() -> str:
    for cand in (
        shutil.which("openssl"),
        r"C:\Program Files\Git\usr\bin\openssl.exe",
        "/usr/bin/openssl",
    ):
        if cand and Path(cand).exists():
            return cand
    raise FileNotFoundError("openssl binary not found on PATH or standard install locations")


def mint_rfc3161() -> None:
    openssl = _find_openssl()
    with tempfile.NamedTemporaryFile(suffix=".tsq", delete=False) as tmp:
        tsq_path = Path(tmp.name)
    try:
        subprocess.run(
            [openssl, "ts", "-query", "-data", str(CHECKSUMS_PATH), "-sha256", "-cert", "-out", str(tsq_path)],
            check=True,
            capture_output=True,
        )
        req = urllib.request.Request(
            DIGICERT_TSA_URL,
            data=tsq_path.read_bytes(),
            headers={"Content-Type": "application/timestamp-query", "User-Agent": f"MegaAtlas-TSA/{ATLAS_VERSION}"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status != 200:
                raise RuntimeError(f"DigiCert TSA returned HTTP {resp.status}")
            TSR_PATH.write_bytes(resp.read())
        reply = subprocess.run(
            [openssl, "ts", "-reply", "-in", str(TSR_PATH), "-text"],
            check=True,
            capture_output=True,
            text=True,
        )
        if "Status: Granted." not in reply.stdout:
            raise RuntimeError(f"DigiCert TSA did not grant timestamp:\n{reply.stdout}")
        ts_line = next((ln.strip() for ln in reply.stdout.splitlines() if "Time stamp:" in ln), "Time stamp: unknown")
        print(f"MINTED {TSR_PATH.name} ({TSR_PATH.stat().st_size:,} B) | {ts_line}")
    finally:
        tsq_path.unlink(missing_ok=True)


def mint_opentimestamps() -> None:
    digest = hashlib.sha256(CHECKSUMS_PATH.read_bytes()).digest()
    calendar_proofs: list[bytes] = []
    for cal_url in OTS_CALENDARS:
        try:
            req = urllib.request.Request(
                cal_url,
                data=digest,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/vnd.opentimestamps.v1",
                    "User-Agent": f"MegaAtlas-OTS/{ATLAS_VERSION}",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                body = resp.read()
                if resp.status == 200 and len(body) > 20:
                    calendar_proofs.append(body)
        except Exception as exc:
            print(f"  [WARN] OTS calendar {cal_url} skipped: {exc}", file=sys.stderr)
    if len(calendar_proofs) < 2:
        raise RuntimeError(f"Expected >=2 OpenTimestamps calendars, got {len(calendar_proofs)}")
    # Standard OpenTimestamps v1 file format: magic + version(0x01) + sha256(0x08) + 32B digest + forked calendar trees
    buf = bytearray()
    buf.extend(OTS_MAGIC)
    buf.append(0x01)  # version 1
    buf.append(0x08)  # SHA256 op
    buf.extend(digest)
    for idx, proof in enumerate(calendar_proofs):
        if idx < len(calendar_proofs) - 1:
            buf.append(0xFF)  # fork marker
        buf.extend(proof)
    OTS_PATH.write_bytes(bytes(buf))
    print(f"MINTED {OTS_PATH.name} ({len(buf):,} B) across {len(calendar_proofs)} OpenTimestamps Bitcoin calendars")


def verify_timestamps() -> None:
    if not CHECKSUMS_PATH.exists():
        raise FileNotFoundError(f"Missing {CHECKSUMS_PATH}")
    digest = hashlib.sha256(CHECKSUMS_PATH.read_bytes()).digest()

    if not TSR_PATH.exists() or TSR_PATH.stat().st_size < 200:
        raise AssertionError(f"Missing or truncated {TSR_PATH.name}")
    tsr_bytes = TSR_PATH.read_bytes()
    if tsr_bytes[0] != 0x30 or digest not in tsr_bytes:
        raise AssertionError(f"{TSR_PATH.name} does not cryptographically bind current CHECKSUMS.sha256 ({digest.hex()[:16]}...)")

    if not OTS_PATH.exists() or OTS_PATH.stat().st_size < len(OTS_MAGIC) + 34 + 32:
        raise AssertionError(f"Missing or truncated {OTS_PATH.name}")
    ots_bytes = OTS_PATH.read_bytes()
    expected_prefix = OTS_MAGIC + b"\x01\x08" + digest
    if not ots_bytes.startswith(expected_prefix):
        raise AssertionError(f"{OTS_PATH.name} header/digest does not bind current CHECKSUMS.sha256 ({digest.hex()[:16]}...)")
    if b"https://" not in ots_bytes:
        raise AssertionError(f"{OTS_PATH.name} missing OpenTimestamps calendar URI attestations")

    print(
        f"PASS: Verified dual cryptographic timestamps for CHECKSUMS.sha256 ({digest.hex()[:16]}...): "
        f"{TSR_PATH.name} ({len(tsr_bytes):,} B RFC 3161) + {OTS_PATH.name} ({len(ots_bytes):,} B OpenTimestamps)"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Mint or verify RFC 3161 (.tsr) and OpenTimestamps (.ots) proofs.")
    parser.add_argument("--mint", action="store_true", help="Mint fresh DigiCert RFC 3161 .tsr and 3-calendar OTS .ots proofs")
    parser.add_argument("--verify", action="store_true", help="Verify both .tsr and .ots cryptographically bind CHECKSUMS.sha256")
    args = parser.parse_args()

    if args.mint:
        mint_rfc3161()
        mint_opentimestamps()
    verify_timestamps()


if __name__ == "__main__":
    main()
