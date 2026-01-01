@echo off
REM ============================================================
REM Python Finder - Helps locate Python installation
REM ============================================================

echo.
echo ============================================================
echo Python Finder - Searching for Python installations...
echo ============================================================
echo.

set PYTHON_FOUND=0

REM Check PATH commands
echo Checking common Python commands...
python --version >nul 2>&1
if not errorlevel 1 (
    echo [FOUND] python command
    python --version
    set PYTHON_FOUND=1
    goto :end
)

python3 --version >nul 2>&1
if not errorlevel 1 (
    echo [FOUND] Python3 found
    python3 --version
    set PYTHON_FOUND=1
    goto :end
)

py --version >nul 2>&1
if not errorlevel 1 (
    echo [FOUND] Python Launcher (py.exe) found
    py --version
    set PYTHON_FOUND=1
    goto :end
)

echo [NOT FOUND] Python not in PATH
echo.
echo Searching common installation locations...
echo.

REM Check common locations
if exist "C:\Python39\python.exe" (
    echo [FOUND] C:\Python39\python.exe
    C:\Python39\python.exe --version
    set PYTHON_FOUND=1
)
if exist "C:\Python310\python.exe" (
    echo [FOUND] C:\Python310\python.exe
    C:\Python310\python.exe --version
    set PYTHON_FOUND=1
)
if exist "C:\Python311\python.exe" (
    echo [FOUND] C:\Python311\python.exe
    C:\Python311\python.exe --version
    set PYTHON_FOUND=1
)
if exist "C:\Python312\python.exe" (
    echo [FOUND] C:\Python312\python.exe
    C:\Python312\python.exe --version
    set PYTHON_FOUND=1
)
if exist "C:\Program Files\Python39\python.exe" (
    echo [FOUND] C:\Program Files\Python39\python.exe
    "C:\Program Files\Python39\python.exe" --version
    set PYTHON_FOUND=1
)
if exist "C:\Program Files\Python310\python.exe" (
    echo [FOUND] C:\Program Files\Python310\python.exe
    "C:\Program Files\Python310\python.exe" --version
    set PYTHON_FOUND=1
)
if exist "C:\Program Files\Python311\python.exe" (
    echo [FOUND] C:\Program Files\Python311\python.exe
    "C:\Program Files\Python311\python.exe" --version
    set PYTHON_FOUND=1
)
if exist "C:\Program Files\Python312\python.exe" (
    echo [FOUND] C:\Program Files\Python312\python.exe
    "C:\Program Files\Python312\python.exe" --version
    set PYTHON_FOUND=1
)
if exist "%LOCALAPPDATA%\Programs\Python\Python39\python.exe" (
    echo [FOUND] %LOCALAPPDATA%\Programs\Python\Python39\python.exe
    "%LOCALAPPDATA%\Programs\Python\Python39\python.exe" --version
    set PYTHON_FOUND=1
)
if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    echo [FOUND] %LOCALAPPDATA%\Programs\Python\Python310\python.exe
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" --version
    set PYTHON_FOUND=1
)
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    echo [FOUND] %LOCALAPPDATA%\Programs\Python\Python311\python.exe
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" --version
    set PYTHON_FOUND=1
)
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    echo [FOUND] %LOCALAPPDATA%\Programs\Python\Python312\python.exe
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" --version
    set PYTHON_FOUND=1
)

:end
echo.
if %PYTHON_FOUND%==0 (
    echo ============================================================
    echo Python NOT FOUND!
    echo ============================================================
    echo.
    echo Please install Python 3.7 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During installation, check "Add Python to PATH"
    echo.
    echo If Python is already installed:
    echo 1. Find your Python installation folder
    echo 2. Add it to Windows PATH environment variable
    echo    - Right-click "This PC" ^> Properties
    echo    - Advanced system settings ^> Environment Variables
    echo    - Edit "Path" variable ^> Add Python folder
    echo.
) else (
    echo ============================================================
    echo Python found! You can now run launch_desktop_app.bat
    echo ============================================================
)
echo.
pause

