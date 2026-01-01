#!/usr/bin/env python3
"""
Test script for property-type-specific CSV generation

This script demonstrates the complete flow:
1. Mapper generates search URLs
2. Orchestrator extracts comprehensive property data
3. PropertyTypeCSVGenerator creates property-type-specific CSV files
"""

import sys
import os
sys.path.insert(0, 'src')

from real_estate_analytics.mappers.fincaraiz_mapper import FincaraizMapper
from real_estate_analytics.orchestrators.fincaraiz_orchestrator import FincaraizOrchestrator
from real_estate_analytics.outputs.property_type_csv_generator import PropertyTypeCSVGenerator
from datetime import datetime

def test_complete_flow():
    """Test the complete flow with property-type-specific CSV generation"""
    
    print("=== TESTING COMPLETE FLOW WITH PROPERTY-TYPE-SPECIFIC CSV ===\n")
    
    # Test data for different property types
    test_cases = [
        {
            'name': 'Apartment Test',
            'property_type': 'apartment',
            'form_data': {
                'address': 'CALLE 145 #23-06 Edf Genesis Cedritos',
                'operation': 'ARRIENDO',
                'property_type': 'Apartamento',
                'neighborhoods': ['Cedritos'],
                'area_total': 37.42,
                'bedrooms': 1,
                'bathrooms': 1.0,
                'stratum': 4,
                'pricing': {'price_per_m2': 49439},
                'publication_date': 'Últimos 30 días'
            }
        },
        {
            'name': 'House Test',
            'property_type': 'house',
            'form_data': {
                'address': 'CALLE 80 #15-20 Casa Cedritos',
                'operation': 'VENTA',
                'property_type': 'Casa',
                'neighborhoods': ['Cedritos', 'Niza'],
                'area_total': 120.0,
                'bedrooms': 3,
                'bathrooms': 2.0,
                'stratum': 5,
                'pricing': {'price_per_m2': 8000000},
                'publication_date': 'Últimos 30 días'
            }
        },
        {
            'name': 'Lote Test',
            'property_type': 'lote',
            'form_data': {
                'address': 'LOTE 15-20 Sector Norte',
                'operation': 'VENTA',
                'property_type': 'Lote',
                'neighborhoods': ['Cedritos'],
                'area_total': 500.0,
                'bedrooms': 0,
                'bathrooms': 0,
                'stratum': 4,
                'pricing': {'price_per_m2': 2000000},
                'publication_date': 'Últimos 30 días'
            }
        }
    ]
    
    # Initialize components
    mapper = FincaraizMapper()
    orchestrator = FincaraizOrchestrator(delay_between_requests=1.0, max_retries=2)
    csv_generator = PropertyTypeCSVGenerator()
    
    # Create output directory
    output_dir = '/tmp/property_type_test_output'
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    
    for test_case in test_cases:
        print(f"--- {test_case['name']} ---")
        
        try:
            # Step 1: Generate search URL
            print("1. Generating search URL...")
            search_result = mapper.map_property_to_search(test_case['form_data'])
            
            if 'error' in search_result:
                print(f"❌ Mapper Error: {search_result['error']}")
                continue
            
            print(f"✅ Search URL: {search_result['search_url']}")
            
            # Step 2: Scrape properties
            print("2. Scraping properties...")
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            raw_filename = os.path.join(output_dir, f'raw_{test_case["property_type"]}_{timestamp}.csv')
            
            scrape_result = orchestrator.process_search_url(search_result['search_url'], raw_filename)
            
            if not scrape_result['success']:
                print(f"❌ Scraping Error: {scrape_result.get('error', 'Unknown error')}")
                continue
            
            print(f"✅ Scraped {len(scrape_result['properties'])} properties")
            
            # Step 3: Generate property-type-specific CSV
            print("3. Generating property-type-specific CSV...")
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            specific_csv_filename = os.path.join(output_dir, f'{test_case["property_type"]}_specific_{timestamp}.csv')
            
            csv_result = csv_generator.generate_csv(
                scrape_result['properties'],
                specific_csv_filename,
                test_case['property_type']
            )
            
            if not csv_result['success']:
                print(f"❌ CSV Generation Error: {csv_result.get('error', 'Unknown error')}")
                continue
            
            print(f"✅ Generated {test_case['property_type']} CSV: {csv_result['properties_count']} properties")
            print(f"   Columns: {len(csv_result['columns'])}")
            print(f"   File: {specific_csv_filename}")
            
            # Show sample data
            if scrape_result['properties']:
                first_prop = scrape_result['properties'][0]
                print(f"   Sample extracted fields:")
                for key in ['title', 'price', 'area', 'bedrooms', 'bathrooms', 'stratum', 'price_per_m2']:
                    value = first_prop.get(key, 'N/A')
                    print(f"     {key}: {value}")
            
            results.append({
                'test_case': test_case['name'],
                'property_type': test_case['property_type'],
                'properties_count': len(scrape_result['properties']),
                'csv_file': specific_csv_filename,
                'success': True
            })
            
        except Exception as e:
            print(f"❌ Error in {test_case['name']}: {str(e)}")
            results.append({
                'test_case': test_case['name'],
                'property_type': test_case['property_type'],
                'error': str(e),
                'success': False
            })
        
        print()
    
    # Summary
    print("=== SUMMARY ===")
    successful_tests = [r for r in results if r['success']]
    failed_tests = [r for r in results if not r['success']]
    
    print(f"✅ Successful tests: {len(successful_tests)}")
    for result in successful_tests:
        print(f"   - {result['test_case']}: {result['properties_count']} properties")
    
    if failed_tests:
        print(f"❌ Failed tests: {len(failed_tests)}")
        for result in failed_tests:
            print(f"   - {result['test_case']}: {result.get('error', 'Unknown error')}")
    
    print(f"\nOutput directory: {output_dir}")
    print("=== TEST COMPLETE ===")

if __name__ == "__main__":
    test_complete_flow()
