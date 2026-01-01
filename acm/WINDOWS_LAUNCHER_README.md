# Windows Desktop App Launcher

This folder contains Windows executables to launch the Real Estate Analytics Desktop App.

## Quick Start

### Option 1: Automatic Launcher (Try This First)

1. **Double-click** `launch_desktop_app.bat`
2. The script will automatically search for Python and launch the app
3. If Python is not found, see troubleshooting below

### Option 2: Manual Python Path Launcher

If the automatic launcher can't find Python:

1. **Double-click** `launch_desktop_app_manual.bat`
2. When prompted, enter your Python path, for example:
   - `python` (if Python is in PATH)
   - `py` (Python Launcher)
   - `C:\Python39\python.exe`
   - `"C:\Program Files\Python39\python.exe"`
   - `"%USERPROFILE%\AppData\Local\Programs\Python\Python39\python.exe"`

### Option 3: Find Python First

1. **Double-click** `find_python.bat`
2. It will search your system and show where Python is installed
3. Note the path shown
4. Use that path with `launch_desktop_app_manual.bat`

### Option 4: PowerShell Method (Recommended for Windows 10/11)

1. **Right-click** `launch_desktop_app.ps1`
2. Select **"Run with PowerShell"**
3. If you get an execution policy error, run this first:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

## Requirements

- **Python 3.7 or higher** must be installed
- **Internet connection** (for first-time package installation)
- **Windows 7 or later**

## What the Launcher Does

The launcher script (`launch_desktop_app.bat` or `.ps1`) performs these steps automatically:

1. ✅ **Checks Python Installation** - Verifies Python is installed and accessible
2. ✅ **Upgrades pip** - Ensures you have the latest package installer
3. ✅ **Installs Dependencies** - Installs all required packages:
   - Flask (web framework)
   - requests (HTTP library)
   - beautifulsoup4 (web scraping)
   - pandas (data analysis)
   - openpyxl (Excel file generation)
   - urllib3 (URL handling)
   - And more...
4. ✅ **Verifies tkinter** - Checks that GUI library is available
5. ✅ **Launches App** - Starts the desktop application

## First-Time Setup

On first run, the script will download and install all dependencies. This may take 2-5 minutes depending on your internet speed.

**Subsequent runs** will be much faster as packages are already installed.

## Troubleshooting

### "Python is not installed"
- Download and install Python from https://www.python.org/downloads/
- **Important**: Check "Add Python to PATH" during installation
- Restart your computer after installation

### "pip install failed"
- Check your internet connection
- Try running as Administrator
- Some corporate networks block pip - contact your IT department

### "tkinter not found"
- tkinter should come with Python on Windows
- If missing, reinstall Python and ensure tkinter is included
- Or install manually: `pip install tk`

### "Execution Policy" Error (PowerShell)
Run this command in PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### App Doesn't Open
- Check the console window for error messages
- Make sure all dependencies installed successfully
- Try running `python desktop_app.py` directly to see detailed errors

## Manual Installation (If Launcher Fails)

If the launcher doesn't work, you can install manually:

```cmd
cd path\to\acm\folder
python -m pip install -r requirements_desktop.txt
python desktop_app.py
```

## Files Included

- `launch_desktop_app.bat` - Windows Batch file launcher
- `launch_desktop_app.ps1` - PowerShell launcher (more features)
- `requirements_desktop.txt` - Complete list of required packages
- `desktop_app.py` - The main desktop application

## Using the Desktop App

Once launched, fill in the form with your property details:

**Example Test Data:**
- **Dirección**: `cll 118A #13-42`
- **Operación**: `VENTA`
- **Área Total**: `95`
- **Alcobas**: `3`
- **Baños**: `3`
- **Estrato**: `4`
- **Precio por m²**: `6315789`
- **Edad Construcción**: `16` ← Important!

Click **"Procesar Propiedad"** to search for similar properties on Fincaraiz.

## Support

If you encounter issues:
1. Check the console output for error messages
2. Verify Python version: `python --version` (should be 3.7+)
3. Verify packages: `pip list` (should show Flask, pandas, etc.)
4. Try running `python desktop_app.py` directly for detailed errors

