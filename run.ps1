# MindMutant Run Script

# 1. Execute Evolution (Generate next generation)
Write-Host "🧬 Running evolution (Engine: DEAP)..." -ForegroundColor Cyan
python app.py new --engine deap

# Check exit code
if ($LASTEXITCODE -eq 0) {
    # 2. Start Local Data Server (if not running)
    $port = 8000
    $isPortOpen = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    
    if (-not $isPortOpen) {
        Write-Host "🌍 Starting local data server on port $port..." -ForegroundColor Cyan
        Start-Process -FilePath "python" -ArgumentList "-m http.server $port --directory data" -WindowStyle Hidden
        Start-Sleep -Seconds 2
    } else {
        Write-Host "🌍 Data server already running on port $port." -ForegroundColor Yellow
    }

    # 3. Start Streamlit Dashboard
    Write-Host "🚀 Starting Dashboard..." -ForegroundColor Green
    streamlit run src/viz/dashboard.py
} else {
    Write-Host "❌ Evolution failed. Aborting dashboard launch." -ForegroundColor Red
    exit 1
}
