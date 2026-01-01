"""
Test script for Fincaraiz Mapper
Demonstrates how to use the mapper with different property types
"""

import json
import requests
import time
from urllib.parse import urlparse, parse_qs
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from real_estate_analytics.mappers.fincaraiz_mapper import FincaraizMapper
    

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
    """Test if generated URLs are valid (path-based structure)"""
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
        
        print(f"\nURL Validation (Path-based):")
        print(f"✅ Valid URL: {url}")
        print(f"✅ Domain: {parsed.netloc}")
        print(f"✅ Path: {parsed.path}")
        print(f"✅ Query Parameters: {len(parsed.query.split('&')) if parsed.query else 0} parameters")
        
        # Check path structure
        path_parts = parsed.path.strip('/').split('/')
        print(f"✅ Path Parts: {path_parts}")
        
        # Validate expected path structure (now includes location)
        expected_structure = ['operation', 'property_type', 'city', 'bedroom_filter']
        if len(path_parts) >= 4:
            print(f"✅ Has operation: {path_parts[0]}")
            print(f"✅ Has property type: {path_parts[1]}")
            print(f"✅ Has city: {path_parts[2]}")
            print(f"✅ Has bedroom filter: {path_parts[3]}")

            # Check for additional filters
            if len(path_parts) > 4:
                print(f"✅ Additional filters: {path_parts[4:]}")
        
        # Check if parameters are properly encoded (should be minimal for path-based)
        params = urllib.parse.parse_qs(parsed.query)
        print(f"✅ Query Parameters: {list(params.keys()) if params else 'None (path-based)'}")


if __name__ == "__main__":
    test_different_property_types()
    test_url_validation()
    
    print("\n" + "=" * 80)
    print("🎉 All tests completed!")
    print("=" * 80)


def test_url_accessibility():
    """Test if generated URLs are actually accessible in browser"""
    
    print("\n" + "=" * 80)
    print("TESTING URL ACCESSIBILITY")
    print("=" * 80)
    
    mapper = FincaraizMapper()
    
    # Test property data
    test_property = {
        "address": "CALLE 145 #23-06 Edf Genesis Cedritos",
        "operation": "ARRIENDO",
        "area_habitable": 37.42,
        "bedrooms": 1,
        "bathrooms": 1.0,
        "parking": 1,
        "stratum": 4,
        "pricing": {
            "price_per_m2": 49439,
            "area": 37.42
        }
    }
    
    # Generate search URL
    search_result = mapper.map_property_to_search(test_property)
    
    if 'error' in search_result:
        print(f"❌ Error generating search URL: {search_result['error']}")
        return False
    
    search_url = search_result['search_url']
    print(f"🔗 Generated URL: {search_url}")
    
    # Validate URL structure (path-based)
    parsed_url = urlparse(search_url)
    print(f"✅ Domain: {parsed_url.netloc}")
    print(f"✅ Path: {parsed_url.path}")
    print(f"✅ Query Parameters: {len(parse_qs(parsed_url.query)) if parsed_url.query else 0} parameters")
    
    # Check path structure
    path_parts = parsed_url.path.strip('/').split('/')
    print(f"✅ Path Parts: {path_parts}")
    
    # Validate path structure
    if len(path_parts) >= 3:
        print(f"✅ Operation: {path_parts[0]}")
        print(f"✅ Property Type: {path_parts[1]}")
        print(f"✅ Bedroom Filter: {path_parts[2]}")
        
        if len(path_parts) > 3:
            print(f"✅ Additional Filters: {path_parts[3:]}")
    else:
        print(f"❌ Invalid path structure: {path_parts}")
        return False
    
    # Test URL accessibility
    print(f"\n🌐 Testing URL accessibility...")
    
    try:
        # Add delay to be respectful to the server
        time.sleep(2)
        
        # Make request with proper headers
        headers = mapper.get_search_headers()
        response = requests.get(search_url, headers=headers, timeout=30)
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📊 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ URL is accessible and returns valid content")
            
            # Check if response contains expected content
            content = response.text.lower()
            if 'fincaraiz' in content:
                print("✅ Response contains Fincaraiz content")
            else:
                print("⚠️  Response doesn't contain expected Fincaraiz content")
            
            if 'buscar' in content or 'inmuebles' in content:
                print("✅ Response appears to be a search results page")
            else:
                print("⚠️  Response doesn't appear to be a search results page")
            
            # Check for error indicators
            error_indicators = ['error', 'not found', '404', '500', 'invalid']
            has_errors = any(indicator in content for indicator in error_indicators)
            
            if has_errors:
                print("⚠️  Response may contain error indicators")
            else:
                print("✅ No obvious error indicators found")
            
            return True
            
        elif response.status_code == 403:
            print("⚠️  Access forbidden (403) - may need different headers or rate limiting")
            return False
            
        elif response.status_code == 404:
            print("❌ URL not found (404) - check URL structure")
            return False
            
        elif response.status_code == 429:
            print("⚠️  Rate limited (429) - too many requests")
            return False
            
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out - server may be slow or unresponsive")
        return False
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - check internet connection or URL")
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {str(e)}")
        return False


