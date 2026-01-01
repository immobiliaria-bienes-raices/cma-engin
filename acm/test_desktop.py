#!/usr/bin/env python3
"""
Test script for the desktop application
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test if all required modules can be imported"""
    try:
        from real_estate_analytics.mappers.fincaraiz_mapper import FincaraizMapper
        from real_estate_analytics.orchestrators.fincaraiz_orchestrator import FincaraizOrchestrator
        from real_estate_analytics.converters.csv_converter import CSVConverter
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_components():
    """Test if components can be initialized"""
    try:
        from real_estate_analytics.mappers.fincaraiz_mapper import FincaraizMapper
        from real_estate_analytics.orchestrators.fincaraiz_orchestrator import FincaraizOrchestrator
        from real_estate_analytics.converters.csv_converter import CSVConverter
        
        mapper = FincaraizMapper()
        orchestrator = FincaraizOrchestrator()
        converter = CSVConverter()
        
        print("✅ All components initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Component initialization error: {e}")
        return False

def test_tkinter():
    """Test if tkinter works"""
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the window
        messagebox.showinfo("Test", "tkinter is working!")
        root.destroy()
        print("✅ tkinter is working")
        return True
    except Exception as e:
        print(f"❌ tkinter error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Real Estate Analytics Desktop App - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Component Initialization", test_components),
        ("Tkinter GUI", test_tkinter)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Desktop app should work correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
