#!/usr/bin/env python3
"""
Fincaraiz Workflow Example

This example demonstrates the complete workflow:
1. Property Schema → Mapper → Search URL
2. Search URL → Orchestrator → CSV Data
"""

import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from real_estate_analytics.mappers.fincaraiz_mapper import FincaraizMapper
from real_estate_analytics.orchestrators.fincaraiz_orchestrator import FincaraizOrchestrator


def main():
    """Run the complete Fincaraiz workflow example"""
    
    print("=" * 80)
    print("FINCARAIZ COMPLETE WORKFLOW EXAMPLE")
    print("=" * 80)
    
    # Initialize components
    mapper = FincaraizMapper()
    orchestrator = FincaraizOrchestrator(delay_between_requests=1.0, max_retries=3)
    
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
            
            # Show search parameters
            search_params = result['search_params']
            print(f"   Price Range: ${search_params.get('precio_min', 0):,} - ${search_params.get('precio_max', 0):,}")
            print(f"   Area Range: {search_params.get('area_min', 0)} - {search_params.get('area_max', 0)} m²")
            print(f"   Bedrooms: {search_params.get('bedrooms', 0)}")
            print(f"   Bathrooms: {search_params.get('bathrooms', 0)}")
        else:
            print(f"❌ Error: {result['error']}")
    
    print(f"\n✅ Generated {len(search_urls)} valid search URLs")
    
    print("\n2. SCRAPING PROPERTIES WITH ORCHESTRATOR")
    print("-" * 50)
    
    all_properties = []
    csv_files = []
    
    for i, search_url in enumerate(search_urls, 1):
        print(f"\nScraping URL {i}:")
        print(f"URL: {search_url}")
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"fincaraiz_properties_{i}_{timestamp}.csv"
        
        # Process search URL
        result = orchestrator.process_search_url(search_url, output_filename)
        
        if result['success']:
            properties = result['properties']
            all_properties.extend(properties)
            csv_files.append(result['csv_file'])
            
            print(f"✅ Found {len(properties)} properties")
            print(f"✅ Saved to: {result['csv_file']}")
            
            # Show sample properties
            for j, prop in enumerate(properties[:2], 1):  # Show first 2 properties
                print(f"   Property {j}: {prop.get('title', 'N/A')} - {prop.get('price', 'N/A')}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    print(f"\n✅ Total properties scraped: {len(all_properties)}")
    print(f"✅ CSV files created: {len(csv_files)}")
    
    # Create combined CSV
    if all_properties:
        print("\n3. CREATING COMBINED CSV")
        print("-" * 50)
        
        combined_filename = f"fincaraiz_all_properties_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        success = orchestrator.save_to_csv(all_properties, combined_filename)
        
        if success:
            print(f"✅ Combined CSV created: {combined_filename}")
            print(f"✅ Total properties in combined file: {len(all_properties)}")
        else:
            print("❌ Failed to create combined CSV")
    
    print("\n" + "=" * 80)
    print("🎉 WORKFLOW COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    
    print("\nGenerated Files:")
    for csv_file in csv_files:
        if os.path.exists(csv_file):
            print(f"  📄 {csv_file}")
    
    if all_properties and os.path.exists(combined_filename):
        print(f"  📄 {combined_filename}")
    
    print(f"\nTotal Properties Found: {len(all_properties)}")
    print(f"CSV Files Created: {len(csv_files) + (1 if all_properties else 0)}")


if __name__ == "__main__":
    main()