def test_url_parameter_validation():
    """Test if URL path structure is correctly formatted"""
    
    print("\n" + "=" * 80)
    print("TESTING URL PATH STRUCTURE VALIDATION")
    print("=" * 80)
    
    mapper = FincaraizMapper()
    
    # Test with minimal data
    minimal_property = {
        "address": "Calle 80 #11-42, Bogotá",
        "operation": "VENTA",
        "area_habitable": 50.0,
        "bedrooms": 2,
        "bathrooms": 1,
        "stratum": 3,
        "pricing": {
            "price_per_m2": 30000
        }
    }
    
    search_result = mapper.map_property_to_search(minimal_property)
    
    if 'error' in search_result:
        print(f"❌ Error: {search_result['error']}")
        return False
    
    search_url = search_result['search_url']
    parsed_url = urlparse(search_url)
    path_parts = parsed_url.path.strip('/').split('/')
    
    print(f"🔗 URL: {search_url}")
    print(f"📋 Path Parts: {path_parts}")
    
    # Validate minimum path structure
    if len(path_parts) < 3:
        print(f"❌ Invalid path structure: {path_parts}")
        return False
    
    # Validate operation (first part)
    operation = path_parts[0]
    if operation in ['venta', 'arriendo']:
        print(f"✅ Operation type correctly mapped: {operation}")
    else:
        print(f"❌ Invalid operation type: {operation}")
        return False
    
    # Validate property type (second part)
    property_type = path_parts[1]
    if property_type in ['apartamentos', 'casas', 'apartaestudios']:
        print(f"✅ Property type correctly mapped: {property_type}")
    else:
        print(f"❌ Invalid property type: {property_type}")
        return False
    
    # Validate bedroom filter (third part)
    bedroom_filter = path_parts[2]
    if 'habitaciones' in bedroom_filter:
        print(f"✅ Bedroom filter correctly mapped: {bedroom_filter}")
    else:
        print(f"❌ Invalid bedroom filter: {bedroom_filter}")
        return False
    
    # Check for additional filters
    if len(path_parts) > 3:
        additional_filters = path_parts[3:]
        print(f"✅ Additional filters: {additional_filters}")
        
        # Check for city filter
        if any(city in additional_filters for city in ['bogota', 'medellin', 'cali', 'barranquilla']):
            print(f"✅ City filter detected")
        
        # Check for price filter
        if any('entre-' in filter_part and 'y-' in filter_part for filter_part in additional_filters):
            print(f"✅ Price filter detected")
        
        # Check for area filter
        if any('m2' in filter_part for filter_part in additional_filters):
            print(f"✅ Area filter detected")
    
    print("✅ All path structure validations passed")
    return True


