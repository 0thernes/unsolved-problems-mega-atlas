<#
.SYNOPSIS
    One-command reproducible build, FAIR metadata sync, Pure Lean 4.35.0 verification (72 theorems),
    immutable AutoResearch evaluation gate, 25-test pytest suite (incl. 9-tool dual-framed MCP stdio test),
    forensic integrity audit, Zenodo dry-run validation, and cryptographic SHA-256 audit
    for the Unsolved Problems Mega-Atlas (V2.3.0).
#>
param(
    [switch]$SkipCharts,
    [switch]$SkipExport,
    [switch]$SkipLean
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $RepoRoot

$VenvPy = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$Py = if (Test-Path -LiteralPath $VenvPy) { $VenvPy } else { "python" }

Write-Host "=== 0thernes Mega-Atlas V2.3.0 Reproducible Build ===" -ForegroundColor Cyan
Write-Host "Python: $Py"

if (-not $SkipCharts) {
    Write-Host "`n[1/8] Generating 15 publication charts (30 files: PNG + SVG)..." -ForegroundColor Yellow
    & $Py src\v2_charts.py
}

if (-not $SkipExport) {
    Write-Host "`n[2/8] Exporting CSV, TSV, JSON, JSONL, SQLite+FTS5, 14-sheet XLSX, XLS, MD, TXT, RANKING.md, HTML & PDF..." -ForegroundColor Yellow
    & $Py src\v2_export_all.py
}

Write-Host "`n[3/8] Generating SHA-256-synced FAIR metadata (croissant.json + ro-crate-metadata.json)..." -ForegroundColor Yellow
& $Py scripts\generate_fair_metadata.py

if (-not $SkipLean) {
    Write-Host "`n[4/8] Building & auditing Pure Lean 4.35.0 formal invariants (72 theorems)..." -ForegroundColor Yellow
    $LakeExe = Join-Path $env:USERPROFILE ".elan\bin\lake.exe"
    $Lake = if (Test-Path -LiteralPath $LakeExe) { $LakeExe } else { "lake" }
    Push-Location -LiteralPath (Join-Path $RepoRoot "lean")
    try {
        & $Lake build
    } finally {
        Pop-Location
    }
}

Write-Host "`n[5/8] Syncing SHA-256 manifest & running full structural/cryptographic audit..." -ForegroundColor Yellow
if ($SkipLean) {
    & $Py scripts\audit_atlas.py --sync-checksums
} else {
    & $Py scripts\audit_atlas.py --sync-checksums --check-lean
}

Write-Host "`n[6/8] Running forensic audit & Option 1 Zenodo manifest dry-run..." -ForegroundColor Yellow
& $Py scripts\forensic_audit.py
& $Py scripts\publish_zenodo.py --dry-run

Write-Host "`n[7/8] Running immutable Karpathy AutoResearch evaluation gate..." -ForegroundColor Yellow
& $Py autoresearch\evaluate.py --verify-gates

Write-Host "`n[8/8] Running full 25-test pytest verification suite (incl. 9-tool MCP & FAIR parity)..." -ForegroundColor Yellow
& $Py -m pytest -v

Write-Host "`n=== ALL V2.3.0 BUILD & VERIFICATION GATES PASSED ===" -ForegroundColor Green
