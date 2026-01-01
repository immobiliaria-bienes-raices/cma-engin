@echo off
REM ============================================================
REM Real Estate Analytics Desktop App Launcher
REM This script installs all dependencies and launches the app
REM ============================================================

echo.
echo ============================================================
echo Real Estate Analytics - Desktop App Launcher
echo ============================================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if Python is installed
echo [1/5] Checking Python installation...
set PYTHON_CMD=

REM Try different Python commands
echo Checking PATH for Python...
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    goto :python_found
)

python3 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python3
    goto :python_found
)

REM Try Python Launcher (py.exe) - common on Windows
py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    goto :python_found
)

REM Try using WHERE command to find Python
echo Searching for Python using WHERE command...
where python >nul 2>&1
if not errorlevel 1 (
    for /f "delims=" %%i in ('where python') do (
        set PYTHON_CMD=%%i
        goto :python_found
    )
)

where py >nul 2>&1
if not errorlevel 1 (
    for /f "delims=" %%i in ('where py') do (
        set PYTHON_CMD=%%i
        goto :python_found
    )
)

echo Checking common installation locations...

REM Try common installation paths (checking multiple versions)
for %%v in (39 310 311 312 313 38 37) do (
    if exist "C:\Python%%v\python.exe" (
        set PYTHON_CMD=C:\Python%%v\python.exe
        goto :python_found
    )
    if exist "C:\Program Files\Python%%v\python.exe" (
        set PYTHON_CMD="C:\Program Files\Python%%v\python.exe"
        goto :python_found
    )
    if exist "%LOCALAPPDATA%\Programs\Python\Python%%v\python.exe" (
        set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python%%v\python.exe"
        goto :python_found
    )
    if exist "%ProgramFiles%\Python%%v\python.exe" (
        set PYTHON_CMD="%ProgramFiles%\Python%%v\python.exe"
        goto :python_found
    )
)

REM Try AppData Local path (common for user installations)
if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe" (
    set PYTHON_CMD="%USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe"
    goto :python_found
)
if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python310\python.exe" (
    set PYTHON_CMD="%USERPROFILE%\AppData\Local\Programs\Python\Python310\python.exe"
    goto :python_found
)
if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe" (
    set PYTHON_CMD="%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe"
    goto :python_found
)
if exist "%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe" (
    set PYTHON_CMD="%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe"
    goto :python_found
)

REM Try searching in Program Files (x86)
if exist "%ProgramFiles(x86)%\Python39\python.exe" (
    set PYTHON_CMD="%ProgramFiles(x86)%\Python39\python.exe"
    goto :python_found
)
if exist "%ProgramFiles(x86)%\Python310\python.exe" (
    set PYTHON_CMD="%ProgramFiles(x86)%\Python310\python.exe"
    goto :python_found
)

REM Python not found - provide helpful instructions
echo.
echo ============================================================
echo ERROR: Python is not installed or not in PATH!
echo ============================================================
echo.
echo QUICK FIX OPTIONS:
echo.
echo Option 1: Install Python (Recommended)
echo   1. Download from: https://www.python.org/downloads/
echo   2. During installation, CHECK "Add Python to PATH"
echo   3. Restart your computer
echo   4. Run this script again
echo.
echo Option 2: Find Existing Python
echo   1. Run: find_python.bat (in this folder)
echo   2. It will search for Python and show you where it is
echo.
echo Option 3: Add Python to PATH Manually
echo   1. Find Python folder (common locations below)
echo   2. Press Win+X ^> System ^> Advanced system settings
echo   3. Environment Variables ^> Edit Path ^> Add Python folder
echo   4. Restart Command Prompt
echo.
echo Common Python locations checked:
echo   - C:\Python39\, C:\Python310\, C:\Python311\, C:\Python312\
echo   - C:\Program Files\Python39\, etc.
echo   - %LOCALAPPDATA%\Programs\Python\Python39\
echo   - %USERPROFILE%\AppData\Local\Programs\Python\Python39\
echo.
echo ============================================================
echo.
pause
exit /b 1

:python_found
%PYTHON_CMD% --version
echo Python found! ✓
echo Using: %PYTHON_CMD%
echo.

REM Upgrade pip
echo [2/5] Upgrading pip...
%PYTHON_CMD% -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo WARNING: Could not upgrade pip, continuing anyway...
) else (
    echo pip upgraded! ✓
)
echo.

REM Install required packages
echo [3/5] Installing required packages...
echo This may take a few minutes on first run...
echo.

REM Install packages from requirements_desktop.txt (preferred) or requirements.txt
if exist requirements_desktop.txt (
    echo Installing packages from requirements_desktop.txt...
    %PYTHON_CMD% -m pip install -r requirements_desktop.txt --quiet
    if errorlevel 1 (
        echo WARNING: Some packages failed to install, trying individual installation...
        %PYTHON_CMD% -m pip install Flask==2.3.3 Werkzeug==2.3.7 requests==2.31.0 beautifulsoup4==4.12.2 urllib3==2.0.7 pandas openpyxl --quiet
    ) else (
        echo All packages installed! ✓
    )
) else if exist requirements.txt (
    echo Installing packages from requirements.txt...
    %PYTHON_CMD% -m pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo WARNING: Some packages from requirements.txt failed to install
    )
    echo Installing additional required packages...
    %PYTHON_CMD% -m pip install pandas openpyxl --quiet
) else (
    echo Installing required packages directly...
    %PYTHON_CMD% -m pip install Flask==2.3.3 Werkzeug==2.3.7 requests==2.31.0 beautifulsoup4==4.12.2 urllib3==2.0.7 pandas openpyxl --quiet
)
if errorlevel 1 (
    echo ERROR: Failed to install required packages!
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)
echo.

REM Verify tkinter (usually comes with Python)
echo [4/5] Verifying tkinter (GUI library)...
%PYTHON_CMD% -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo WARNING: tkinter not found. Trying to install...
    %PYTHON_CMD% -m pip install tk --quiet
    if errorlevel 1 (
        echo ERROR: tkinter is required but could not be installed!
        echo On Windows, tkinter should come with Python.
        echo Please reinstall Python and make sure tkinter is included.
        pause
        exit /b 1
    )
) else (
    echo tkinter found! ✓
)
echo.

REM Launch the desktop app
echo [5/5] Launching Desktop App...
echo.
echo ============================================================
echo Starting Real Estate Analytics Desktop App...
echo ============================================================
echo.
echo The application window should open shortly.
echo If it doesn't appear, check the error messages above.
echo.
echo To close this window, close the application first.
echo.

%PYTHON_CMD% desktop_app.py

REM Check if app exited with error
if errorlevel 1 (
    echo.
    echo ============================================================
    echo ERROR: The application exited with an error!
    echo ============================================================
    echo.
    echo Please check the error messages above.
    echo Common issues:
    echo - Missing dependencies (run this script again)
    echo - Python version too old (need 3.7+)
    echo - tkinter not installed
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Application closed successfully.
echo ============================================================
pause