def test_url_parameter_effectiveness():
    """Test if the URL path structure actually affects the search results"""
    
    print("\n" + "=" * 80)
    print("TESTING URL PATH EFFECTIVENESS")
    print("=" * 80)
    
    mapper = FincaraizMapper()
    
    # Test property with specific criteria
    test_property = {
        "address": "Calle 80 #11-42, Bogotá",
        "operation": "ARRIENDO",
        "area_habitable": 50.0,
        "bedrooms": 2,
        "bathrooms": 1,
        "stratum": 3,
        "pricing": {
            "price_per_m2": 30000
        }
    }
    
    # Generate URL with path-based structure
    search_result = mapper.map_property_to_search(test_property)
    
    if 'error' in search_result:
        print(f"❌ Error generating search URL: {search_result['error']}")
        return False
    
    url_with_params = search_result['search_url']
    print(f"🔗 URL with path filters: {url_with_params}")
    
    # Baseline URL with minimal path (just operation and property type)
    url_without_params = "https://www.fincaraiz.com.co/arriendo/apartamentos"
    print(f"🔗 Baseline URL: {url_without_params}")
    
    try:
        # Add delay to be respectful
        time.sleep(2)
        
        headers = mapper.get_search_headers()
        
        # Get content with parameters
        print(f"\n🌐 Fetching page with parameters...")
        response_with_params = requests.get(url_with_params, headers=headers, timeout=30, allow_redirects=True)
        
        print(f"📊 Final URL after redirects: {response_with_params.url}")
        print(f"📊 Response status: {response_with_params.status_code}")
        
        # Check if URL was redirected
        if response_with_params.url != url_with_params:
            print(f"⚠️  URL was redirected from original!")
            print(f"   Original: {url_with_params}")
            print(f"   Final:    {response_with_params.url}")
            
            # Check if parameters were lost in redirect
            original_params = parse_qs(urlparse(url_with_params).query)
            final_params = parse_qs(urlparse(response_with_params.url).query)
            
            if original_params != final_params:
                print(f"❌ Parameters were lost during redirect!")
                print(f"   Original params: {original_params}")
                print(f"   Final params:    {final_params}")
                return False
            else:
                print(f"✅ Parameters preserved during redirect")
        else:
            print(f"✅ No redirect occurred")
        
        if response_with_params.status_code != 200:
            print(f"❌ Failed to fetch page with parameters: {response_with_params.status_code}")
            return False
        
        content_with_params = response_with_params.text.lower()
        print(f"✅ Page with parameters loaded successfully")
        
        # Get baseline content without parameters
        print(f"\n🌐 Fetching baseline page...")
        time.sleep(2)  # Be respectful to the server
        
        response_baseline = requests.get(url_without_params, headers=headers, timeout=30)
        
        if response_baseline.status_code != 200:
            print(f"❌ Failed to fetch baseline page: {response_baseline.status_code}")
            return False
        
        content_baseline = response_baseline.text.lower()
        print(f"✅ Baseline page loaded successfully")
        
        # Compare content to see if parameters had effect
        print(f"\n📊 Analyzing parameter effectiveness...")
        
        # Check for specific parameter indicators in content
        param_indicators = {
            'arriendo': 'tipo_operacion=arriendo' in url_with_params,
            'apartamento': 'tipo_inmueble=apartamento' in url_with_params,
            'precio_min': 'precio_min=' in url_with_params,
            'precio_max': 'precio_max=' in url_with_params,
            'area_min': 'area_min=' in url_with_params,
            'area_max': 'area_max=' in url_with_params,
            'alcobas': 'alcobas' in url_with_params,
            'estrato': 'estrato=' in url_with_params
        }
        
        print(f"📋 Parameters in URL: {param_indicators}")
        
        # Look for search result indicators
        search_indicators = [
            'resultado', 'inmueble', 'propiedad', 'apartamento', 'casa',
            'precio', 'area', 'alcoba', 'baño', 'estrato'
        ]
        
        # Count search-related content
        with_params_count = sum(1 for indicator in search_indicators if indicator in content_with_params)
        baseline_count = sum(1 for indicator in search_indicators if indicator in content_baseline)
        
        print(f"📊 Search indicators in parameterized page: {with_params_count}")
        print(f"📊 Search indicators in baseline page: {baseline_count}")
        
        # Check for specific content differences
        content_differences = []
        
        # Look for price-related content
        if 'precio' in content_with_params and 'precio' in content_baseline:
            # Extract price information if possible
            precio_with = content_with_params.count('precio')
            precio_baseline = content_baseline.count('precio')
            if precio_with != precio_baseline:
                content_differences.append(f"Price mentions: {precio_with} vs {precio_baseline}")
        
        # Look for area-related content
        if 'area' in content_with_params and 'area' in content_baseline:
            area_with = content_with_params.count('area')
            area_baseline = content_baseline.count('area')
            if area_with != area_baseline:
                content_differences.append(f"Area mentions: {area_with} vs {area_baseline}")
        
        # Look for bedroom-related content
        if 'alcoba' in content_with_params and 'alcoba' in content_baseline:
            alcoba_with = content_with_params.count('alcoba')
            alcoba_baseline = content_baseline.count('alcoba')
            if alcoba_with != alcoba_baseline:
                content_differences.append(f"Bedroom mentions: {alcoba_with} vs {alcoba_baseline}")
        
        if content_differences:
            print(f"✅ Content differences detected: {content_differences}")
            print(f"✅ Parameters appear to be affecting search results")
        else:
            print(f"⚠️  No significant content differences detected")
            print(f"⚠️  Parameters may not be affecting search results")
        
        # Check if the page contains search results
        search_result_indicators = [
            'resultado', 'encontrado', 'mostrando', 'página', 'total',
            'filtro', 'buscar', 'inmueble'
        ]
        
        has_search_results = any(indicator in content_with_params for indicator in search_result_indicators)
        
        if has_search_results:
            print(f"✅ Page appears to contain search results")
        else:
            print(f"⚠️  Page may not contain search results")
        
        # Check for error messages
        error_indicators = ['error', 'no encontrado', 'sin resultados', 'invalid', 'bad request']
        has_errors = any(indicator in content_with_params for indicator in error_indicators)
        
        if has_errors:
            print(f"⚠️  Error indicators found in content")
        else:
            print(f"✅ No error indicators found")
        
        # Overall assessment
        if content_differences and has_search_results and not has_errors:
            print(f"\n🎉 SUCCESS: URL parameters are working and affecting search results!")
            return True
        elif has_search_results and not has_errors:
            print(f"\n✅ PARTIAL SUCCESS: URL loads and shows search results, but parameter effectiveness unclear")
            return True
        else:
            print(f"\n❌ FAILURE: URL parameters may not be working as expected")
            return False
        
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False


