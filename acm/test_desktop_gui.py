#!/usr/bin/env python3
"""
Test the desktop app GUI with example data from ejemplo_venta.csv
This script will automatically fill the form and test the processing
"""

import sys
import os
import time
import tkinter as tk
from tkinter import messagebox
import threading

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_desktop_app_with_examples():
    """Test the desktop app with example data"""
    print("=" * 60)
    print("TESTING DESKTOP APP GUI WITH EXAMPLE DATA")
    print("=" * 60)
    
    # Import the desktop app
    try:
        from desktop_app import RealEstateApp
        print("✅ Desktop app imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import desktop app: {e}")
        return False
    
    # Create the app
    try:
        app = RealEstateApp()
        print("✅ Desktop app created successfully")
    except Exception as e:
        print(f"❌ Failed to create desktop app: {e}")
        return False
    
    # Test with Example 1 data
    print("\n📋 Testing with Example 1 data...")
    example1_data = {
        "address": "CARRERA 17 No. 134-79",
        "operation": "VENTA",
        "area_habitable": 37.42,
        "terrace": False,
        "area_total": 37.42,
        "administration": 315000,
        "bedrooms": 1,
        "bathrooms": 1.0,
        "parking": 1,
        "walking_closet": False,
        "loft": False,
        "study_room": False,
        "floor": 4,
        "deposit": 1,
        "terrace_area": 0,
        "construction_age": 29,
        "interior_exterior": "I",
        "elevator": True,
        "finish_quality": 4,
        "conservation_state": 4,
        "location_quality": 5,
        "stratum": 4,
        "observations": "",
        "contact_method": "",
        "contact_info": "",
        "pricing": {
            "area": 37.42,
            "price_per_m2": 6948156.06627472,
            "total_area": 37.42,
            "total_price_per_m2": 6948156.06627472,
            "admin_per_m2": 8417.9583110636
        }
    }
    
    # Fill the form with example data
    try:
        # Fill basic information
        app.address_entry.insert(0, example1_data["address"])
        app.operation_var.set(example1_data["operation"])
        
        # Fill property details
        app.area_habitable_entry.insert(0, str(example1_data["area_habitable"]))
        app.area_total_entry.insert(0, str(example1_data["area_total"]))
        app.administration_entry.insert(0, str(example1_data["administration"]))
        app.bedrooms_entry.insert(0, str(example1_data["bedrooms"]))
        app.bathrooms_entry.insert(0, str(example1_data["bathrooms"]))
        app.parking_entry.insert(0, str(example1_data["parking"]))
        app.stratum_entry.insert(0, str(example1_data["stratum"]))
        
        # Fill amenities
        app.terrace_var.set(example1_data["terrace"])
        app.elevator_var.set(example1_data["elevator"])
        app.walking_closet_var.set(example1_data["walking_closet"])
        app.loft_var.set(example1_data["loft"])
        app.study_room_var.set(example1_data["study_room"])
        
        # Fill additional information
        app.floor_entry.insert(0, str(example1_data["floor"]))
        app.deposit_entry.insert(0, str(example1_data["deposit"]))
        app.construction_age_entry.insert(0, str(example1_data["construction_age"]))
        app.interior_exterior_var.set(example1_data["interior_exterior"])
        app.finish_quality_entry.insert(0, str(example1_data["finish_quality"]))
        app.conservation_state_entry.insert(0, str(example1_data["conservation_state"]))
        app.location_quality_entry.insert(0, str(example1_data["location_quality"]))
        app.observations_text.insert("1.0", example1_data["observations"])
        app.contact_method_entry.insert(0, example1_data["contact_method"])
        app.contact_info_entry.insert(0, example1_data["contact_info"])
        
        # Fill pricing information
        app.pricing_area_entry.insert(0, str(example1_data["pricing"]["area"]))
        app.pricing_price_per_m2_entry.insert(0, str(example1_data["pricing"]["price_per_m2"]))
        app.pricing_total_area_entry.insert(0, str(example1_data["pricing"]["total_area"]))
        app.pricing_total_price_per_m2_entry.insert(0, str(example1_data["pricing"]["total_price_per_m2"]))
        app.pricing_admin_per_m2_entry.insert(0, str(example1_data["pricing"]["admin_per_m2"]))
        
        print("✅ Form filled with Example 1 data")
        
        # Test the processing (this will actually run the workflow)
        print("🔄 Testing property processing...")
        
        # Switch to results tab to see the output
        app.notebook.select(2)  # Results tab
        
        # Process the property
        app.process_property()
        
        print("✅ Property processing completed")
        
        # Check if output files were created
        output_dir = "outputs"
        if os.path.exists(output_dir):
            files = os.listdir(output_dir)
            csv_files = [f for f in files if f.endswith('.csv')]
            print(f"✅ Output files created: {len(csv_files)} CSV files")
            for file in csv_files:
                print(f"   📄 {file}")
        else:
            print("❌ No output directory found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during form filling: {e}")
        return False

def run_gui_test():
    """Run the GUI test in a separate thread"""
    def test_thread():
        try:
            success = test_desktop_app_with_examples()
            if success:
                print("\n🎉 Desktop app GUI test completed successfully!")
                print("The app window should be open and you can see the results.")
            else:
                print("\n❌ Desktop app GUI test failed!")
        except Exception as e:
            print(f"\n❌ Error during GUI test: {e}")
    
    # Run test in a separate thread
    test_thread_obj = threading.Thread(target=test_thread)
    test_thread_obj.daemon = True
    test_thread_obj.start()
    
    # Keep the main thread alive for a bit to let the test complete
    time.sleep(2)

def main():
    """Main test function"""
    print("Real Estate Analytics Desktop App - GUI Test")
    print("This will open the desktop app and fill it with example data")
    print("Press Ctrl+C to stop the test")
    
    try:
        run_gui_test()
        
        # Keep the app running
        print("\nDesktop app is running. Close the window to exit.")
        print("You can interact with the form and test the processing manually.")
        
        # Start the main event loop
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        # Keep running until the user closes the app
        root.mainloop()
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
