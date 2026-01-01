# ============================================================
# Real Estate Analytics Desktop App Launcher (PowerShell)
# This script installs all dependencies and launches the app
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Real Estate Analytics - Desktop App Launcher" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

# Check if Python is installed
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "$pythonVersion" -ForegroundColor Green
    Write-Host "Python found! ✓" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.7 or higher from:" -ForegroundColor Yellow
    Write-Host "https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Upgrade pip
Write-Host "[2/5] Upgrading pip..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip --quiet
    Write-Host "pip upgraded! ✓" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Could not upgrade pip, continuing anyway..." -ForegroundColor Yellow
}
Write-Host ""

# Install required packages
Write-Host "[3/5] Installing required packages..." -ForegroundColor Yellow
Write-Host "This may take a few minutes on first run..." -ForegroundColor Gray
Write-Host ""

$packagesInstalled = $false

# Try to install from requirements_desktop.txt first
if (Test-Path "requirements_desktop.txt") {
    Write-Host "Installing packages from requirements_desktop.txt..." -ForegroundColor Gray
    try {
        python -m pip install -r requirements_desktop.txt --quiet
        Write-Host "All packages installed! ✓" -ForegroundColor Green
        $packagesInstalled = $true
    } catch {
        Write-Host "WARNING: Some packages failed to install, trying individual installation..." -ForegroundColor Yellow
    }
}

# If not installed yet, try requirements.txt
if (-not $packagesInstalled -and (Test-Path "requirements.txt")) {
    Write-Host "Installing packages from requirements.txt..." -ForegroundColor Gray
    try {
        python -m pip install -r requirements.txt --quiet
        Write-Host "Installing additional required packages..." -ForegroundColor Gray
        python -m pip install pandas openpyxl --quiet
        Write-Host "All packages installed! ✓" -ForegroundColor Green
        $packagesInstalled = $true
    } catch {
        Write-Host "WARNING: Some packages failed to install..." -ForegroundColor Yellow
    }
}

# If still not installed, install directly
if (-not $packagesInstalled) {
    Write-Host "Installing required packages directly..." -ForegroundColor Gray
    try {
        python -m pip install Flask==2.3.3 Werkzeug==2.3.7 requests==2.31.0 beautifulsoup4==4.12.2 urllib3==2.0.7 pandas openpyxl --quiet
        Write-Host "All packages installed! ✓" -ForegroundColor Green
        $packagesInstalled = $true
    } catch {
        Write-Host "ERROR: Failed to install required packages!" -ForegroundColor Red
        Write-Host "Please check your internet connection and try again." -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
}
Write-Host ""

# Verify tkinter
Write-Host "[4/5] Verifying tkinter (GUI library)..." -ForegroundColor Yellow
try {
    python -c "import tkinter" 2>$null
    Write-Host "tkinter found! ✓" -ForegroundColor Green
} catch {
    Write-Host "WARNING: tkinter not found. Trying to install..." -ForegroundColor Yellow
    try {
        python -m pip install tk --quiet
        Write-Host "tkinter installed! ✓" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: tkinter is required but could not be installed!" -ForegroundColor Red
        Write-Host "On Windows, tkinter should come with Python." -ForegroundColor Yellow
        Write-Host "Please reinstall Python and make sure tkinter is included." -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
}
Write-Host ""

# Launch the desktop app
Write-Host "[5/5] Launching Desktop App..." -ForegroundColor Yellow
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Starting Real Estate Analytics Desktop App..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "The application window should open shortly." -ForegroundColor Gray
Write-Host "If it doesn't appear, check the error messages above." -ForegroundColor Gray
Write-Host ""

try {
    python desktop_app.py
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "Application closed successfully." -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host "ERROR: The application exited with an error!" -ForegroundColor Red
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please check the error messages above." -ForegroundColor Yellow
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "- Missing dependencies (run this script again)" -ForegroundColor Gray
    Write-Host "- Python version too old (need 3.7+)" -ForegroundColor Gray
    Write-Host "- tkinter not installed" -ForegroundColor Gray
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Read-Host "Press Enter to exit"