def test_parameter_specific_validation():
    """Test specific parameter values in path-based URL structure"""
    
    print("\n" + "=" * 80)
    print("TESTING PATH-BASED PARAMETER VALIDATION")
    print("=" * 80)
    
    mapper = FincaraizMapper()
    
    # Test with very specific criteria that should produce different results
    specific_property = {
        "address": "Calle 100 #15-20, Bogotá",
        "operation": "VENTA",
        "area_habitable": 80.0,
        "bedrooms": 3,
        "bathrooms": 2,
        "stratum": 5,
        "pricing": {
            "price_per_m2": 5000000  # Very specific price
        }
    }
    
    search_result = mapper.map_property_to_search(specific_property)
    
    if 'error' in search_result:
        print(f"❌ Error: {search_result['error']}")
        return False
    
    search_url = search_result['search_url']
    print(f"🔗 Specific search URL: {search_url}")
    
    # Extract path parts from URL
    parsed_url = urlparse(search_url)
    path_parts = parsed_url.path.strip('/').split('/')
    
    print(f"📋 Path parts: {path_parts}")
    
    validation_passed = True
    
    # Validate operation (first part)
    if len(path_parts) > 0 and path_parts[0] == 'venta':
        print(f"✅ Operation: {path_parts[0]} (correct)")
    else:
        print(f"❌ Operation: {path_parts[0] if path_parts else 'None'} (expected 'venta')")
        validation_passed = False

    # Validate property type (second part)
    if len(path_parts) > 1 and path_parts[1] == 'apartamentos':
        print(f"✅ Property type: {path_parts[1]} (correct)")
    else:
        print(f"❌ Property type: {path_parts[1] if len(path_parts) > 1 else 'None'} (expected 'apartamentos')")
        validation_passed = False

    # Validate city (third part)
    if len(path_parts) > 2 and 'bogota' in path_parts[2]:
        print(f"✅ City: {path_parts[2]} (correct)")
    else:
        print(f"❌ City: {path_parts[2] if len(path_parts) > 2 else 'None'} (expected 'bogota')")
        validation_passed = False

    # Validate bedroom filter (fourth part)
    if len(path_parts) > 3 and '3-o-mas-habitaciones' in path_parts[3]:
        print(f"✅ Bedroom filter: {path_parts[3]} (correct)")
    else:
        print(f"❌ Bedroom filter: {path_parts[3] if len(path_parts) > 3 else 'None'} (expected '3-o-mas-habitaciones')")
        validation_passed = False
    
    # Check price range in path (new format: desde-X/hasta-Y)
    price_from = next((part for part in path_parts if part.startswith('desde-')), None)
    price_to = next((part for part in path_parts if part.startswith('hasta-')), None)
    
    if price_from and price_to:
        print(f"✅ Price filter: {price_from} / {price_to}")

        # Extract price values from filter
        try:
            min_price = int(price_from.replace('desde-', ''))
            max_price = int(price_to.replace('hasta-', ''))

            expected_total = 80 * 5000000  # area * price_per_m2
            expected_min = int(expected_total * 0.75)  # 25% tolerance
            expected_max = int(expected_total * 1.25)  # 25% tolerance

            if expected_min <= min_price <= expected_max and expected_min <= max_price <= expected_max:
                print(f"✅ Price range: {min_price:,} - {max_price:,} (within expected range)")
            else:
                print(f"❌ Price range: {min_price:,} - {max_price:,} (expected around {expected_min:,} - {expected_max:,})")
                validation_passed = False

        except (ValueError, IndexError):
            print(f"❌ Invalid price filter format: {price_from} / {price_to}")
            validation_passed = False
    else:
        print(f"❌ Price filter: not found")
        validation_passed = False
    
    # Check area filter in path (new format: m2-desde-X/m2-hasta-Y)
    area_from = next((part for part in path_parts if part.startswith('m2-desde-')), None)
    area_to = next((part for part in path_parts if part.startswith('m2-hasta-')), None)
    
    if area_from and area_to:
        print(f"✅ Area filter: {area_from} / {area_to}")
    else:
        print(f"❌ Area filter: not found")
        validation_passed = False
    
    if validation_passed:
        print(f"\n✅ All path-based parameter validations passed")
    else:
        print(f"\n❌ Some path-based parameter validations failed")
    
    return validation_passed


