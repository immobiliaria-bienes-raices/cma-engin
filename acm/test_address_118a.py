#!/usr/bin/env python3
"""
Test ACM System with Address "cll 118A #13-42"

This script tests the ACM real estate analytics system with a specific property:
- Address: cll 118A #13-42
- Operation: VENTA
- Area: 95 m²
- Bedrooms: 3
- Bathrooms: 3
- Construction Age: 16 years (antiguedad)
- Price: 600,000,000 COP (600 millones)
"""

import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from real_estate_analytics.mappers.fincaraiz_mapper import FincaraizMapper
from real_estate_analytics.orchestrators.fincaraiz_orchestrator import FincaraizOrchestrator
from real_estate_analytics.converters.csv_converter import CSVConverter


def create_property_data():
    """Create property data dictionary for cll 118A #13-42"""
    
    # Property details
    total_price = 600000000  # 600 millones COP
    area = 95.0  # m²
    price_per_m2 = total_price / area  # ~6,315,789 COP/m²
    
    property_data = {
        "address": "cll 118A #13-42",
        "operation": "VENTA",
        "area_habitable": area,
        "bedrooms": 3,
        "bathrooms": 3.0,
        "construction_age": 16,  # 16 years old (antiguedad)
        "stratum": 4,  # Default stratum, adjust if known
        "parking": 1,  # Default parking, adjust if known
        "pricing": {
            "area": area,
            "price_per_m2": price_per_m2,
            "total_area": area,
            "total_price_per_m2": price_per_m2,
            "admin_per_m2": 0  # Unknown administration fee
        }
    }
    
    return property_data


def test_mapper(property_data):
    """Test the mapper component"""
    print("\n" + "=" * 80)
    print("1. TESTING MAPPER COMPONENT")
    print("=" * 80)
    
    mapper = FincaraizMapper()
    
    print(f"\nProperty Details:")
    print(f"  Address: {property_data['address']}")
    print(f"  Operation: {property_data['operation']}")
    print(f"  Area: {property_data['area_habitable']} m²")
    print(f"  Bedrooms: {property_data['bedrooms']}")
    print(f"  Bathrooms: {property_data['bathrooms']}")
    print(f"  Construction Age: {property_data.get('construction_age', 'N/A')} years")
    print(f"  Price per m²: ${property_data['pricing']['price_per_m2']:,.2f} COP/m²")
    print(f"  Total Price: ${property_data['pricing']['price_per_m2'] * property_data['area_habitable']:,.0f} COP")
    
    # Generate search URL
    result = mapper.map_property_to_search(property_data)
    
    if 'error' in result:
        print(f"\n❌ Error generating search URL: {result['error']}")
        return None
    else:
        search_url = result['search_url']
        print(f"\n✅ Search URL generated successfully!")
        print(f"   URL: {search_url}")
        print(f"   Portal: {result.get('portal', 'N/A')}")
        print(f"   Timestamp: {result.get('timestamp', 'N/A')}")
        return search_url


def test_orchestrator(search_url):
    """Test the orchestrator component - scrapes actual property listings"""
    print("\n" + "=" * 80)
    print("2. TESTING ORCHESTRATOR COMPONENT - Scraping Real Properties")
    print("=" * 80)
    
    if not search_url:
        print("\n⚠️  Skipping orchestrator test - no search URL available")
        return None
    
    orchestrator = FincaraizOrchestrator(delay_between_requests=1.0, max_retries=2)
    
    print(f"\nScraping properties from:")
    print(f"  URL: {search_url}")
    
    # Generate output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_filename = f"raw_properties_118a_{timestamp}.csv"
    
    # Process search URL
    result = orchestrator.process_search_url(search_url, raw_filename)
    
    if result['success']:
        properties = result['properties']
        print(f"\n✅ Scraping successful!")
        print(f"   Properties found: {len(properties)}")
        print(f"   Output file: {result['csv_file']}")
        
        # Display sample of scraped properties
        if properties:
            print(f"\n   Sample of scraped properties:")
            for i, prop in enumerate(properties[:3], 1):  # Show first 3 properties
                print(f"   {i}. {prop.get('title', 'N/A')}")
                print(f"      Price: {prop.get('price', 'N/A')}")
                print(f"      Address: {prop.get('address', 'N/A')}")
                if i < min(3, len(properties)):
                    print()
        
        return result['csv_file']
    else:
        print(f"\n❌ Scraping failed: {result.get('error', 'Unknown error')}")
        return None


