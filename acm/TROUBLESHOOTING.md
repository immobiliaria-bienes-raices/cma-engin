# Troubleshooting Guide

## Python Not Found Error

If you get the error "Python is not installed or not in PATH", follow these steps:

### Option 1: Install Python (Recommended)

1. Download Python from: https://www.python.org/downloads/
2. **IMPORTANT**: During installation, check the box **"Add Python to PATH"**
3. Click "Install Now"
4. Restart your computer
5. Run `launch_desktop_app.bat` again

### Option 2: Find Existing Python Installation

1. Run `find_python.bat` - This will search for Python on your system
2. If Python is found, note the path
3. Add Python to PATH (see instructions below)

### Option 3: Add Python to PATH Manually

If Python is installed but not in PATH:

1. **Find Python Installation:**
   - Common locations:
     - `C:\Python39\`
     - `C:\Python310\`
     - `C:\Python311\`
     - `C:\Program Files\Python39\`
     - `%LOCALAPPDATA%\Programs\Python\Python39\`

2. **Add to PATH:**
   - Press `Win + X` → System
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find "Path" and click "Edit"
   - Click "New" and add:
     - `C:\Python39\` (or your Python folder)
     - `C:\Python39\Scripts\` (for pip)
   - Click OK on all windows
   - Restart Command Prompt/PowerShell

3. **Verify:**
   - Open Command Prompt
   - Type: `python --version`
   - Should show Python version

### Option 4: Use Python Launcher

Windows 10/11 often includes Python Launcher:

1. Try running: `py desktop_app.py`
2. If that works, you can modify `launch_desktop_app.bat` to use `py` instead of `python`

### Option 5: Manual Installation

If the launcher still doesn't work:

1. Open Command Prompt in the project folder
2. Find your Python executable (use `find_python.bat`)
3. Run manually:
   ```cmd
   "C:\Python39\python.exe" -m pip install -r requirements_desktop.txt
   "C:\Python39\python.exe" desktop_app.py
   ```

## Other Common Issues

### "pip install failed"

**Solutions:**
- Check internet connection
- Try running as Administrator
- Some corporate networks block pip - contact IT
- Try: `python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements_desktop.txt`

### "tkinter not found"

**Solutions:**
- tkinter should come with Python on Windows
- If missing, reinstall Python and ensure tkinter is included
- Or install: `pip install tk`

### "Execution Policy" Error (PowerShell)

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### App Window Doesn't Open

**Solutions:**
- Check console window for error messages
- Verify all packages installed: `pip list`
- Try running directly: `python desktop_app.py`
- Check Python version: `python --version` (need 3.7+)

### "Module not found" Errors

**Solution:**
- Re-run `launch_desktop_app.bat` to install missing packages
- Or install manually: `pip install [package-name]`

## Getting Help

If none of these solutions work:

1. Run `find_python.bat` and note the output
2. Check Python version: `python --version`
3. Check installed packages: `pip list`
4. Try running directly: `python desktop_app.py`
5. Note any error messages and share them for support