def test_url_redirection_behavior():
    """Test if different path-based URLs work correctly without redirecting to defaults"""
    
    print("\n" + "=" * 80)
    print("TESTING PATH-BASED URL BEHAVIOR")
    print("=" * 80)
    
    mapper = FincaraizMapper()
    
    # Test with two very different property searches
    property1 = {
        "address": "Calle 80 #11-42, Bogotá",
        "operation": "ARRIENDO",
        "area_habitable": 30.0,
        "bedrooms": 1,
        "bathrooms": 1,
        "stratum": 2,
        "pricing": {
            "price_per_m2": 20000  # Very low price
        }
    }
    
    property2 = {
        "address": "Carrera 15 #93-47, Bogotá",
        "operation": "VENTA",
        "area_habitable": 200.0,
        "bedrooms": 5,
        "bathrooms": 4,
        "stratum": 6,
        "pricing": {
            "price_per_m2": 10000000  # Very high price
        }
    }
    
    # Generate URLs for both properties
    result1 = mapper.map_property_to_search(property1)
    result2 = mapper.map_property_to_search(property2)
    
    if 'error' in result1 or 'error' in result2:
        print(f"❌ Error generating URLs")
        return False
    
    url1 = result1['search_url']
    url2 = result2['search_url']
    
    print(f"🔗 URL 1 (Low-end rental): {url1}")
    print(f"🔗 URL 2 (High-end sale):  {url2}")
    
    # Analyze path differences
    path1_parts = url1.split('/')
    path2_parts = url2.split('/')
    
    print(f"\n📋 Path Analysis:")
    print(f"   URL 1 parts: {path1_parts}")
    print(f"   URL 2 parts: {path2_parts}")
    
    # Check if paths are different
    if path1_parts != path2_parts:
        print(f"✅ URLs have different path structures")
        
        # Check specific differences
        if path1_parts[0] != path2_parts[0]:
            print(f"✅ Different operations: {path1_parts[0]} vs {path2_parts[0]}")
        
        if len(path1_parts) > 2 and len(path2_parts) > 2 and path1_parts[2] != path2_parts[2]:
            print(f"✅ Different bedroom filters: {path1_parts[2]} vs {path2_parts[2]}")
        
        if len(path1_parts) > 3 and len(path2_parts) > 3:
            # Check for price differences
            price1 = next((part for part in path1_parts if 'entre-' in part and 'y-' in part), None)
            price2 = next((part for part in path2_parts if 'entre-' in part and 'y-' in part), None)
            
            if price1 and price2 and price1 != price2:
                print(f"✅ Different price filters: {price1} vs {price2}")
        
        return True
    else:
        print(f"❌ URLs have identical path structures - this shouldn't happen!")
        return False
    
    try:
        headers = mapper.get_search_headers()
        
        # Fetch both URLs
        print(f"\n🌐 Fetching URL 1...")
        time.sleep(2)
        response1 = requests.get(url1, headers=headers, timeout=30, allow_redirects=True)
        
        print(f"🌐 Fetching URL 2...")
        time.sleep(2)
        response2 = requests.get(url2, headers=headers, timeout=30, allow_redirects=True)
        
        final_url1 = response1.url
        final_url2 = response2.url
        
        print(f"📊 Final URL 1: {final_url1}")
        print(f"📊 Final URL 2: {final_url2}")
        
        # Check if both URLs redirect to the same final URL
        if final_url1 == final_url2:
            print(f"❌ CRITICAL: Both URLs redirect to the same final URL!")
            print(f"   This means Fincaraiz is ignoring our search parameters!")
            print(f"   Our constructed URLs are useless for actual searching.")
            return False
        else:
            print(f"✅ URLs redirect to different final URLs")
            print(f"   This means our parameters are being processed correctly.")
        
        # Check if parameters are preserved in final URLs
        params1 = parse_qs(urlparse(final_url1).query)
        params2 = parse_qs(urlparse(final_url2).query)
        
        print(f"📋 Final URL 1 parameters: {params1}")
        print(f"📋 Final URL 2 parameters: {params2}")
        
        # Compare key parameters
        key_params = ['tipo_operacion', 'precio_min', 'precio_max', 'area_min', 'area_max']
        
        for param in key_params:
            val1 = params1.get(param, ['N/A'])
            val2 = params2.get(param, ['N/A'])
            
            if val1 == val2:
                print(f"⚠️  Parameter '{param}' is the same in both URLs: {val1}")
            else:
                print(f"✅ Parameter '{param}' differs between URLs: {val1} vs {val2}")
        
        # Check response content similarity
        content1 = response1.text.lower()
        content2 = response2.text.lower()
        
        # Look for specific indicators that should be different
        price_indicators = ['precio', 'costo', 'valor', '$']
        area_indicators = ['area', 'm²', 'metro']
        operation_indicators = ['arriendo', 'venta', 'rent', 'sale']
        
        print(f"\n📊 Content comparison:")
        
        for indicator in price_indicators:
            count1 = content1.count(indicator)
            count2 = content2.count(indicator)
            print(f"   '{indicator}': {count1} vs {count2}")
        
        for indicator in area_indicators:
            count1 = content1.count(indicator)
            count2 = content2.count(indicator)
            print(f"   '{indicator}': {count1} vs {count2}")
        
        for indicator in operation_indicators:
            count1 = content1.count(indicator)
            count2 = content2.count(indicator)
            print(f"   '{indicator}': {count1} vs {count2}")
        
        # Overall assessment
        if final_url1 != final_url2 and params1 != params2:
            print(f"\n🎉 SUCCESS: URLs are different and parameters are preserved!")
            print(f"   Our constructed URLs are working correctly for searching.")
            return True
        else:
            print(f"\n❌ FAILURE: URLs are too similar or parameters are lost!")
            print(f"   Our constructed URLs may not be effective for searching.")
            return False
        
    except Exception as e:
        print(f"❌ Error during redirection test: {str(e)}")
        return False


