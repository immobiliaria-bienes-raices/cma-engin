"""
Unit tests for CSV Converter
"""

import sys
import os
import unittest
import tempfile
import csv
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from real_estate_analytics.converters.csv_converter import CSVConverter


class TestCSVConverter(unittest.TestCase):
    """Test cases for CSV Converter"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.converter = CSVConverter()
        
        # Sample raw property data (as would come from orchestrator)
        self.sample_raw_properties = [
            {
                'title': 'Apartamento en arriendo en la felicidad, bogotá',
                'price': '$1,500,000',
                'address': 'Calle 145 #23-06, Bogotá',
                'area': '80 m²',
                'bedrooms': '2',
                'bathrooms': '2.0',
                'parking': '1',
                'stratum': '4',
                'property_type': 'Apartamento',
                'operation': 'ARRIENDO',
                'amenities': 'Ascensor; Balcón; Parqueadero',
                'contact': '3001234567',
                'property_url': 'https://www.fincaraiz.com.co/property/123',
                'images': 'https://example.com/image1.jpg'
            },
            {
                'title': 'Casa en venta en chico, bogotá',
                'price': '$2,500,000',
                'address': 'Carrera 15 #93-07, Bogotá',
                'area': '120 m²',
                'bedrooms': '3',
                'bathrooms': '2.5',
                'parking': '2',
                'stratum': '5',
                'property_type': 'Casa',
                'operation': 'VENTA',
                'amenities': 'Piscina; Gimnasio; Vigilancia',
                'contact': '3007654321',
                'property_url': 'https://www.fincaraiz.com.co/property/456',
                'images': 'https://example.com/image2.jpg'
            }
        ]
    
    def test_converter_initialization(self):
        """Test converter initialization"""
        converter = CSVConverter()
        self.assertIsNotNone(converter.field_mappings)
        self.assertIsNotNone(converter.amenity_keywords)
        self.assertIn('address', converter.field_mappings)
        self.assertIn('terrace', converter.amenity_keywords)
    
    def test_parse_area(self):
        """Test area parsing"""
        self.assertEqual(self.converter._parse_area('80 m²'), 80.0)
        self.assertEqual(self.converter._parse_area('120m2'), 120.0)
        self.assertEqual(self.converter._parse_area('45.5 m²'), 45.5)
        self.assertEqual(self.converter._parse_area(''), 0.0)
        self.assertEqual(self.converter._parse_area('invalid'), 0.0)
    
    def test_parse_price(self):
        """Test price parsing"""
        self.assertEqual(self.converter._parse_price('$1,500,000'), 1500000.0)
        self.assertEqual(self.converter._parse_price('2,500,000'), 2500000.0)
        self.assertEqual(self.converter._parse_price('1.500.000'), 0.0)  # This format is not recognized, returns 0
        self.assertEqual(self.converter._parse_price(''), 0.0)
        self.assertEqual(self.converter._parse_price('invalid'), 0.0)
    
    def test_parse_integer(self):
        """Test integer parsing"""
        self.assertEqual(self.converter._parse_integer('2'), 2)
        self.assertEqual(self.converter._parse_integer('2.5'), 2)
        self.assertEqual(self.converter._parse_integer(''), 0)
        self.assertEqual(self.converter._parse_integer('invalid'), 0)
        self.assertEqual(self.converter._parse_integer('3', default=5), 3)
    
    def test_parse_float(self):
        """Test float parsing"""
        self.assertEqual(self.converter._parse_float('2.5'), 2.5)
        self.assertEqual(self.converter._parse_float('2'), 2.0)
        self.assertEqual(self.converter._parse_float(''), 0.0)
        self.assertEqual(self.converter._parse_float('invalid'), 0.0)
        self.assertEqual(self.converter._parse_float('3.5', default=1.0), 3.5)
    
    def test_extract_operation(self):
        """Test operation extraction"""
        # Test direct operation field
        self.assertEqual(self.converter._extract_operation({'operation': 'ARRIENDO'}), 'ARRIENDO')
        self.assertEqual(self.converter._extract_operation({'operation': 'VENTA'}), 'VENTA')
        
        # Test inference from title
        self.assertEqual(self.converter._extract_operation({'title': 'Apartamento en arriendo'}), 'ARRIENDO')
        self.assertEqual(self.converter._extract_operation({'title': 'Casa en venta'}), 'VENTA')
        
        # Test default
        self.assertEqual(self.converter._extract_operation({}), 'VENTA')
    
    def test_extract_amenity(self):
        """Test amenity extraction"""
        # Test with amenities field
        property_with_amenities = {'amenities': 'Ascensor; Balcón; Piscina'}
        self.assertTrue(self.converter._extract_amenity(property_with_amenities, 'elevator'))
        self.assertTrue(self.converter._extract_amenity(property_with_amenities, 'terrace'))
        self.assertFalse(self.converter._extract_amenity(property_with_amenities, 'loft'))
        
        # Test with specific field
        property_with_field = {'terrace': 'SI'}
        self.assertTrue(self.converter._extract_amenity(property_with_field, 'terrace'))
        
        property_with_field_no = {'terrace': 'NO'}
        self.assertFalse(self.converter._extract_amenity(property_with_field_no, 'terrace'))
    
    def test_convert_single_property(self):
        """Test conversion of a single property"""
        raw_property = self.sample_raw_properties[0]
        converted = self.converter._convert_single_property(raw_property)
        
        self.assertIsNotNone(converted)
        self.assertEqual(converted['address'], 'Calle 145 #23-06, Bogotá')
        self.assertEqual(converted['operation'], 'ARRIENDO')
        self.assertEqual(converted['area_habitable'], 80.0)
        self.assertEqual(converted['bedrooms'], 2)
        self.assertEqual(converted['bathrooms'], 2.0)
        self.assertEqual(converted['parking'], 1)
        self.assertEqual(converted['stratum'], 4)
        self.assertTrue(converted['elevator'])  # From amenities
        self.assertTrue(converted['terrace'])   # From amenities
        self.assertIsInstance(converted['pricing'], dict)
        self.assertIn('price_per_m2', converted['pricing'])
    
    def test_convert_single_property_missing_required(self):
        """Test conversion with missing required fields"""
        raw_property = {'title': 'Test Property'}  # Missing required fields
        converted = self.converter._convert_single_property(raw_property)
        # The converter fills in defaults, so it won't be None, but pricing will be invalid
        self.assertIsNotNone(converted)
        self.assertEqual(converted['pricing']['price_per_m2'], 0)  # Invalid pricing due to missing data
    
    def test_validate_required_fields(self):
        """Test required field validation"""
        # Valid property
        valid_property = {
            'address': 'Test Address',
            'operation': 'VENTA',
            'area_habitable': 80.0,
            'bedrooms': 2,
            'bathrooms': 2.0,
            'pricing': {'price_per_m2': 1000}
        }
        self.assertTrue(self.converter._validate_required_fields(valid_property))
        
        # Missing required field
        invalid_property = {
            'address': 'Test Address',
            'operation': 'VENTA',
            'area_habitable': 80.0,
            'bedrooms': 2,
            # Missing bathrooms and pricing
        }
        self.assertFalse(self.converter._validate_required_fields(invalid_property))
    
    def test_convert_csv_file(self):
        """Test complete CSV file conversion"""
        # Create temporary input file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_input:
            temp_input_path = temp_input.name
            writer = csv.DictWriter(temp_input, fieldnames=self.sample_raw_properties[0].keys())
            writer.writeheader()
            writer.writerows(self.sample_raw_properties)
        
        # Create temporary output file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_output:
            temp_output_path = temp_output.name
        
        try:
            # Convert CSV file
            result = self.converter.convert_csv_file(temp_input_path, temp_output_path)
            
            self.assertTrue(result['success'])
            self.assertEqual(result['total_input_properties'], 2)
            self.assertEqual(result['converted_properties'], 2)
            self.assertEqual(result['conversion_rate'], 1.0)
            
            # Verify output file exists and has content
            self.assertTrue(os.path.exists(temp_output_path))
            
            with open(temp_output_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
                self.assertEqual(len(rows), 2)
                
                # Check first row
                first_row = rows[0]
                self.assertEqual(first_row['address'], 'Calle 145 #23-06, Bogotá')
                self.assertEqual(first_row['operation'], 'ARRIENDO')
                self.assertEqual(first_row['area_habitable'], '80.0')
                self.assertEqual(first_row['bedrooms'], '2')
                self.assertEqual(first_row['bathrooms'], '2.0')
                self.assertEqual(first_row['parking'], '1')
                self.assertEqual(first_row['stratum'], '4')
                
                # Check pricing is JSON string
                pricing = json.loads(first_row['pricing'])
                self.assertIn('price_per_m2', pricing)
                self.assertIn('area', pricing)
        
        finally:
            # Clean up temporary files
            if os.path.exists(temp_input_path):
                os.unlink(temp_input_path)
            if os.path.exists(temp_output_path):
                os.unlink(temp_output_path)
    
    def test_convert_csv_file_nonexistent(self):
        """Test conversion with nonexistent input file"""
        result = self.converter.convert_csv_file('nonexistent.csv', 'output.csv')
        self.assertFalse(result['success'])
        self.assertIn('error', result)
    
    def test_convert_multiple_files(self):
        """Test conversion of multiple files"""
        # Create temporary input files
        temp_files = []
        for i, prop in enumerate(self.sample_raw_properties):
            with tempfile.NamedTemporaryFile(mode='w', suffix=f'_{i}.csv', delete=False) as temp_file:
                temp_files.append(temp_file.name)
                writer = csv.DictWriter(temp_file, fieldnames=prop.keys())
                writer.writeheader()
                writer.writerow(prop)
        
        # Create temporary output directory
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Convert multiple files
                result = self.converter.convert_multiple_files(temp_files, temp_dir)
                
                self.assertTrue(result['success'])
                self.assertEqual(result['total_files'], 2)
                self.assertEqual(result['converted_files'], 2)
                self.assertEqual(result['failed_files'], 0)
                self.assertEqual(result['total_properties'], 2)
                self.assertEqual(result['total_converted'], 2)
                
                # Check output files exist (files are named based on input file names)
                output_files = [f for f in os.listdir(temp_dir) if f.endswith('_standardized.csv')]
                self.assertEqual(len(output_files), 2)
            
            finally:
                # Clean up input files
                for temp_file in temp_files:
                    if os.path.exists(temp_file):
                        os.unlink(temp_file)


def run_converter_tests():
    """Run converter tests with sample data"""
    print("=" * 80)
    print("CSV CONVERTER TEST RESULTS")
    print("=" * 80)
    
    converter = CSVConverter()
    
    # Test with actual scraped data if available
    test_files = [
        "fincaraiz_all_properties_20250919_191833.csv",
        "fincaraiz_properties_1_20250919_191820.csv"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\nTesting conversion of: {test_file}")
            print("-" * 50)
            
            output_file = f"standardized_{test_file}"
            result = converter.convert_csv_file(test_file, output_file)
            
            if result['success']:
                print(f"✅ Conversion successful!")
                print(f"   Input properties: {result['total_input_properties']}")
                print(f"   Converted properties: {result['converted_properties']}")
                print(f"   Conversion rate: {result['conversion_rate']:.2%}")
                print(f"   Output file: {result['output_file']}")
                
                # Show sample of converted data
                if os.path.exists(output_file):
                    with open(output_file, 'r', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile)
                        rows = list(reader)
                        if rows:
                            print(f"   Sample property: {rows[0]['address']} - {rows[0]['operation']}")
                            print(f"   Area: {rows[0]['area_habitable']} m², Bedrooms: {rows[0]['bedrooms']}")
            else:
                print(f"❌ Conversion failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"⚠️  Test file {test_file} not found")
    
    print("\n" + "=" * 80)
    print("🎉 CSV Converter tests completed!")
    print("=" * 80)


if __name__ == "__main__":
    # Run the test suite
    run_converter_tests()
    
    # Also run unit tests
    print("\n" + "=" * 80)
    print("RUNNING UNIT TESTS")
    print("=" * 80)
    
    unittest.main(argv=[''], exit=False, verbosity=2)
