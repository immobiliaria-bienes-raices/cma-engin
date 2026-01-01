#!/usr/bin/env python3
"""
Complete Real Estate Analytics Workflow Example

This example demonstrates the complete workflow:
1. Property Schema → Mapper → Search URL
2. Search URL → Orchestrator → Raw CSV
3. Raw CSV → CSV Converter → Standardized CSV
"""

import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from real_estate_analytics.mappers.fincaraiz_mapper import FincaraizMapper
from real_estate_analytics.orchestrators.fincaraiz_orchestrator import FincaraizOrchestrator
from real_estate_analytics.converters.csv_converter import CSVConverter


def main():
    """Run the complete real estate analytics workflow"""
    
    print("=" * 80)
    print("COMPLETE REAL ESTATE ANALYTICS WORKFLOW")
    print("=" * 80)
    
    # Initialize components
    mapper = FincaraizMapper()
    orchestrator = FincaraizOrchestrator(delay_between_requests=1.0, max_retries=3)
    converter = CSVConverter()
    
    # Test properties (same as mapper tests)
    test_properties = [
        {
            "address": "CALLE 145 #23-06 Edf Genesis Cedritos",
            "operation": "ARRIENDO",
            "area_habitable": 37.42,
            "bedrooms": 1,
            "bathrooms": 1.0,
            "stratum": 4,
            "pricing": {
                "price_per_m2": 49439,
                "area": 37.42
            }
        },
        {
            "address": "Carrera 15 #93-07, Bogotá",
            "operation": "VENTA",
            "area_habitable": 120.0,
            "bedrooms": 3,
            "bathrooms": 2.0,
            "stratum": 5,
            "elevator": True,
            "terrace": True,
            "walking_closet": True,
            "study_room": True,
            "loft": True,
            "parking": 2,
            "deposit": 1,
            "pricing": {
                "price_per_m2": 6000000,
                "area": 120.0
            }
        },
        {
            "address": "Calle 50 #80-40, Medellín",
            "operation": "ARRIENDO",
            "area_habitable": 50.0,
            "bedrooms": 2,
            "bathrooms": 1.0,
            "stratum": 3,
            "pricing": {
                "price_per_m2": 25000,
                "area": 50.0
            }
        }
    ]
    
    print("\n1. GENERATING SEARCH URLS WITH MAPPER")
    print("-" * 50)
    
    search_urls = []
    for i, property_data in enumerate(test_properties, 1):
        print(f"\nProperty {i}: {property_data['operation']} - {property_data['area_habitable']}m²")
        print(f"Address: {property_data['address']}")
        
        # Generate search URL
        result = mapper.map_property_to_search(property_data)
        
        if 'error' not in result:
            search_url = result['search_url']
            search_urls.append(search_url)
            print(f"✅ Search URL: {search_url}")
        else:
            print(f"❌ Error: {result['error']}")
    
    print(f"\n✅ Generated {len(search_urls)} valid search URLs")
    
    print("\n2. SCRAPING PROPERTIES WITH ORCHESTRATOR")
    print("-" * 50)
    
    raw_csv_files = []
    all_raw_properties = []
    
    for i, search_url in enumerate(search_urls, 1):
        print(f"\nScraping URL {i}:")
        print(f"URL: {search_url}")
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        raw_filename = f"raw_properties_{i}_{timestamp}.csv"
        
        # Process search URL
        result = orchestrator.process_search_url(search_url, raw_filename)
        
        if result['success']:
            properties = result['properties']
            all_raw_properties.extend(properties)
            raw_csv_files.append(result['csv_file'])
            
            print(f"✅ Found {len(properties)} properties")
            print(f"✅ Saved to: {result['csv_file']}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    print(f"\n✅ Total raw properties scraped: {len(all_raw_properties)}")
    print(f"✅ Raw CSV files created: {len(raw_csv_files)}")
    
    # Create combined raw CSV
    if all_raw_properties:
        print("\n3. CREATING COMBINED RAW CSV")
        print("-" * 50)
        
        combined_raw_filename = f"raw_all_properties_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        success = orchestrator.save_to_csv(all_raw_properties, combined_raw_filename)
        
        if success:
            print(f"✅ Combined raw CSV created: {combined_raw_filename}")
            raw_csv_files.append(combined_raw_filename)
        else:
            print("❌ Failed to create combined raw CSV")
    
    print("\n4. CONVERTING TO STANDARDIZED FORMAT")
    print("-" * 50)
    
    standardized_csv_files = []
    
    for i, raw_csv_file in enumerate(raw_csv_files, 1):
        print(f"\nConverting file {i}: {raw_csv_file}")
        
        # Generate standardized filename
        base_name = os.path.splitext(os.path.basename(raw_csv_file))[0]
        standardized_filename = f"standardized_{base_name}.csv"
        
        # Convert CSV file
        result = converter.convert_csv_file(raw_csv_file, standardized_filename)
        
        if result['success']:
            standardized_csv_files.append(result['output_file'])
            print(f"✅ Conversion successful!")
            print(f"   Input properties: {result['total_input_properties']}")
            print(f"   Converted properties: {result['converted_properties']}")
            print(f"   Conversion rate: {result['conversion_rate']:.2%}")
            print(f"   Output file: {result['output_file']}")
        else:
            print(f"❌ Conversion failed: {result.get('error', 'Unknown error')}")
    
    print(f"\n✅ Total standardized CSV files created: {len(standardized_csv_files)}")
    
    print("\n5. WORKFLOW SUMMARY")
    print("-" * 50)
    
    print(f"📊 Properties processed: {len(all_raw_properties)}")
    print(f"📄 Raw CSV files: {len(raw_csv_files)}")
    print(f"📄 Standardized CSV files: {len(standardized_csv_files)}")
    
    print("\nGenerated Files:")
    print("\nRaw CSV Files:")
    for csv_file in raw_csv_files:
        if os.path.exists(csv_file):
            print(f"  📄 {csv_file}")
    
    print("\nStandardized CSV Files:")
    for csv_file in standardized_csv_files:
        if os.path.exists(csv_file):
            print(f"  📄 {csv_file}")
    
    # Show sample of standardized data
    if standardized_csv_files:
        print(f"\nSample of standardized data from {standardized_csv_files[0]}:")
        try:
            import csv
            with open(standardized_csv_files[0], 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
                if rows:
                    sample = rows[0]
                    print(f"  Address: {sample['address']}")
                    print(f"  Operation: {sample['operation']}")
                    print(f"  Area: {sample['area_habitable']} m²")
                    print(f"  Bedrooms: {sample['bedrooms']}")
                    print(f"  Bathrooms: {sample['bathrooms']}")
                    print(f"  Stratum: {sample['stratum']}")
                    print(f"  Elevator: {sample['elevator']}")
                    print(f"  Terrace: {sample['terrace']}")
        except Exception as e:
            print(f"  Error reading sample: {e}")
    
    print("\n" + "=" * 80)
    print("🎉 COMPLETE WORKFLOW FINISHED SUCCESSFULLY!")
    print("=" * 80)
    
    print("\nNext Steps:")
    print("1. Use standardized CSV files for market analysis")
    print("2. Compare properties across different searches")
    print("3. Calculate market statistics and trends")
    print("4. Generate comparative market analysis reports")


if __name__ == "__main__":
    main()
