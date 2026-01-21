# Set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force

$ScriptDir = $PSScriptRoot
Set-Location $ScriptDir

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   MindMutant Local Setup (set-local)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Virtual Environment
$VenvPath = Join-Path $ScriptDir ".venv"
if (-not (Test-Path $VenvPath)) {
    Write-Host "[1/4] Creating virtual environment (.venv)..." -ForegroundColor Yellow
    python -m venv $VenvPath
} else {
    Write-Host "[1/4] Virtual environment already exists." -ForegroundColor Green
}

$VenvPython = Join-Path $VenvPath "Scripts\python.exe"
if (-not (Test-Path $VenvPython)) {
    Write-Error "Python executable not found in $VenvPath."
    exit 1
}

# 2. Upgrade pip
Write-Host "[2/4] Upgrading pip..." -ForegroundColor Yellow
& $VenvPython -m pip install --upgrade pip

# 3. Install Dependencies
$ReqPath = Join-Path $ScriptDir "set\requirements_local.txt"
if (Test-Path $ReqPath) {
    Write-Host "[3/4] Installing dependencies from set/requirements_local.txt..." -ForegroundColor Yellow
    & $VenvPython -m pip install -r $ReqPath
} else {
    Write-Error "Requirements file not found: $ReqPath"
    exit 1
}

# 4. Install Spacy Model (ja_core_news_md)
Write-Host "[4/4] Checking/Installing Spacy model (ja_core_news_md)..." -ForegroundColor Yellow
try {
    # Check if model is installed by trying to load it (simple check)
    & $VenvPython -c "import spacy; spacy.load('ja_core_news_md')" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Spacy model 'ja_core_news_md' is already installed." -ForegroundColor Green
    } else {
        Write-Host "Installing Spacy model 'ja_core_news_md'..." -ForegroundColor Yellow
        & $VenvPython -m spacy download ja_core_news_md
    }
} catch {
    Write-Host "Installing Spacy model 'ja_core_news_md'..." -ForegroundColor Yellow
    & $VenvPython -m spacy download ja_core_news_md
}

Write-Host "`nLocal Setup Completed Successfully! `u{1F389}" -ForegroundColor Green
Write-Host "Run './run.ps1' to start the local server." -ForegroundColor Gray
