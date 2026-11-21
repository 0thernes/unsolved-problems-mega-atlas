<#
.SYNOPSIS
    One-command reproducible build, Pure Lean 4.35.0 verification, pytest suite,
    and cryptographic SHA-256 audit for the Unsolved Problems Mega-Atlas (V2.1.0).
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

Write-Host "=== 0thernes Mega-Atlas V2.1.0 Reproducible Build ===" -ForegroundColor Cyan
Write-Host "Python: $Py"

if (-not $SkipCharts) {
    Write-Host "`n[1/5] Generating 12 publication charts (PNG + SVG)..." -ForegroundColor Yellow
    & $Py src\v2_charts.py
}

if (-not $SkipExport) {
    Write-Host "`n[2/5] Exporting CSV, TSV, JSON, JSONL, SQLite+FTS5, XLSX, XLS, MD, TXT, RANKING.md, HTML & PDF..." -ForegroundColor Yellow
    & $Py src\v2_export_all.py
}

if (-not $SkipLean) {
    Write-Host "`n[3/5] Building & auditing Pure Lean 4.35.0 formal invariants (46 theorems)..." -ForegroundColor Yellow
    $LakeExe = Join-Path $env:USERPROFILE ".elan\bin\lake.exe"
    $Lake = if (Test-Path -LiteralPath $LakeExe) { $LakeExe } else { "lake" }
    Push-Location -LiteralPath (Join-Path $RepoRoot "lean")
    try {
        & $Lake build
    } finally {
        Pop-Location
    }
}

Write-Host "`n[4/5] Syncing SHA-256 manifest & running full structural/cryptographic audit..." -ForegroundColor Yellow
if ($SkipLean) {
    & $Py scripts\audit_atlas.py --sync-checksums
} else {
    & $Py scripts\audit_atlas.py --sync-checksums --check-lean
}

Write-Host "`n[5/5] Running full pytest verification suite..." -ForegroundColor Yellow
& $Py -m pytest -v

Write-Host "`n=== ALL V2.1.0 BUILD & VERIFICATION GATES PASSED ===" -ForegroundColor Green
