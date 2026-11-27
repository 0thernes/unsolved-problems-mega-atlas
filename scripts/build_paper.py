#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Alexander Stephen Donahue
"""Compile `paper/main.tex` via Tectonic, audit for zero overfull hboxes / undefined refs,
copy frozen PDF to `dist/Donahue_2026_unsolved_problems_mega_atlas.pdf`, package deterministic
`dist/arxiv_submission.tar.gz`, and verify clean-room arXiv compilation."""

from __future__ import annotations

import gzip
import io
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPER_DIR = ROOT / "paper"
DIST_DIR = ROOT / "dist"


def find_tectonic() -> str:
    env_bin = os.environ.get("TECTONIC_BIN")
    if env_bin and Path(env_bin).exists():
        return env_bin
    for cand in [
        shutil.which("tectonic"),
        str(Path.home() / ".local" / "bin" / ("tectonic.exe" if sys.platform == "win32" else "tectonic")),
    ]:
        if cand and Path(cand).exists():
            return cand
    raise FileNotFoundError("tectonic not found on PATH or ~/.local/bin")


def main() -> None:
    tectonic = find_tectonic()
    build_dir = PAPER_DIR / "build"
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True, exist_ok=True)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    res = subprocess.run(
        [tectonic, "-X", "compile", "main.tex", "--outdir", "build", "--keep-logs", "--keep-intermediates"],
        cwd=PAPER_DIR,
        capture_output=True,
        text=True,
        check=False,
    )
    if res.returncode != 0:
        print(res.stdout, file=sys.stderr)
        print(res.stderr, file=sys.stderr)
        sys.exit(res.returncode)

    log_pattern = re.compile(
        r"Overfull \\hbox|Overfull \\vbox|Float too large for page|LaTeX Warning: Reference|"
        r"LaTeX Warning: Citation|LaTeX Warning: Label .* multiply defined|Missing character"
    )
    log_txt = (build_dir / "main.log").read_text(encoding="utf-8", errors="replace")
    bad_lines = [ln for ln in log_txt.splitlines() if log_pattern.search(ln)]
    if bad_lines:
        print(f"WARNING: Found {len(bad_lines)} TeX log issues:", file=sys.stderr)
        for ln in bad_lines:
            print("  " + ln, file=sys.stderr)
        sys.exit(1)

    frozen_pdf = DIST_DIR / "Donahue_2026_unsolved_problems_mega_atlas.pdf"
    shutil.copy2(build_dir / "main.pdf", frozen_pdf)
    print(f"PASS: Compiled {frozen_pdf.name} ({frozen_pdf.stat().st_size / 1048576:.3f} MB) with 0 overfull hboxes/vboxes & 0 undefined refs!")

    # Package deterministic arXiv tarball (mtime=0, uid=0, gid=0, USTAR)
    tar_buf = io.BytesIO()
    files = [
        ("main.tex", PAPER_DIR / "main.tex"),
        ("main.bbl", build_dir / "main.bbl"),
        ("refs.bib", PAPER_DIR / "refs.bib"),
    ] + [(f"figures/{p.name}", p) for p in sorted((PAPER_DIR / "figures").glob("*.pdf"))]

    with tarfile.open(fileobj=tar_buf, mode="w", format=tarfile.USTAR_FORMAT) as tf:
        for arcname, src in files:
            raw = src.read_bytes()
            ti = tarfile.TarInfo(name=arcname)
            ti.size = len(raw)
            ti.mtime = 0
            ti.uid = 0
            ti.gid = 0
            ti.uname = ""
            ti.gname = ""
            ti.mode = 0o644
            tf.addfile(ti, io.BytesIO(raw))

    arxiv_gz = DIST_DIR / "arxiv_submission.tar.gz"
    with arxiv_gz.open("wb") as f_out:
        with gzip.GzipFile(filename="", mode="wb", fileobj=f_out, compresslevel=9, mtime=0) as gz:
            gz.write(tar_buf.getvalue())
    print(f"PASS: Packaged deterministic {arxiv_gz.name} ({arxiv_gz.stat().st_size / 1048576:.3f} MB)")

    # Clean-room arXiv compilation verification (exit code + zero-warning log parity)
    tmp = Path(tempfile.mkdtemp(prefix="arxiv_clean_"))
    try:
        with tarfile.open(arxiv_gz, "r:gz") as tf:
            tf.extractall(tmp, filter="data")
        cres = subprocess.run(
            [tectonic, "-X", "compile", "main.tex", "--keep-logs"],
            cwd=tmp,
            capture_output=True,
            text=True,
            check=False,
        )
        if cres.returncode != 0:
            print("FAIL: Clean-room arXiv compilation failed:\n" + cres.stderr, file=sys.stderr)
            sys.exit(cres.returncode)
        clog = (tmp / "main.log").read_text(encoding="utf-8", errors="replace") if (tmp / "main.log").exists() else ""
        cbad = [ln for ln in clog.splitlines() if log_pattern.search(ln)]
        if cbad:
            print(f"FAIL: Clean-room arXiv tarball had {len(cbad)} TeX log issues:", file=sys.stderr)
            for ln in cbad:
                print("  " + ln, file=sys.stderr)
            sys.exit(1)
        print("PASS: Clean-room arXiv tarball compilation succeeded with 0 warnings!")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
