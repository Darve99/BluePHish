#!/usr/bin/env pwsh
# BluePHish Platform Quick Test Script
# Usage: .\test_platform.ps1

$ErrorActionPreference = 'Stop'
$BluePHishRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Join-Path $BluePHishRoot 'backend'
$FrontendDir = Join-Path $BluePHishRoot 'frontend'

Write-Host 'BluePHish platform launcher' -ForegroundColor Cyan

Write-Host "`n[1/5] Checking prerequisites..." -ForegroundColor Yellow
$commands = @('python', 'node', 'npm')
$allGood = $true
foreach ($cmd in $commands) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        Write-Host "  [OK] $cmd" -ForegroundColor Green
    }
    else {
        Write-Host "  [MISSING] $cmd" -ForegroundColor Red
        $allGood = $false
    }
}

if (-not $allGood) {
    Write-Host "Prerequisites are missing." -ForegroundColor Red
    exit 1
}

Write-Host "`n[2/5] Verifying project structure..." -ForegroundColor Yellow
$required = @(
    "$BackendDir/main.py",
    "$BackendDir/requirements.txt",
    "$BackendDir/app/auth.py",
    "$FrontendDir/package.json",
    "$FrontendDir/src/App.tsx",
    "$BluePHishRoot/README.md"
)

foreach ($item in $required) {
    if (Test-Path $item) {
        Write-Host "  [OK] $(Split-Path $item -Leaf)" -ForegroundColor Green
    }
    else {
        Write-Host "  [MISSING] $item" -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n[3/5] Setting up backend..." -ForegroundColor Yellow
Push-Location $BackendDir
if (-not (Test-Path '.venv')) {
    python -m venv .venv
}
& '.\.venv\Scripts\Activate.ps1'
pip install -q -r requirements.txt
Pop-Location

Write-Host "`n[4/5] Setting up frontend..." -ForegroundColor Yellow
Push-Location $FrontendDir
if (-not (Test-Path 'node_modules')) {
    npm install -q
}
Pop-Location

Write-Host "`n[5/5] Starting servers..." -ForegroundColor Yellow
$shellExe = if (Get-Command pwsh -ErrorAction SilentlyContinue) { 'pwsh' } else { 'powershell.exe' }
$backendCommand = "Set-Location '$BackendDir'; .\\.venv\\Scripts\\Activate.ps1; uvicorn main:app --reload"
Start-Process $shellExe -ArgumentList '-NoExit', '-Command', $backendCommand

$frontendCommand = "Set-Location '$FrontendDir'; npm run dev"
Start-Process $shellExe -ArgumentList '-NoExit', '-Command', $frontendCommand

Write-Host "`nServers started." -ForegroundColor Green
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "API docs: http://localhost:8000/docs" -ForegroundColor Cyan

Read-Host "Press Enter to exit"
