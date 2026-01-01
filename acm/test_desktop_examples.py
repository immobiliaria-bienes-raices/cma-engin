#!/usr/bin/env python3
"""
Test the desktop app with example data from ejemplo_venta.csv
"""

import sys
import os
import json
import pandas as pd
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from real_estate_analytics.mappers.fincaraiz_mapper import FincaraizMapper
from real_estate_analytics.orchestrators.fincaraiz_orchestrator import FincaraizOrchestrator
from real_estate_analytics.converters.csv_converter import CSVConverter

def create_test_property_from_csv():
    """Create test property data based on the first property in ejemplo_venta.csv"""
    
    # Example 1: First property from CSV (row 9)
    example1 = {
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
    
    # Example 2: Second property from CSV (row 10)
    example2 = {
        "address": "CARRERA 17 No. 134-79",
        "operation": "VENTA", 
        "area_habitable": 38.0,
        "terrace": False,
        "area_total": 38.0,
        "administration": 50000,
        "bedrooms": 1,
        "bathrooms": 1.0,
        "parking": 1,
        "walking_closet": False,
        "loft": False,
        "study_room": False,
        "floor": 5,
        "deposit": 1,
        "terrace_area": 0,
        "construction_age": 23,
        "interior_exterior": "E",
        "elevator": True,
        "finish_quality": 4,
        "conservation_state": 4,
        "location_quality": 5,
        "stratum": 4,
        "observations": "",
        "contact_method": "C.C.",
        "contact_info": "3762-633829",
        "pricing": {
            "area": 38.0,
            "price_per_m2": 6578947.36842105,
            "total_area": 38.0,
            "total_price_per_m2": 6578947.36842105,
            "admin_per_m2": 1315.78947368421
        }
    }
    
    return example1, example2

def test_mapper_with_examples():
    """Test the mapper with example data"""
    print("=" * 60)
    print("TESTING MAPPER WITH EXAMPLE DATA")
    print("=" * 60)
    
    mapper = FincaraizMapper()
    example1, example2 = create_test_property_from_csv()
    
    # Test Example 1
    print("\n📋 Example 1:")
    print(f"Address: {example1['address']}")
    print(f"Operation: {example1['operation']}")
    print(f"Area: {example1['area_habitable']} m²")
    print(f"Price per m²: ${example1['pricing']['price_per_m2']:,.0f}")
    
    result1 = mapper.map_property_to_search(example1)
    if 'search_url' in result1:
        print(f"✅ Search URL: {result1['search_url']}")
        print(f"   Portal: {result1.get('portal', 'N/A')}")
        print(f"   Timestamp: {result1.get('timestamp', 'N/A')}")
    else:
        print(f"❌ Error: {result1.get('error', 'Unknown error')}")
    
    # Test Example 2
    print("\n📋 Example 2:")
    print(f"Address: {example2['address']}")
    print(f"Operation: {example2['operation']}")
    print(f"Area: {example2['area_habitable']} m²")
    print(f"Price per m²: ${example2['pricing']['price_per_m2']:,.0f}")
    
    result2 = mapper.map_property_to_search(example2)
    if 'search_url' in result2:
        print(f"✅ Search URL: {result2['search_url']}")
        print(f"   Portal: {result2.get('portal', 'N/A')}")
        print(f"   Timestamp: {result2.get('timestamp', 'N/A')}")
    else:
        print(f"❌ Error: {result2.get('error', 'Unknown error')}")
    
    return result1, result2

def test_orchestrator_with_examples():
    """Test the orchestrator with example URLs (mock mode)"""
    print("\n" + "=" * 60)
    print("TESTING ORCHESTRATOR WITH EXAMPLE DATA")
    print("=" * 60)
    
    orchestrator = FincaraizOrchestrator(delay_between_requests=0.1, max_retries=1)
    
    # Create mock CSV data that simulates what the orchestrator would scrape
    mock_properties = [
        {
            'title': 'Apartamento en Cedritos - Example 1',
            'price': '$260,000,000',
            'address': 'CARRERA 17 No. 134-79',
            'area': '37.42 m²',
            'bedrooms': '1 habitación',
            'bathrooms': '1 baño',
            'parking': '1 parqueadero',
            'stratum': 'Estrato 4',
            'amenities': 'Ascensor',
            'property_type': 'Apartamento',
            'operation': 'VENTA'
        },
        {
            'title': 'Apartamento en Cedritos - Example 2',
            'price': '$250,000,000',
            'address': 'CARRERA 17 No. 134-79',
            'area': '38 m²',
            'bedrooms': '1 habitación',
            'bathrooms': '1 baño',
            'parking': '1 parqueadero',
            'stratum': 'Estrato 4',
            'amenities': 'Ascensor',
            'property_type': 'Apartamento',
            'operation': 'VENTA'
        }
    ]
    
    # Save mock data to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mock_csv_filename = f"test_mock_properties_{timestamp}.csv"
    
    success = orchestrator.save_to_csv(mock_properties, mock_csv_filename)
    if success:
        print(f"✅ Mock CSV created: {mock_csv_filename}")
        print(f"   Properties: {len(mock_properties)}")
        return mock_csv_filename
    else:
        print("❌ Failed to create mock CSV")
        return None

def test_converter_with_examples():
    """Test the converter with example data"""
    print("\n" + "=" * 60)
    print("TESTING CONVERTER WITH EXAMPLE DATA")
    print("=" * 60)
    
    mapper = FincaraizMapper()
    converter = CSVConverter()
    
    # Create mock CSV data
    mock_csv_filename = test_orchestrator_with_examples()
    
    if mock_csv_filename and os.path.exists(mock_csv_filename):
        # Convert to standardized format
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        standardized_filename = f"test_standardized_{timestamp}.csv"
        
        result = converter.convert_csv_file(mock_csv_filename, standardized_filename)
        
        if result['success']:
            print(f"✅ Conversion successful!")
            print(f"   Input properties: {result['total_input_properties']}")
            print(f"   Converted properties: {result['converted_properties']}")
            print(f"   Conversion rate: {result['conversion_rate']:.2%}")
            print(f"   Output file: {result['output_file']}")
            
            # Show sample of converted data
            if os.path.exists(standardized_filename):
                df = pd.read_csv(standardized_filename)
                print(f"\n📊 Sample of converted data:")
                print(f"   Columns: {list(df.columns)}")
                if not df.empty:
                    sample = df.iloc[0]
                    print(f"   Address: {sample.get('address', 'N/A')}")
                    print(f"   Operation: {sample.get('operation', 'N/A')}")
                    print(f"   Area: {sample.get('area_habitable', 'N/A')} m²")
                    print(f"   Bedrooms: {sample.get('bedrooms', 'N/A')}")
                    print(f"   Price per m²: {sample.get('pricing', 'N/A')}")
            
            return standardized_filename
        else:
            print(f"❌ Conversion failed: {result.get('error', 'Unknown error')}")
            return None
    else:
        print("❌ No mock CSV file to convert")
        return None

def test_desktop_app_workflow():
    """Test the complete desktop app workflow"""
    print("\n" + "=" * 60)
    print("TESTING COMPLETE DESKTOP APP WORKFLOW")
    print("=" * 60)
    
    # Test mapper
    result1, result2 = test_mapper_with_examples()
    
    # Test converter
    standardized_file = test_converter_with_examples()
    
    # Summary
    print("\n" + "=" * 60)
    print("WORKFLOW TEST SUMMARY")
    print("=" * 60)
    
    print(f"✅ Mapper Test 1: {'PASS' if 'search_url' in result1 else 'FAIL'}")
    print(f"✅ Mapper Test 2: {'PASS' if 'search_url' in result2 else 'FAIL'}")
    print(f"✅ Converter Test: {'PASS' if standardized_file else 'FAIL'}")
    
    if 'search_url' in result1 and 'search_url' in result2 and standardized_file:
        print("\n🎉 All tests passed! Desktop app workflow is working correctly.")
        print("\nTo test the GUI:")
        print("1. Run: python3 desktop_app.py")
        print("2. Fill in the form with the example data")
        print("3. Click 'Procesar Propiedad'")
        print("4. Check the Results tab for output")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")

def main():
    """Run all tests"""
    print("Real Estate Analytics Desktop App - Example Data Test")
    test_desktop_app_workflow()

if __name__ == "__main__":
    main()
