#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Regenerate byte-exact CHECKSUMS.sha256 for all frozen Unsolved Problems Mega-Atlas artifacts."""

from audit_atlas import sync_checksums


if __name__ == "__main__":
    sync_checksums()
