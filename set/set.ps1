# Set execution policy to allow script execution (scope: Process)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
Set-Location $ProjectRoot

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   MindMutant Environment Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Define venv path
$VenvPath = Join-Path $ProjectRoot ".venv"

# 1. Create Virtual Environment
if (-not (Test-Path $VenvPath)) {
    Write-Host "[1/3] Creating virtual environment (.venv)..." -ForegroundColor Yellow
    python -m venv $VenvPath
} else {
    Write-Host "[1/3] Virtual environment already exists." -ForegroundColor Green
}

# 2. Check Python Executable in venv
$VenvPython = Join-Path $VenvPath "Scripts\python.exe"
if (-not (Test-Path $VenvPython)) {
    Write-Error "Python executable not found in $VenvPath. Setup failed."
    exit 1
}

# 3. Install Dependencies
$ReqPath = Join-Path $ScriptDir "requirements.txt"
if (Test-Path $ReqPath) {
    Write-Host "[2/3] Upgrading pip..." -ForegroundColor Yellow
    & $VenvPython -m pip install --upgrade pip

    Write-Host "[3/3] Installing dependencies from requirements.txt..." -ForegroundColor Yellow
    & $VenvPython -m pip install -r $ReqPath
} else {
    Write-Warning "requirements.txt not found at $ReqPath. Skipping installation."
}

Write-Host "`nSetup Completed Successfully! `u{1F389}" -ForegroundColor Green
Write-Host "To activate the environment, run:" -ForegroundColor Gray
Write-Host ".venv\Scripts\Activate.ps1" -ForegroundColor White
