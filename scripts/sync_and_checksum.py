"""Sync V2.0 Mega-Atlas sources + all compiled outputs to Z:\\unsolved-problems-mega-atlas and generate SHA-256 manifest."""

import os
import shutil
import hashlib
from pathlib import Path

SRC_ROOT = Path(r"C:\Users\Alexa\.gemini\antigravity\scratch\unsolved-problems-encyclopedia")
DST_ROOT = Path(r"Z:\unsolved-problems-mega-atlas")


def copy_tree_clean(src: Path, dst: Path):
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".venv"))


def main():
    DST_ROOT.mkdir(parents=True, exist_ok=True)
    # 1. Copy V2 source code
    src_dst = DST_ROOT / "src"
    src_dst.mkdir(parents=True, exist_ok=True)
    for fname in ["v2_schema.py", "v2_loader.py", "v2_charts.py", "v2_export_all.py"]:
        shutil.copy2(SRC_ROOT / "src" / fname, src_dst / fname)
    copy_tree_clean(SRC_ROOT / "src" / "v2_data", src_dst / "v2_data")

    # 2. Copy all compiled V2 outputs (CSV, TSV, JSON, XLSX, XLS, MD, TXT, HTML, PDF, 12 PNG+SVG charts)
    copy_tree_clean(SRC_ROOT / "outputs_v2", DST_ROOT / "outputs")

    # 3. Generate cryptographic SHA-256 checksums for all tracked output & data artifacts
    manifest_lines = []
    out_dir = DST_ROOT / "outputs"
    for p in sorted(out_dir.rglob("*")):
        if p.is_file():
            rel = p.relative_to(DST_ROOT).as_posix()
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            manifest_lines.append(f"{h}  {rel}")
    chk_path = DST_ROOT / "CHECKSUMS.sha256"
    chk_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    print(f"Synced V2.0 Mega-Atlas to {DST_ROOT}")
    print(f"Wrote {len(manifest_lines)} SHA-256 checksums to {chk_path}")


if __name__ == "__main__":
    main()
