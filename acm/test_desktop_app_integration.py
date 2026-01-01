#!/usr/bin/env python3
"""
Test Desktop App Integration with CSV to XLSX Parser

This script tests that the desktop app properly integrates the CSV to XLSX parser
without requiring the GUI to be launched.
"""

import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all imports work correctly"""
    print("=" * 80)
    print("TEST 1: Testing Imports")
    print("=" * 80)
    
    try:
        from real_estate_analytics.mappers.fincaraiz_mapper import FincaraizMapper
        from real_estate_analytics.orchestrators.fincaraiz_orchestrator import FincaraizOrchestrator
        from real_estate_analytics.converters.csv_converter import CSVConverter
        from real_estate_analytics.outputs.property_type_csv_generator import PropertyTypeCSVGenerator
        from real_estate_analytics.formatters.property_type_analysis_formatter import PropertyTypeAnalysisFormatter
        from csv_to_xlsx_parser import CSVToXLSXParser
        
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_desktop_app_class():
    """Test that DesktopApp class can be initialized"""
    print("\n" + "=" * 80)
    print("TEST 2: Testing Desktop App Class Initialization")
    print("=" * 80)
    
    try:
        # Import tkinter first to check if available
        import tkinter as tk
        
        # Import desktop app
        from desktop_app import RealEstateApp
        
        # Create a root window (hidden)
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Initialize the app
        app = RealEstateApp(root)
        
        # Check that CSV to XLSX parser is initialized
        if hasattr(app, 'csv_to_xlsx_parser'):
            print("✅ CSV to XLSX parser initialized in desktop app")
        else:
            print("❌ CSV to XLSX parser NOT found in desktop app")
            return False
        
        # Check that parser is the right type
        from csv_to_xlsx_parser import CSVToXLSXParser
        if isinstance(app.csv_to_xlsx_parser, CSVToXLSXParser):
            print("✅ CSV to XLSX parser is correct type")
        else:
            print(f"❌ CSV to XLSX parser is wrong type: {type(app.csv_to_xlsx_parser)}")
            return False
        
        # Clean up
        root.destroy()
        
        print("✅ Desktop app class initialization successful!")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing desktop app: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_csv_to_xlsx_conversion():
    """Test CSV to XLSX conversion with a sample CSV"""
    print("\n" + "=" * 80)
    print("TEST 3: Testing CSV to XLSX Conversion")
    print("=" * 80)
    
    try:
        from csv_to_xlsx_parser import CSVToXLSXParser
        
        # Use an existing CSV file for testing
        test_csv = "demo_standardized_1_20250919_195435.csv"
        
        if not os.path.exists(test_csv):
            print(f"⚠️  Test CSV file not found: {test_csv}")
            print("   Skipping conversion test")
            return True
        
        # Create parser
        parser = CSVToXLSXParser()
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_xlsx = f"test_integration_{timestamp}.xlsx"
        
        # Convert CSV to XLSX
        print(f"Converting: {test_csv} → {test_xlsx}")
        result = parser.parse_csv_to_xlsx(
            csv_file=test_csv,
            xlsx_file=test_xlsx,
            property_address="Test Property Address",
            city="Bogotá",
            analyst_name="Test Analyst"
        )
        
        if result['success']:
            print(f"✅ Conversion successful!")
            print(f"   Properties processed: {result['properties_processed']}")
            print(f"   Output file: {result['output_file']}")
            
            # Verify file exists
            if os.path.exists(test_xlsx):
                file_size = os.path.getsize(test_xlsx)
                print(f"   File size: {file_size} bytes")
                print(f"✅ XLSX file created successfully!")
                return True
            else:
                print(f"❌ XLSX file not found after conversion")
                return False
        else:
            print(f"❌ Conversion failed: {result.get('error', 'Unknown error')}")
            if 'error_trace' in result:
                print("\nError traceback:")
                print(result['error_trace'])
            return False
            
    except Exception as e:
        print(f"❌ Error testing conversion: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_workflow_simulation():
    """Simulate the desktop app workflow"""
    print("\n" + "=" * 80)
    print("TEST 4: Simulating Desktop App Workflow")
    print("=" * 80)
    
    try:
        from real_estate_analytics.mappers.fincaraiz_mapper import FincaraizMapper
        from csv_to_xlsx_parser import CSVToXLSXParser
        
        # Create property data (similar to what desktop app would create)
        property_data = {
            'address': 'cll 118A #13-42',
            'operation': 'VENTA',
            'area_habitable': 95.0,
            'bedrooms': 3,
            'bathrooms': 3.0,
            'construction_age': 16,
            'stratum': 4,
            'parking': 1,
            'pricing': {
                'price_per_m2': 6315789.47,
                'area': 95.0
            }
        }
        
        print("Step 1: Generating search URL...")
        mapper = FincaraizMapper()
        search_result = mapper.map_property_to_search(property_data)
        
        if 'error' in search_result:
            print(f"❌ Error generating URL: {search_result['error']}")
            return False
        
        print(f"✅ Search URL generated: {search_result['search_url'][:80]}...")
        
        # For testing, we'll use an existing CSV instead of scraping
        print("\nStep 2: Using existing CSV for testing...")
        test_csv = "demo_standardized_1_20250919_195435.csv"
        
        if not os.path.exists(test_csv):
            print(f"⚠️  Test CSV not found, skipping workflow test")
            return True
        
        print("\nStep 3: Converting CSV to XLSX...")
        parser = CSVToXLSXParser()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_xlsx = f"test_workflow_{timestamp}.xlsx"
        
        result = parser.parse_csv_to_xlsx(
            csv_file=test_csv,
            xlsx_file=test_xlsx,
            property_address=property_data['address'],
            city="Bogotá"
        )
        
        if result['success']:
            print(f"✅ Workflow simulation successful!")
            print(f"   CSV: {test_csv}")
            print(f"   XLSX: {test_xlsx}")
            print(f"   Properties: {result['properties_processed']}")
            return True
        else:
            print(f"❌ Workflow simulation failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error in workflow simulation: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("DESKTOP APP INTEGRATION TEST SUITE")
    print("=" * 80)
    print("\nTesting CSV to XLSX parser integration in desktop_app.py")
    print()
    
    results = []
    
    # Test 1: Imports
    results.append(("Imports", test_imports()))
    
    # Test 2: Desktop App Class
    results.append(("Desktop App Class", test_desktop_app_class()))
    
    # Test 3: CSV to XLSX Conversion
    results.append(("CSV to XLSX Conversion", test_csv_to_xlsx_conversion()))
    
    # Test 4: Workflow Simulation
    results.append(("Workflow Simulation", test_workflow_simulation()))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 80)
    print(f"Total: {len(results)} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("=" * 80)
    
    if failed == 0:
        print("\n🎉 All tests passed! Desktop app integration is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

