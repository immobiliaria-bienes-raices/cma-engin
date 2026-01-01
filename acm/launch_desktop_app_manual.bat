@echo off
REM ============================================================
REM Real Estate Analytics Desktop App Launcher (Manual Python Path)
REM Use this if Python is not found automatically
REM ============================================================

echo.
echo ============================================================
echo Real Estate Analytics - Manual Python Path Launcher
echo ============================================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Try to find Python automatically first
set PYTHON_CMD=
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    goto :found_python
)

py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    goto :found_python
)

REM If not found, ask user
echo Python not found automatically.
echo.
echo Please enter your Python executable path.
echo Examples:
echo   - python (if in PATH)
echo   - py (Python Launcher)
echo   - C:\Python39\python.exe
echo   - "C:\Program Files\Python39\python.exe"
echo   - "%USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe"
echo.
set /p PYTHON_CMD="Enter Python command or path: "

REM Test the provided Python
echo.
echo Testing Python installation...
%PYTHON_CMD% --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Cannot run Python with: %PYTHON_CMD%
    echo.
    echo Please verify the path is correct.
    echo Common locations:
    echo   - C:\Python39\python.exe
    echo   - C:\Python310\python.exe
    echo   - C:\Program Files\Python39\python.exe
    echo   - %USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe
    echo.
    echo Tip: Run find_python.bat to search for Python
    echo.
    pause
    exit /b 1
)

:found_python
echo.
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

if exist requirements_desktop.txt (
    echo Installing packages from requirements_desktop.txt...
    %PYTHON_CMD% -m pip install -r requirements_desktop.txt --quiet
    if errorlevel 1 (
        echo WARNING: Some packages failed, trying individual installation...
        %PYTHON_CMD% -m pip install Flask==2.3.3 Werkzeug==2.3.7 requests==2.31.0 beautifulsoup4==4.12.2 urllib3==2.0.7 pandas openpyxl --quiet
    ) else (
        echo All packages installed! ✓
    )
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

REM Verify tkinter
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

%PYTHON_CMD% desktop_app.py

if errorlevel 1 (
    echo.
    echo ============================================================
    echo ERROR: The application exited with an error!
    echo ============================================================
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Application closed successfully.
echo ============================================================
pause

