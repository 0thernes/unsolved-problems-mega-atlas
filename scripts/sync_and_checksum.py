#!/usr/bin/env python3
"""Regenerate byte-exact CHECKSUMS.sha256 for all frozen Unsolved Problems Mega-Atlas artifacts."""

from audit_atlas import sync_checksums


if __name__ == "__main__":
    sync_checksums()
