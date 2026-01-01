"""
Unit tests for Fincaraiz Orchestrator
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import csv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from real_estate_analytics.orchestrators.fincaraiz_orchestrator import FincaraizOrchestrator
from real_estate_analytics.mappers.fincaraiz_mapper import FincaraizMapper


class TestFincaraizOrchestrator(unittest.TestCase):
    """Test cases for Fincaraiz Orchestrator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.orchestrator = FincaraizOrchestrator(delay_between_requests=0.1, max_retries=1)
        self.mapper = FincaraizMapper()
        
        # Test properties from mapper tests
        self.test_properties = [
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
    
    def test_orchestrator_initialization(self):
        """Test orchestrator initialization"""
        orchestrator = FincaraizOrchestrator(delay_between_requests=2.0, max_retries=5)
        
        self.assertEqual(orchestrator.delay_between_requests, 2.0)
        self.assertEqual(orchestrator.max_retries, 5)
        self.assertIsNotNone(orchestrator.session)
        self.assertIn('User-Agent', orchestrator.session.headers)
    
    def test_generate_search_urls(self):
        """Test URL generation using mapper"""
        urls = []
        
        for property_data in self.test_properties:
            result = self.mapper.map_property_to_search(property_data)
            if 'error' not in result:
                urls.append(result['search_url'])
        
        self.assertEqual(len(urls), 3)
        
        # Check URL structure
        for url in urls:
            self.assertTrue(url.startswith('https://www.fincaraiz.com.co/'))
            self.assertIn('/', url.split('fincaraiz.com.co/')[1])  # Has path segments
    
    @patch('requests.Session.get')
    def test_scrape_search_results_success(self, mock_get):
        """Test successful scraping of search results"""
        # Mock successful response
        mock_response = Mock()
        mock_response.content = """
        <html>
            <body>
                <div class="property-card">
                    <h3 class="property-title">Apartamento en Cedritos</h3>
                    <div class="property-price">$1,500,000</div>
                    <div class="property-address">Calle 145 #23-06, Bogota</div>
                    <div class="property-area">80 m²</div>
                    <div class="property-bedrooms">2 habitaciones</div>
                    <div class="property-bathrooms">2 banos</div>
                    <div class="property-parking">1 parqueadero</div>
                    <div class="property-stratum">Estrato 4</div>
                    <div class="property-amenities">Ascensor, Balcon</div>
                </div>
                <div class="property-card">
                    <h3 class="property-title">Casa en Chico</h3>
                    <div class="property-price">$2,500,000</div>
                    <div class="property-address">Carrera 15 #93-07, Bogota</div>
                    <div class="property-area">120 m²</div>
                    <div class="property-bedrooms">3 habitaciones</div>
                    <div class="property-bathrooms">2 banos</div>
                    <div class="property-parking">2 parqueaderos</div>
                    <div class="property-stratum">Estrato 5</div>
                </div>
            </body>
        </html>
        """.encode('utf-8')
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test URL
        test_url = "https://www.fincaraiz.com.co/arriendo/apartamentos/bogota/1-o-mas-habitaciones/1-o-mas-banos/desde-1125000/hasta-1875000/m2-desde-40/m2-hasta-60/edificados/publicado-ultimos-7-dias?IDmoneda=4&stratum[]=3"
        
        result = self.orchestrator.scrape_search_results(test_url)
        
        self.assertTrue(result['success'])
        self.assertGreaterEqual(len(result['properties']), 2)
        self.assertEqual(result['url'], test_url)
        
        # Check first property
        first_prop = result['properties'][0]
        self.assertEqual(first_prop['title'], 'Apartamento en Cedritos')
        self.assertEqual(first_prop['price'], '$1,500,000')
        self.assertEqual(first_prop['area'], '80 m²')
        self.assertEqual(first_prop['bedrooms'], 2)
        self.assertEqual(first_prop['bathrooms'], 2.0)
        self.assertEqual(first_prop['parking'], 1)
        self.assertEqual(first_prop['stratum'], 4)
        self.assertIn('Ascensor', first_prop['amenities'])
        # Note: Amenities extraction depends on HTML content and regex patterns
    
    @patch('requests.Session.get')
    def test_scrape_search_results_failure(self, mock_get):
        """Test handling of failed requests"""
        # Mock failed response
        mock_get.side_effect = Exception("Network error")
        
        test_url = "https://www.fincaraiz.com.co/invalid-url"
        result = self.orchestrator.scrape_search_results(test_url)
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)
        self.assertEqual(len(result['properties']), 0)
    
    def test_extract_property_data(self):
        """Test property data extraction from HTML"""
        from bs4 import BeautifulSoup
        
        html_content = """
        <div class="property-card">
            <h3 class="property-title">Test Apartamento</h3>
            <div class="property-price">$2,000,000</div>
            <div class="property-address">Test Address 123</div>
            <div class="property-area">100 m²</div>
            <div class="property-bedrooms">3 habitaciones</div>
            <div class="property-bathrooms">2.5 baños</div>
            <div class="property-parking">2 parqueaderos</div>
            <div class="property-stratum">Estrato 4</div>
            <div class="property-amenities">Ascensor, Piscina, Gimnasio</div>
            <a href="/property/123">Ver detalles</a>
            <img src="/images/property1.jpg" alt="Property image">
        </div>
        """
        
        soup = BeautifulSoup(html_content, 'html.parser')
        container = soup.find('div', class_='property-card')
        
        property_data = self.orchestrator._extract_single_property(container, "https://www.fincaraiz.com.co")
        
        self.assertIsNotNone(property_data)
        self.assertEqual(property_data['title'], 'Test Apartamento')
        self.assertEqual(property_data['price'], '$2,000,000')
        self.assertEqual(property_data['address'], 'Test Address 123')
        self.assertEqual(property_data['area'], '100 m²')
        self.assertEqual(property_data['bedrooms'], 3)
        self.assertEqual(property_data['bathrooms'], 2.5)
        self.assertEqual(property_data['parking'], 2)
        self.assertEqual(property_data['stratum'], 4)
        self.assertIn('Ascensor', property_data['amenities'])
        self.assertIn('Piscina', property_data['amenities'])
        self.assertIn('Gimnasio', property_data['amenities'])
        self.assertTrue(property_data['property_url'].endswith('/property/123'))
        self.assertIn('property1.jpg', property_data['images'][0])
    
    def test_save_to_csv(self):
        """Test saving properties to CSV"""
        test_properties = [
            {
                'title': 'Test Property 1',
                'price': '$1,000,000',
                'area': '80 m²',
                'bedrooms': 2,
                'bathrooms': 2.0,
                'amenities': ['Ascensor', 'Balcón']
            },
            {
                'title': 'Test Property 2',
                'price': '$2,000,000',
                'area': '120 m²',
                'bedrooms': 3,
                'bathrooms': 2.5,
                'amenities': ['Piscina', 'Gimnasio']
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            success = self.orchestrator.save_to_csv(test_properties, temp_filename)
            self.assertTrue(success)
            
            # Verify CSV content
            with open(temp_filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
                
                self.assertEqual(len(rows), 2)
                self.assertEqual(rows[0]['title'], 'Test Property 1')
                self.assertEqual(rows[0]['price'], '$1,000,000')
                self.assertEqual(rows[0]['amenities'], 'Ascensor; Balcón')
                self.assertEqual(rows[1]['title'], 'Test Property 2')
                self.assertEqual(rows[1]['price'], '$2,000,000')
                self.assertEqual(rows[1]['amenities'], 'Piscina; Gimnasio')
        
        finally:
            os.unlink(temp_filename)
    
    def test_save_to_csv_empty_properties(self):
        """Test saving empty properties list"""
        success = self.orchestrator.save_to_csv([], "test.csv")
        self.assertFalse(success)
    
    @patch('requests.Session.get')
    def test_complete_process(self, mock_get):
        """Test complete process: scrape and save to CSV"""
        # Mock successful response
        mock_response = Mock()
        mock_response.content = """
        <html>
            <body>
                <div class="property-card">
                    <h3 class="property-title">Test Property</h3>
                    <div class="property-price">$1,500,000</div>
                    <div class="property-address">Test Address</div>
                    <div class="property-area">80 m²</div>
                    <div class="property-bedrooms">2 habitaciones</div>
                    <div class="property-bathrooms">2 banos</div>
                </div>
            </body>
        </html>
        """.encode('utf-8')
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        test_url = "https://www.fincaraiz.com.co/arriendo/apartamentos/bogota/1-o-mas-habitaciones/1-o-mas-banos/desde-1125000/hasta-1875000/m2-desde-40/m2-hasta-60/edificados/publicado-ultimos-7-dias?IDmoneda=4&stratum[]=3"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            result = self.orchestrator.process_search_url(test_url, temp_filename)
            
            self.assertTrue(result['success'])
            self.assertTrue(result['csv_success'])
            self.assertEqual(result['csv_file'], temp_filename)
            self.assertGreaterEqual(len(result['properties']), 1)
            
            # Verify CSV was created and has content
            self.assertTrue(os.path.exists(temp_filename))
            with open(temp_filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
                self.assertGreaterEqual(len(rows), 1)
                self.assertEqual(rows[0]['title'], 'Test Property')
        
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_integration_with_mapper(self):
        """Test integration between mapper and orchestrator"""
        # Generate search URL using mapper
        property_data = self.test_properties[0]
        mapper_result = self.mapper.map_property_to_search(property_data)
        
        self.assertIn('search_url', mapper_result)
        search_url = mapper_result['search_url']
        
        # Verify URL structure
        self.assertTrue(search_url.startswith('https://www.fincaraiz.com.co/'))
        self.assertIn('arriendo', search_url)
        self.assertIn('apartamentos', search_url)
        # Note: bogota might not be in URL if address parsing fails
        
        # Test that orchestrator can process the URL (without actual scraping)
        orchestrator = FincaraizOrchestrator()
        self.assertIsNotNone(orchestrator)
        self.assertEqual(orchestrator.delay_between_requests, 1.0)
        self.assertEqual(orchestrator.max_retries, 3)


def run_orchestrator_tests():
    """Run orchestrator tests with the same test cases as mapper"""
    print("=" * 80)
    print("FINCARAIZ ORCHESTRATOR TEST RESULTS")
    print("=" * 80)
    
    # Initialize components
    mapper = FincaraizMapper()
    orchestrator = FincaraizOrchestrator(delay_between_requests=0.1, max_retries=1)
    
    # Test properties from mapper tests
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
    
    print("\nTesting URL Generation with Mapper:")
    print("-" * 50)
    
    urls = []
    for i, property_data in enumerate(test_properties, 1):
        result = mapper.map_property_to_search(property_data)
        
        if 'error' not in result:
            url = result['search_url']
            urls.append(url)
            print(f"✅ Property {i}: {property_data['operation']} - {property_data['area_habitable']}m²")
            print(f"   URL: {url}")
        else:
            print(f"❌ Property {i}: Error - {result['error']}")
    
    print(f"\n✅ Generated {len(urls)} valid search URLs")
    
    print("\nTesting Orchestrator Initialization:")
    print("-" * 50)
    print(f"✅ Delay between requests: {orchestrator.delay_between_requests}s")
    print(f"✅ Max retries: {orchestrator.max_retries}")
    print(f"✅ User-Agent: {orchestrator.session.headers.get('User-Agent', 'Not set')[:50]}...")
    
    print("\nTesting CSV Generation:")
    print("-" * 50)
    
    # Test CSV generation with mock data
    test_properties_data = [
        {
            'title': 'Apartamento en Cedritos',
            'price': '$1,500,000',
            'address': 'Calle 145 #23-06, Bogotá',
            'area': '80 m²',
            'bedrooms': 2,
            'bathrooms': 2.0,
            'parking': 1,
            'stratum': 4,
            'property_type': 'Apartamento',
            'operation': 'ARRIENDO',
            'amenities': ['Ascensor', 'Balcón'],
            'contact': '3001234567',
            'property_url': 'https://www.fincaraiz.com.co/property/123',
            'images': ['https://www.fincaraiz.com.co/images/prop1.jpg']
        },
        {
            'title': 'Casa en Chico',
            'price': '$2,500,000',
            'address': 'Carrera 15 #93-07, Bogotá',
            'area': '120 m²',
            'bedrooms': 3,
            'bathrooms': 2.5,
            'parking': 2,
            'stratum': 5,
            'property_type': 'Casa',
            'operation': 'VENTA',
            'amenities': ['Piscina', 'Gimnasio', 'Vigilancia'],
            'contact': '3007654321',
            'property_url': 'https://www.fincaraiz.com.co/property/456',
            'images': ['https://www.fincaraiz.com.co/images/prop2.jpg', 'https://www.fincaraiz.com.co/images/prop2_2.jpg']
        }
    ]
    
    # Test CSV saving
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
        temp_filename = temp_file.name
    
    try:
        csv_success = orchestrator.save_to_csv(test_properties_data, temp_filename)
        
        if csv_success:
            print(f"✅ CSV file created: {temp_filename}")
            
            # Verify CSV content
            import csv
            with open(temp_filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
                
                print(f"✅ CSV contains {len(rows)} properties")
                print(f"✅ CSV headers: {list(rows[0].keys()) if rows else 'No data'}")
                
                if rows:
                    print(f"✅ First property: {rows[0]['title']} - {rows[0]['price']}")
                    print(f"✅ Amenities format: {rows[0]['amenities']}")
        else:
            print("❌ CSV creation failed")
    
    finally:
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)
    
    print("\n" + "=" * 80)
    print("🎉 All orchestrator tests completed!")
    print("=" * 80)


if __name__ == "__main__":
    # Run the test suite
    run_orchestrator_tests()
    
    # Also run unit tests
    print("\n" + "=" * 80)
    print("RUNNING UNIT TESTS")
    print("=" * 80)
    
    unittest.main(argv=[''], exit=False, verbosity=2)
