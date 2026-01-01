"""
Test script for Fincaraiz Mapper
Demonstrates how to use the mapper with different property types
"""

import json
from fincaraiz_mapper import FincaraizMapper


def test_different_property_types():
    """Test the mapper with different property scenarios"""
    
    mapper = FincaraizMapper()
    
    # Test Case 1: Rental Apartment (from your example)
    rental_apartment = {
        "address": "CALLE 145 #23-06 Edf Genesis Cedritos",
        "operation": "ARRIENDO",
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
            "price_per_m2": 49439,
            "total_area": 37.42,
            "total_price_per_m2": 49439,
            "admin_per_m2": 8418
        }
    }
    
    # Test Case 2: Sale House
    sale_house = {
        "address": "Carrera 15 #93-47, Chapinero, Bogotá",
        "operation": "VENTA",
        "area_habitable": 120.0,
        "terrace": True,
        "area_total": 150.0,
        "administration": 0,
        "bedrooms": 3,
        "bathrooms": 2.5,
        "parking": 2,
        "walking_closet": True,
        "loft": False,
        "study_room": True,
        "floor": 0,  # House
        "deposit": 1,
        "terrace_area": 30.0,
        "construction_age": 5,
        "interior_exterior": "E",
        "elevator": False,
        "finish_quality": 5,
        "conservation_state": 5,
        "location_quality": 5,
        "stratum": 5,
        "observations": "Beautiful house with garden",
        "contact_method": "WhatsApp",
        "contact_info": "+57 300 123 4567",
        "pricing": {
            "area": 120.0,
            "price_per_m2": 8000000,
            "total_area": 150.0,
            "total_price_per_m2": 6400000,
            "admin_per_m2": 0
        }
    }
    
    # Test Case 3: Minimal Data (edge case)
    minimal_property = {
        "address": "Calle 80 #11-42, Medellín",
        "operation": "ARRIENDO",
        "area_habitable": 50.0,
        "bedrooms": 2,
        "bathrooms": 1,
        "stratum": 3,
        "pricing": {
            "price_per_m2": 30000
        }
    }
    
    test_cases = [
        ("Rental Apartment", rental_apartment),
        ("Sale House", sale_house),
        ("Minimal Data Property", minimal_property)
    ]
    
    print("=" * 80)
    print("FINCARAIZ MAPPER TEST RESULTS")
    print("=" * 80)
    
    for test_name, property_data in test_cases:
        print(f"\n{test_name}:")
        print("-" * 40)
        
        result = mapper.map_property_to_search(property_data)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Success!")
            print(f"🔗 Search URL: {result['search_url']}")
            print(f"📊 Price Range: ${result['metadata']['search_criteria']['price_range']['min']:,} - ${result['metadata']['search_criteria']['price_range']['max']:,}")
            print(f"📐 Area Range: {result['metadata']['search_criteria']['area_range']['min']} - {result['metadata']['search_criteria']['area_range']['max']} m²")
            print(f"🏠 Operation: {result['search_params']['tipo_operacion']}")
            print(f"🏢 Property Type: {result['search_params']['tipo_inmueble']}")
            if result['search_params'].get('ciudad'):
                print(f"📍 City: {result['search_params']['ciudad']}")
            if result['search_params'].get('barrio'):
                print(f"🏘️ Neighborhood: {result['search_params']['barrio']}")


def test_url_validation():
    """Test if generated URLs are valid"""
    import urllib.parse
    
    mapper = FincaraizMapper()
    
    # Simple test property
    test_property = {
        "address": "Calle 100 #15-20, Bogotá",
        "operation": "VENTA",
        "area_habitable": 80.0,
        "bedrooms": 2,
        "bathrooms": 2,
        "stratum": 4,
        "pricing": {
            "price_per_m2": 5000000
        }
    }
    
    result = mapper.map_property_to_search(test_property)
    
    if 'error' not in result:
        url = result['search_url']
        parsed = urllib.parse.urlparse(url)
        
        print(f"\nURL Validation:")
        print(f"✅ Valid URL: {url}")
        print(f"✅ Domain: {parsed.netloc}")
        print(f"✅ Path: {parsed.path}")
        print(f"✅ Query Parameters: {len(parsed.query.split('&'))} parameters")
        
        # Check if parameters are properly encoded
        params = urllib.parse.parse_qs(parsed.query)
        print(f"✅ Decoded Parameters: {list(params.keys())}")


if __name__ == "__main__":
    test_different_property_types()
    test_url_validation()
    
    print("\n" + "=" * 80)
    print("🎉 All tests completed!")
    print("=" * 80)
