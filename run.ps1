Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "    CampusConnect - Lost and Found Management System" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $ScriptDir

# Determine python command
$PythonCmd = "py"
try {
    & py --version | Out-Null
} catch {
    try {
        & python --version | Out-Null
        $PythonCmd = "python"
    } catch {
        Write-Error "Python was not found. Please install Python from https://www.python.org/"
        exit 1
    }
}

Write-Host "Using Python launcher: $PythonCmd" -ForegroundColor Green

# Create venv if not existing
if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "[INFO] Creating virtual environment (.venv)..." -ForegroundColor Yellow
    & $PythonCmd -m venv .venv
}

Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

Write-Host "[INFO] Installing requirements..." -ForegroundColor Yellow
python -m pip install -r requirements.txt

Write-Host "`nLaunching CampusConnect..." -ForegroundColor Green
python -m streamlit run app.py
