#!/usr/bin/env python3
"""
Demonstration script for the Real Estate Analytics Desktop App
Shows how to use the app with example data from ejemplo_venta.csv
"""

import sys
import os
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from real_estate_analytics.mappers.fincaraiz_mapper import FincaraizMapper
from real_estate_analytics.orchestrators.fincaraiz_orchestrator import FincaraizOrchestrator
from real_estate_analytics.converters.csv_converter import CSVConverter

def create_example_properties():
    """Create example properties based on ejemplo_venta.csv"""
    
    # Example 1: First property from CSV
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
    
    # Example 2: Second property from CSV
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
    
    return [example1, example2]

def demonstrate_workflow():
    """Demonstrate the complete workflow with example data"""
    print("=" * 80)
    print("REAL ESTATE ANALYTICS DESKTOP APP - DEMONSTRATION")
    print("=" * 80)
    
    # Initialize components
    mapper = FincaraizMapper()
    orchestrator = FincaraizOrchestrator(delay_between_requests=0.1, max_retries=1)
    converter = CSVConverter()
    
    # Get example properties
    examples = create_example_properties()
    
    print(f"\n📋 Processing {len(examples)} example properties...")
    
    # Process each example
    for i, example in enumerate(examples, 1):
        print(f"\n{'='*60}")
        print(f"PROCESSING EXAMPLE {i}")
        print(f"{'='*60}")
        
        print(f"Address: {example['address']}")
        print(f"Operation: {example['operation']}")
        print(f"Area: {example['area_habitable']} m²")
        print(f"Price per m²: ${example['pricing']['price_per_m2']:,.0f}")
        print(f"Bedrooms: {example['bedrooms']}")
        print(f"Bathrooms: {example['bathrooms']}")
        print(f"Stratum: {example['stratum']}")
        
        # Step 1: Generate search URL
        print(f"\n1️⃣ Generating search URL...")
        mapper_result = mapper.map_property_to_search(example)
        
        if 'search_url' in mapper_result:
            print(f"✅ Search URL generated:")
            print(f"   {mapper_result['search_url']}")
        else:
            print(f"❌ Error generating search URL: {mapper_result.get('error', 'Unknown error')}")
            continue
        
        # Step 2: Create mock CSV data (simulating web scraping)
        print(f"\n2️⃣ Creating mock CSV data...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        mock_csv_filename = f"demo_example_{i}_{timestamp}.csv"
        
        # Create mock property data
        mock_properties = [{
            'title': f'Apartamento en Cedritos - Example {i}',
            'price': f'${example["pricing"]["price_per_m2"] * example["area_habitable"]:,.0f}',
            'address': example['address'],
            'area': f'{example["area_habitable"]} m²',
            'bedrooms': f'{example["bedrooms"]} habitación' + ('es' if example["bedrooms"] > 1 else ''),
            'bathrooms': f'{example["bathrooms"]} baño' + ('s' if example["bathrooms"] > 1 else ''),
            'parking': f'{example["parking"]} parqueadero' + ('s' if example["parking"] > 1 else ''),
            'stratum': f'Estrato {example["stratum"]}',
            'amenities': 'Ascensor' if example['elevator'] else '',
            'property_type': 'Apartamento',
            'operation': example['operation']
        }]
        
        # Save mock data
        success = orchestrator.save_to_csv(mock_properties, mock_csv_filename)
        if success:
            print(f"✅ Mock CSV created: {mock_csv_filename}")
        else:
            print(f"❌ Failed to create mock CSV")
            continue
        
        # Step 3: Convert to standardized format
        print(f"\n3️⃣ Converting to standardized format...")
        standardized_filename = f"demo_standardized_{i}_{timestamp}.csv"
        convert_result = converter.convert_csv_file(mock_csv_filename, standardized_filename)
        
        if convert_result['success']:
            print(f"✅ Conversion successful!")
            print(f"   Input properties: {convert_result['total_input_properties']}")
            print(f"   Converted properties: {convert_result['converted_properties']}")
            print(f"   Conversion rate: {convert_result['conversion_rate']:.2%}")
            print(f"   Output file: {convert_result['output_file']}")
        else:
            print(f"❌ Conversion failed: {convert_result.get('error', 'Unknown error')}")
            continue
        
        print(f"\n✅ Example {i} processed successfully!")
    
    print(f"\n{'='*80}")
    print("DEMONSTRATION COMPLETED")
    print(f"{'='*80}")
    
    print(f"\n📊 Summary:")
    print(f"   • Processed {len(examples)} example properties")
    print(f"   • Generated search URLs for Fincaraiz")
    print(f"   • Created mock CSV data")
    print(f"   • Converted to standardized format")
    
    print(f"\n🎯 Next Steps:")
    print(f"   1. Run the desktop app: python3 desktop_app.py")
    print(f"   2. Fill in the form with the example data")
    print(f"   3. Click 'Procesar Propiedad' to see the workflow in action")
    print(f"   4. Check the Results tab for processing logs and output files")
    
    print(f"\n📁 Generated Files:")
    # List generated files
    for file in os.listdir('.'):
        if file.startswith('demo_') and file.endswith('.csv'):
            print(f"   📄 {file}")

def main():
    """Main demonstration function"""
    print("Real Estate Analytics Desktop App - Demonstration")
    print("This script demonstrates the workflow with example data from ejemplo_venta.csv")
    print()
    
    try:
        demonstrate_workflow()
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
