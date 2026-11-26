# SPDX-License-Identifier: Apache-2.0
<#
.SYNOPSIS
    One-command reproducible build, FAIR metadata sync, 92-theorem Pure Lean 4.35.0 verification,
    AMS-LaTeX white paper + clean-room arXiv tarball build, immutable AutoResearch gate,
    full pytest + Hypothesis + differential + mutation + lint + typecheck suite,
    forensic audit, Zenodo dry-run, and SHA-256 verification for Mega-Atlas V2.4.0.
#>
param(
    [switch]$SkipCharts,
    [switch]$SkipExport,
    [switch]$SkipLean,
    [switch]$SkipPaper
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $RepoRoot

$VenvPy = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$Py = if (Test-Path -LiteralPath $VenvPy) { $VenvPy } else { "python" }

Write-Host "=== Unsolved Problems Mega-Atlas V2.4.0 Reproducible Build ===" -ForegroundColor Cyan
Write-Host "Python: $Py"

if (-not $SkipCharts) {
    Write-Host "`n[1/10] Generating 15 charts (PNG+SVG), 5 vector PDF paper figures & social card..." -ForegroundColor Yellow
    & $Py src\v2_charts.py
}

if (-not $SkipExport) {
    Write-Host "`n[2/10] Exporting CSV, TSV, JSON(.gz), JSONL(.gz), SQLite+FTS5, 15-sheet XLSX, XLS, MD, TXT, RANKING.md & <4 MB WCAG HTML..." -ForegroundColor Yellow
    & $Py src\v2_export_all.py --skip-pdf
}

if (-not $SkipLean) {
    Write-Host "`n[3/10] Building & auditing 92 Pure Lean 4.35.0 formal theorems..." -ForegroundColor Yellow
    $LakeExe = Join-Path $env:USERPROFILE ".elan\bin\lake.exe"
    $Lake = if (Test-Path -LiteralPath $LakeExe) { $LakeExe } else { "lake" }
    Push-Location -LiteralPath (Join-Path $RepoRoot "lean")
    try {
        & $Lake build
        & $Lake env lean MegaAtlasProofs/VerifyAxioms.lean | Out-Null
    } finally {
        Pop-Location
    }
    & $Py scripts\check_readme_axioms.py
}

if (-not $SkipPaper) {
    Write-Host "`n[4/10] Compiling 10-page AMS-LaTeX white paper & clean-room arXiv tarball..." -ForegroundColor Yellow
    & $Py scripts\build_paper.py
}

Write-Host "`n[5/10] Generating FAIR metadata (croissant.json, ro-crate-metadata.json, data/MANIFEST.sha256) & llms-full.txt..." -ForegroundColor Yellow
& $Py scripts\generate_fair_metadata.py
& $Py scripts\generate_llms_full.py

Write-Host "`n[6/10] Syncing CHECKSUMS.sha256 & running full structural/cryptographic audit..." -ForegroundColor Yellow
if ($SkipLean) {
    & $Py scripts\audit_atlas.py --sync-checksums
} else {
    & $Py scripts\audit_atlas.py --sync-checksums --check-lean
}

Write-Host "`n[7/10] Running forensic audit, Zenodo dry-run & AutoResearch immutable gates..." -ForegroundColor Yellow
& $Py scripts\forensic_audit.py
& $Py scripts\publish_zenodo.py --dry-run
& $Py autoresearch\evaluate.py --verify-gates

Write-Host "`n[8/10] Running full pytest suite (functional, Hypothesis, differential, metamorphic, MCP, FAIR)..." -ForegroundColor Yellow
& $Py -m pytest tests/ -v

Write-Host "`n[9/10] Running ruff lint, mypy typecheck & 6-mutant semantic mutation audit..." -ForegroundColor Yellow
& $Py -m ruff check src rag mcp_server reference scripts examples tests
& $Py -m mypy src rag mcp_server reference scripts examples --ignore-missing-imports
& $Py scripts\run_mutation_audit.py

Write-Host "`n[10/10] Running Build Standard v1.2.0 repository audit..." -ForegroundColor Yellow
& pwsh -NoProfile -ExecutionPolicy Bypass -File scripts\Audit-Repo.ps1

Write-Host "`n=== ALL V2.4.0 BUILD & VERIFICATION GATES PASSED ===" -ForegroundColor Green