def test_converter(raw_csv_file):
    """Test the converter component - converts scraped data to standardized format"""
    print("\n" + "=" * 80)
    print("3. TESTING CONVERTER COMPONENT - Converting Scraped Data")
    print("=" * 80)
    
    if not raw_csv_file or not os.path.exists(raw_csv_file):
        print("\n⚠️  Skipping converter test - no raw CSV file available")
        return None
    
    converter = CSVConverter()
    
    print(f"\nConverting CSV file:")
    print(f"  Input: {raw_csv_file}")
    
    # Generate standardized filename
    base_name = os.path.splitext(os.path.basename(raw_csv_file))[0]
    standardized_filename = f"standardized_{base_name}.csv"
    
    # Convert CSV file
    result = converter.convert_csv_file(raw_csv_file, standardized_filename)
    
    if result['success']:
        print(f"\n✅ Conversion successful!")
        print(f"   Input properties: {result['total_input_properties']}")
        print(f"   Converted properties: {result['converted_properties']}")
        print(f"   Conversion rate: {result['conversion_rate']:.2%}")
        print(f"   Output file: {result['output_file']}")
        return result['output_file']
    else:
        print(f"\n❌ Conversion failed: {result.get('error', 'Unknown error')}")
        return None


def display_results(property_data, search_url, raw_csv_file, standardized_csv_file):
    """Display final test results"""
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    
    print(f"\n📋 Property Tested:")
    print(f"   Address: {property_data['address']}")
    print(f"   Operation: {property_data['operation']}")
    print(f"   Area: {property_data['area_habitable']} m²")
    print(f"   Bedrooms: {property_data['bedrooms']}")
    print(f"   Bathrooms: {property_data['bathrooms']}")
    print(f"   Construction Age: {property_data.get('construction_age', 'N/A')} years")
    
    print(f"\n🔗 Generated Search URL:")
    if search_url:
        print(f"   ✅ {search_url}")
    else:
        print(f"   ❌ No URL generated")
    
    print(f"\n📄 Generated Files:")
    if raw_csv_file and os.path.exists(raw_csv_file):
        print(f"   ✅ Raw CSV: {raw_csv_file}")
    else:
        print(f"   ⚠️  No raw CSV file generated")
    
    if standardized_csv_file and os.path.exists(standardized_csv_file):
        print(f"   ✅ Standardized CSV: {standardized_csv_file}")
    else:
        print(f"   ⚠️  No standardized CSV file generated")
    
    print("\n" + "=" * 80)
    if search_url:
        print("✅ MAPPER TEST: PASSED")
    else:
        print("❌ MAPPER TEST: FAILED")
    
    if raw_csv_file:
        print("✅ ORCHESTRATOR TEST: PASSED")
    else:
        print("⚠️  ORCHESTRATOR TEST: SKIPPED OR FAILED")
    
    if standardized_csv_file:
        print("✅ CONVERTER TEST: PASSED")
    else:
        print("⚠️  CONVERTER TEST: SKIPPED OR FAILED")
    print("=" * 80)


def main():
    """Main test function"""
    print("=" * 80)
    print("ACM SYSTEM TEST - Address: cll 118A #13-42")
    print("=" * 80)
    
    # Create property data
    property_data = create_property_data()
    
    # Test mapper
    search_url = test_mapper(property_data)
    
    # Test orchestrator - scrape actual property listings from Fincaraiz
    raw_csv_file = None
    if search_url:
        print("\n⚠️  Starting web scraping - this will fetch real property data from Fincaraiz")
        print("    This may take a few moments...")
        raw_csv_file = test_orchestrator(search_url)
    
    # Test converter - convert scraped data to standardized format
    standardized_csv_file = None
    if raw_csv_file:
        standardized_csv_file = test_converter(raw_csv_file)
    
    # Display results
    display_results(property_data, search_url, raw_csv_file, standardized_csv_file)
    
    print("\n🎉 Test completed!")
    print("\nResults:")
    if standardized_csv_file:
        print(f"✅ Found and processed real property listings from Fincaraiz")
        print(f"✅ Standardized data saved to: {standardized_csv_file}")
        print("\nYou can now:")
        print("1. Review the standardized CSV file with actual property data")
        print("2. Compare properties found with similar characteristics")
        print("3. Use the data for market analysis")
    elif raw_csv_file:
        print(f"✅ Scraped properties saved to: {raw_csv_file}")
        print("⚠️  Conversion step may have failed - check the raw CSV file")
    elif search_url:
        print(f"✅ Generated search URL: {search_url}")
        print("⚠️  Scraping step failed - check error messages above")
    else:
        print("❌ Test failed - could not generate search URL")


if __name__ == "__main__":
    main()

