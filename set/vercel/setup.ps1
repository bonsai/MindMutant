# Set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force

$ScriptDir = $PSScriptRoot
# Navigate to project root (2 levels up: set/vercel -> set -> root)
$ProjectRoot = Resolve-Path (Join-Path $ScriptDir "..\..")
Set-Location $ProjectRoot

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   MindMutant Vercel Setup (set/vercel)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$Source = Join-Path $ScriptDir "requirements.txt"
$Dest = Join-Path $ProjectRoot "requirements.txt"

if (Test-Path $Source) {
    Write-Host "Copying $Source to $Dest..." -ForegroundColor Yellow
    Copy-Item -Path $Source -Destination $Dest -Force
    
    Write-Host "`nSuccess! requirements.txt is now optimized for Vercel (Viewer Only)." -ForegroundColor Green
    Write-Host "Contents:" -ForegroundColor Gray
    Get-Content $Dest | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
    
    Write-Host "`nYou can now push to Vercel." -ForegroundColor Cyan
} else {
    Write-Error "Source file not found: $Source"
    exit 1
}
