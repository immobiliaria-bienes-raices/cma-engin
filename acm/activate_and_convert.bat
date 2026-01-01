@echo off
REM Activate virtual environment and convert CSV to XLSX (Windows)

cd /d "%~dp0"

echo ============================================================
echo CSV to XLSX Converter - Virtual Environment Setup
echo ============================================================
echo.

REM Check if virtual environment exists
if exist venv (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment activated
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment created and activated
)

echo.
echo Installing required packages...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet pandas openpyxl
echo ✅ Packages installed
echo.

REM Check if CSV file argument provided
if "%~1"=="" (
    echo Usage: %~nx0 ^<csv_file^> [output_xlsx_file] [property_address]
    echo.
    echo Example:
    echo   %~nx0 outputs\standardized_property.csv
    echo   %~nx0 outputs\standardized_property.csv output.xlsx "Calle 123 #45-67"
    echo.
    pause
    exit /b 1
)

set CSV_FILE=%~1
set OUTPUT_FILE=%~2
set ADDRESS=%~3

REM If output file not specified, use CSV name with .xlsx extension
if "%OUTPUT_FILE%"=="" (
    for %%F in ("%CSV_FILE%") do set OUTPUT_FILE=%%~dpnF.xlsx
)

echo Converting CSV to XLSX...
echo   Input:  %CSV_FILE%
echo   Output: %OUTPUT_FILE%
echo.

if not "%ADDRESS%"=="" (
    python csv_to_xlsx_parser.py "%CSV_FILE%" -o "%OUTPUT_FILE%" -a "%ADDRESS%"
) else (
    python csv_to_xlsx_parser.py "%CSV_FILE%" -o "%OUTPUT_FILE%"
)

if errorlevel 1 (
    echo.
    echo ❌ Conversion failed!
    pause
    exit /b 1
)

echo.
echo ✅ Conversion completed successfully!
echo.
pause