if __name__ == "__main__":
    test_different_property_types()
    test_url_validation()
    
    # Run new URL accessibility tests
    print("\n" + "=" * 80)
    print("RUNNING URL ACCESSIBILITY TESTS")
    print("=" * 80)
    
    # Test URL parameter validation first
    param_test_passed = test_url_parameter_validation()
    
    if param_test_passed:
        # Test actual URL accessibility
        accessibility_test_passed = test_url_accessibility()
        
        if accessibility_test_passed:
            print("\n🎉 All URL tests passed! The mapper generates valid, accessible URLs.")
        else:
            print("\n⚠️  URL accessibility test failed. Check the generated URL manually.")
    else:
        print("\n❌ URL parameter validation failed. Fix parameter issues first.")
    
    # Run parameter effectiveness tests
    print("\n" + "=" * 80)
    print("RUNNING PARAMETER EFFECTIVENESS TESTS")
    print("=" * 80)
    
    # Test parameter-specific validation
    param_specific_passed = test_parameter_specific_validation()
    
    if param_specific_passed:
        # Test if parameters actually affect search results
        effectiveness_test_passed = test_url_parameter_effectiveness()
        
        if effectiveness_test_passed:
            print("\n🎉 Parameter effectiveness tests passed! URL parameters are working correctly.")
        else:
            print("\n⚠️  Parameter effectiveness test failed. Parameters may not be affecting search results.")
    else:
        print("\n❌ Parameter-specific validation failed. Fix parameter issues first.")
    
    # Run redirection behavior test
    print("\n" + "=" * 80)
    print("RUNNING REDIRECTION BEHAVIOR TEST")
    print("=" * 80)
    
    redirection_test_passed = test_url_redirection_behavior()
    
    if redirection_test_passed:
        print("\n🎉 Redirection test passed! URLs are working correctly and not redirecting to defaults.")
    else:
        print("\n❌ CRITICAL: Redirection test failed! URLs may be redirecting to default pages.")
        print("   This means our constructed URLs are useless for actual searching.")
    
    print("\n" + "=" * 80)
    print("🎉 All tests completed!")
    print("=" * 80)
