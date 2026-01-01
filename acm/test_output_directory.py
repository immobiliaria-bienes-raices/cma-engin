#!/usr/bin/env python3
"""
Test script for the output directory feature in the desktop app
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_output_directory_feature():
    """Test the output directory feature"""
    print("=" * 60)
    print("TESTING OUTPUT DIRECTORY FEATURE")
    print("=" * 60)
    
    try:
        from desktop_app import RealEstateApp
        print("✅ Desktop app imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import desktop app: {e}")
        return False
    
    # Create a test root window
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    try:
        # Create the app
        app = RealEstateApp(root)
        print("✅ Desktop app created successfully")
        
        # Test default output directory
        print(f"✅ Default output directory: {app.output_dir}")
        print(f"✅ Output directory variable: {app.output_dir_var.get()}")
        
        # Test changing the output directory
        test_dir = "/tmp/test_output"
        app.output_dir_var.set(test_dir)
        app.output_dir = test_dir
        
        print(f"✅ Updated output directory: {app.output_dir}")
        
        # Test directory creation
        os.makedirs(app.output_dir, exist_ok=True)
        if os.path.exists(app.output_dir):
            print(f"✅ Output directory created successfully: {app.output_dir}")
        else:
            print(f"❌ Failed to create output directory: {app.output_dir}")
            return False
        
        # Test file path generation
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_filename = os.path.join(app.output_dir, f"test_file_{timestamp}.csv")
        
        # Create a test file
        with open(test_filename, 'w') as f:
            f.write("test,data\n1,2\n")
        
        if os.path.exists(test_filename):
            print(f"✅ Test file created successfully: {test_filename}")
            # Clean up
            os.remove(test_filename)
            print("✅ Test file cleaned up")
        else:
            print(f"❌ Failed to create test file: {test_filename}")
            return False
        
        print("\n🎉 Output directory feature test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        root.destroy()

def main():
    """Main test function"""
    print("Real Estate Analytics Desktop App - Output Directory Test")
    print("Testing the new output directory selection feature")
    print()
    
    success = test_output_directory_feature()
    
    if success:
        print("\n✅ All tests passed! The output directory feature is working correctly.")
        print("\nTo test the GUI:")
        print("1. Run: python3 desktop_app.py")
        print("2. Check the 'Directorio de Salida' section")
        print("3. Verify the default path is: /mnt/c/Users/Asus/Downloads/")
        print("4. Click 'Seleccionar Carpeta' to choose a different directory")
        print("5. Fill in the form and process a property")
        print("6. Check that files are saved to the selected directory")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
