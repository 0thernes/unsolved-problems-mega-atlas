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
ATLAS_VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").exists() else "2.10.0"
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


def _read_varuint(buf: bytes, pos: int) -> tuple[int, int]:
    val, shift = 0, 0
    while True:
        if pos >= len(buf):
            raise AssertionError("Truncated varuint in OpenTimestamps proof")
        byte = buf[pos]
        pos += 1
        val |= (byte & 0x7F) << shift
        if not (byte & 0x80):
            return val, pos
        shift += 7


def _parse_ots_tree(buf: bytes, pos: int, calendars: list[str]) -> int:
    """Strictly parse OpenTimestamps v1 binary operation/attestation tree."""
    while pos < len(buf):
        tag = buf[pos]
        pos += 1
        if tag == 0xFF:  # fork branch
            pos = _parse_ots_tree(buf, pos, calendars)
        elif tag == 0x00:  # attestation leaf
            if pos + 8 > len(buf):
                raise AssertionError("Truncated OTS attestation tag")
            att_tag = buf[pos : pos + 8]
            pos += 8
            att_len, pos = _read_varuint(buf, pos)
            if pos + att_len > len(buf):
                raise AssertionError("Truncated OTS attestation payload")
            payload = buf[pos : pos + att_len]
            pos += att_len
            if att_tag == b"\x83\xdf\xe3\x0d\x2e\xf9\x0c\x8e":  # PendingAttestation
                uri_len, up = _read_varuint(payload, 0)
                uri = payload[up : up + uri_len].decode("utf-8", errors="strict")
                if not uri.startswith("https://"):
                    raise AssertionError(f"Non-HTTPS OTS calendar URI: {uri!r}")
                calendars.append(uri)
            return pos
        elif tag in (0x08, 0x02, 0x03, 0x67):  # unary hash ops (sha256, sha1, ripemd160, keccak256)
            continue
        elif tag in (0xF0, 0xF1):  # append / prepend
            dlen, pos = _read_varuint(buf, pos)
            if pos + dlen > len(buf):
                raise AssertionError("Truncated OTS append/prepend operand")
            pos += dlen
        else:
            raise AssertionError(f"Unknown OTS opcode 0x{tag:02x} at byte {pos - 1}")
    return pos


def verify_timestamps() -> None:
    if not CHECKSUMS_PATH.exists():
        raise FileNotFoundError(f"Missing {CHECKSUMS_PATH}")
    digest = hashlib.sha256(CHECKSUMS_PATH.read_bytes()).digest()
    digest_hex = digest.hex()

    if not TSR_PATH.exists() or TSR_PATH.stat().st_size < 200:
        raise AssertionError(f"Missing or truncated {TSR_PATH.name}")
    tsr_bytes = TSR_PATH.read_bytes()
    if tsr_bytes[0] != 0x30 or digest not in tsr_bytes:
        raise AssertionError(f"{TSR_PATH.name} does not cryptographically bind current CHECKSUMS.sha256 ({digest_hex[:16]}...)")

    # Structural ASN.1 RFC 3161 TimeStampResp check via OpenSSL when available
    ts_verified_asn1 = ""
    try:
        openssl = _find_openssl()
    except FileNotFoundError:
        openssl = ""
    if openssl:
        reply = subprocess.run(
            [openssl, "ts", "-reply", "-in", str(TSR_PATH), "-text"],
            capture_output=True,
            text=True,
            check=False,
        )
        if reply.returncode != 0 or "Status: Granted." not in reply.stdout:
            raise AssertionError(f"OpenSSL RFC 3161 ASN.1 parse failed for {TSR_PATH.name}:\n{reply.stdout}\n{reply.stderr}")
        # Extract hex bytes printed under "Message data:" and compare exact SHA-256
        msg_lines: list[str] = []
        in_msg = False
        for ln in reply.stdout.splitlines():
            if "Message data:" in ln:
                in_msg = True
                continue
            if in_msg:
                if ln.startswith("    ") and " - " in ln:
                    hex_part = ln.strip().split("   ")[0].strip()
                    parts = hex_part.split(" - ", 1)
                    if len(parts) == 2:
                        msg_lines.append(parts[1])
                else:
                    in_msg = False
        parsed_hex = "".join(tok for ln in msg_lines for tok in ln.replace("-", " ").split() if len(tok) == 2).lower()
        if parsed_hex != digest_hex:
            raise AssertionError(f"RFC 3161 ASN.1 Message data ({parsed_hex}) != SHA256(CHECKSUMS.sha256) ({digest_hex})")
        ts_line = next((ln.strip() for ln in reply.stdout.splitlines() if "Time stamp:" in ln), "ASN.1 OK")
        ts_verified_asn1 = f" [{ts_line}]"

    # Full structural OpenTimestamps v1 binary wire-format check (0 trailing bytes)
    if not OTS_PATH.exists() or OTS_PATH.stat().st_size < len(OTS_MAGIC) + 34 + 32:
        raise AssertionError(f"Missing or truncated {OTS_PATH.name}")
    ots_bytes = OTS_PATH.read_bytes()
    expected_prefix = OTS_MAGIC + b"\x01\x08" + digest
    if not ots_bytes.startswith(expected_prefix):
        raise AssertionError(f"{OTS_PATH.name} header/digest does not bind current CHECKSUMS.sha256 ({digest_hex[:16]}...)")
    calendars: list[str] = []
    consumed = _parse_ots_tree(ots_bytes, len(expected_prefix), calendars)
    if consumed != len(ots_bytes):
        raise AssertionError(f"{OTS_PATH.name} has {len(ots_bytes) - consumed} trailing unparsed byte(s)")
    if len(calendars) < 2:
        raise AssertionError(f"{OTS_PATH.name} has fewer than 2 verified calendar attestations: {calendars}")

    print(
        f"PASS: Verified dual cryptographic timestamps for CHECKSUMS.sha256 ({digest_hex[:16]}...): "
        f"{TSR_PATH.name} ({len(tsr_bytes):,} B RFC 3161{ts_verified_asn1}) + "
        f"{OTS_PATH.name} ({len(ots_bytes):,} B OTS v1, {len(calendars)} calendars, 0 trailing bytes)"
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
