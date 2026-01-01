#!/usr/bin/env python3
"""
Test script for Excel generation
"""

import sys
import os
sys.path.insert(0, 'src')

from real_estate_analytics.mappers.fincaraiz_mapper import FincaraizMapper
from real_estate_analytics.orchestrators.fincaraiz_orchestrator import FincaraizOrchestrator
from real_estate_analytics.outputs.property_type_csv_generator import PropertyTypeCSVGenerator
from real_estate_analytics.formatters.property_type_analysis_formatter import PropertyTypeAnalysisFormatter
from datetime import datetime

def test_excel_generation():
    """Test Excel generation functionality"""
    
    print("=== TESTING EXCEL GENERATION ===\n")
    
    # Test apartment property type
    form_data_apartment = {
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
    
    # Initialize components
    mapper = FincaraizMapper()
    orchestrator = FincaraizOrchestrator(delay_between_requests=1.0, max_retries=2)
    csv_generator = PropertyTypeCSVGenerator()
    analysis_formatter = PropertyTypeAnalysisFormatter()
    
    # Generate search URL
    search_result = mapper.map_property_to_search(form_data_apartment)
    print(f"✅ Search URL: {search_result['search_url']}")
    
    # Scrape properties
    output_dir = '/tmp/excel_test'
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    raw_filename = os.path.join(output_dir, f'raw_apartment_{timestamp}.csv')
    
    scrape_result = orchestrator.process_search_url(search_result['search_url'], raw_filename)
    print(f"✅ Scraped {len(scrape_result['properties'])} properties")
    
    # Generate property-type-specific CSV
    property_type = 'apartment'
    specific_csv_filename = os.path.join(output_dir, f'apartment_specific_{timestamp}.csv')
    csv_result = csv_generator.generate_csv(scrape_result['properties'], specific_csv_filename, property_type)
    
    if csv_result['success']:
        print(f"✅ Generated {csv_result['property_type']} CSV: {csv_result['properties_count']} properties")
        
        # Read the generated CSV for analysis
        import csv
        with open(specific_csv_filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            properties_for_analysis = list(reader)
        
        print(f"✅ Read {len(properties_for_analysis)} properties for analysis")
        
        # Test the Excel generation
        analysis_result = analysis_formatter.format_analysis_files(
            properties_for_analysis,
            form_data_apartment['address'],
            output_dir,
            f'analisis_apartment_{timestamp}',
            'Bogotá',
            property_type
        )
        
        if analysis_result['success']:
            print(f"✅ Analysis CSV generated: {analysis_result['csv_file']}")
            print(f"✅ Analysis Excel generated: {analysis_result['excel_file']}")
            avg_price = analysis_result.get('average_price', 0)
            print(f"✅ Average price: ${avg_price:,.0f}")
            print(f"✅ Property type: {analysis_result['property_type']}")
            
            # Check if Excel file exists and has content
            excel_file = analysis_result['excel_file']
            if os.path.exists(excel_file):
                file_size = os.path.getsize(excel_file)
                print(f"✅ Excel file exists: {excel_file}")
                print(f"✅ Excel file size: {file_size} bytes")
            else:
                print(f"❌ Excel file not found: {excel_file}")
        else:
            print(f"❌ Analysis Error: {analysis_result.get('error', 'Unknown error')}")
            if 'csv_error' in analysis_result:
                print(f"   CSV Error: {analysis_result['csv_error']}")
            if 'excel_error' in analysis_result:
                print(f"   Excel Error: {analysis_result['excel_error']}")
    else:
        print(f"❌ CSV Generation Error: {csv_result.get('error', 'Unknown error')}")
    
    print("\n=== EXCEL GENERATION TEST COMPLETE ===")

if __name__ == "__main__":
    test_excel_generation()
