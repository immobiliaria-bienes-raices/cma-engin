#!/usr/bin/env python3
"""
Real Estate Analytics Desktop Application Launcher

Simple launcher for the desktop application.
"""

import sys
import os
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import tkinter
        print("✅ tkinter is available")
        return True
    except ImportError:
        print("❌ tkinter is not available. Please install python3-tkinter")
        return False

def main():
    """Launch the desktop application"""
    print("=" * 60)
    print("Real Estate Analytics - Desktop Application")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease install the required dependencies:")
        print("sudo apt-get install python3-tkinter")
        sys.exit(1)
    
    print("\nStarting desktop application...")
    print("Close the application window to exit.")
    print("-" * 60)
    
    try:
        # Run the desktop application
        subprocess.run([sys.executable, "desktop_app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running desktop application: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nApplication closed by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
