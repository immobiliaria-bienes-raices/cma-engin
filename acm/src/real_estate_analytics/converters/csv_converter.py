"""
CSV Converter for Real Estate Data

This converter transforms raw scraped CSV data from orchestrators
into the standardized property schema format used for analysis.
"""

import csv
import re
import json
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CSVConverter:
    """Converts raw scraped CSV data to standardized property schema format"""
    
    def __init__(self):
        """Initialize the CSV converter with field mappings"""
        self.field_mappings = {
            # Basic information
            'title': 'address',  # Use title as address if no specific address
            'address': 'address',
            'operation': 'operation',
            'property_type': 'property_type',
            
            # Areas
            'area': 'area_habitable',
            'area_habitable': 'area_habitable',
            'area_total': 'area_total',
            'terrace_area': 'terrace_area',
            
            # Rooms and spaces
            'bedrooms': 'bedrooms',
            'bathrooms': 'bathrooms',
            'parking': 'parking',
            'deposit': 'deposit',
            'floor': 'floor',
            
            # Amenities (boolean fields)
            'terrace': 'terrace',
            'walking_closet': 'walking_closet',
            'loft': 'loft',
            'study_room': 'study_room',
            'elevator': 'elevator',
            
            # Quality ratings
            'stratum': 'stratum',
            'finish_quality': 'finish_quality',
            'conservation_state': 'conservation_state',
            'location_quality': 'location_quality',
            
            # Additional info
            'construction_age': 'construction_age',
            'interior_exterior': 'interior_exterior',
            'observations': 'observations',
            'contact': 'contact_info',
            'contact_method': 'contact_method',
            
            # Pricing
            'price': 'total_price',
            'administration': 'administration'
        }
        
        # Amenity keywords mapping
        self.amenity_keywords = {
            'terrace': ['terraza', 'balcon', 'balcón'],
            'walking_closet': ['walking closet', 'closet'],
            'loft': ['loft'],
            'study_room': ['estudio', 'sala tv', 'sala de tv'],
            'elevator': ['ascensor', 'elevador'],
            'parking': ['parqueadero', 'garaje'],
            'deposit': ['deposito', 'depósito', 'bodega'],
            'pool': ['piscina'],
            'gym': ['gimnasio'],
            'security': ['vigilancia', 'seguridad'],
            'bbq': ['bbq', 'asado', 'parrilla']
        }
    
    def convert_csv_file(self, input_file: str, output_file: str) -> Dict[str, Any]:
        """
        Convert a raw CSV file to standardized format
        
        Args:
            input_file: Path to input CSV file
            output_file: Path to output CSV file
            
        Returns:
            Dictionary with conversion results
        """
        try:
            logger.info(f"Converting CSV file: {input_file}")
            
            # Read raw CSV data
            raw_properties = self._read_csv_file(input_file)
            logger.info(f"Read {len(raw_properties)} properties from {input_file}")
            
            # Convert to standardized format
            converted_properties = []
            conversion_errors = []
            
            for i, raw_property in enumerate(raw_properties):
                try:
                    converted = self._convert_single_property(raw_property)
                    if converted:
                        converted_properties.append(converted)
                except Exception as e:
                    error_msg = f"Error converting property {i+1}: {str(e)}"
                    logger.warning(error_msg)
                    conversion_errors.append(error_msg)
            
            # Write converted data to output file
            success = self._write_standardized_csv(converted_properties, output_file)
            
            result = {
                'success': success,
                'input_file': input_file,
                'output_file': output_file,
                'total_input_properties': len(raw_properties),
                'converted_properties': len(converted_properties),
                'conversion_errors': conversion_errors,
                'conversion_rate': len(converted_properties) / len(raw_properties) if raw_properties else 0
            }
            
            logger.info(f"Conversion completed: {len(converted_properties)}/{len(raw_properties)} properties converted")
            return result
            
        except Exception as e:
            logger.error(f"Error converting CSV file: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'input_file': input_file,
                'output_file': output_file
            }
    
    def _read_csv_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Read CSV file and return list of property dictionaries"""
        properties = []
        
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Clean up the row data
                cleaned_row = {k: v.strip() if isinstance(v, str) else v for k, v in row.items()}
                properties.append(cleaned_row)
        
        return properties
    
    def _convert_single_property(self, raw_property: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Convert a single raw property to standardized format"""
        try:
            converted = {}
            
            # Basic information
            converted['address'] = self._extract_address(raw_property)
            converted['operation'] = self._extract_operation(raw_property)
            
            # Areas
            converted['area_habitable'] = self._extract_area_habitable(raw_property)
            converted['area_total'] = self._extract_area_total(raw_property)
            converted['terrace_area'] = self._extract_terrace_area(raw_property)
            
            # Rooms and spaces
            converted['bedrooms'] = self._extract_bedrooms(raw_property)
            converted['bathrooms'] = self._extract_bathrooms(raw_property)
            converted['parking'] = self._extract_parking(raw_property)
            converted['deposit'] = self._extract_deposit(raw_property)
            converted['floor'] = self._extract_floor(raw_property)
            
            # Amenities (boolean fields)
            converted['terrace'] = self._extract_terrace(raw_property)
            converted['walking_closet'] = self._extract_walking_closet(raw_property)
            converted['loft'] = self._extract_loft(raw_property)
            converted['study_room'] = self._extract_study_room(raw_property)
            converted['elevator'] = self._extract_elevator(raw_property)
            
            # Quality ratings
            converted['stratum'] = self._extract_stratum(raw_property)
            converted['finish_quality'] = self._extract_finish_quality(raw_property)
            converted['conservation_state'] = self._extract_conservation_state(raw_property)
            converted['location_quality'] = self._extract_location_quality(raw_property)
            
            # Additional info
            converted['construction_age'] = self._extract_construction_age(raw_property)
            converted['interior_exterior'] = self._extract_interior_exterior(raw_property)
            converted['observations'] = self._extract_observations(raw_property)
            converted['contact_info'] = self._extract_contact_info(raw_property)
            converted['contact_method'] = self._extract_contact_method(raw_property)
            
            # Administration
            converted['administration'] = self._extract_administration(raw_property)
            
            # Pricing information
            pricing_data = self._extract_pricing(raw_property)
            converted['pricing'] = pricing_data
            
            # Extract individual pricing fields for easier access
            converted['price_per_m2'] = pricing_data.get('price_per_m2', 0)
            converted['total_price_per_m2'] = pricing_data.get('total_price_per_m2', 0)
            converted['admin_per_m2'] = pricing_data.get('admin_per_m2', 0)
            
            # Validate required fields
            if not self._validate_required_fields(converted):
                logger.warning(f"Property missing required fields: {converted.get('address', 'Unknown')}")
                return None
            
            return converted
            
        except Exception as e:
            logger.warning(f"Error converting property: {str(e)}")
            return None
    
    def _extract_address(self, raw_property: Dict[str, Any]) -> str:
        """Extract and clean address"""
        address = raw_property.get('address', '') or raw_property.get('title', '')
        return address.strip() if address else 'Dirección no disponible'
    
    def _extract_operation(self, raw_property: Dict[str, Any]) -> str:
        """Extract operation type (ARRIENDO/VENTA)"""
        operation = raw_property.get('operation', '').upper()
        if 'ARRIENDO' in operation or 'RENTA' in operation:
            return 'ARRIENDO'
        elif 'VENTA' in operation or 'SALE' in operation:
            return 'VENTA'
        else:
            # Try to infer from title
            title = raw_property.get('title', '').upper()
            if 'ARRIENDO' in title or 'RENTA' in title:
                return 'ARRIENDO'
            elif 'VENTA' in title or 'SALE' in title:
                return 'VENTA'
            return 'VENTA'  # Default to VENTA
    
    def _extract_area_habitable(self, raw_property: Dict[str, Any]) -> float:
        """Extract habitable area in m²"""
        area = raw_property.get('area', '') or raw_property.get('area_habitable', '')
        return self._parse_area(area)
    
    def _extract_area_total(self, raw_property: Dict[str, Any]) -> float:
        """Extract total area in m²"""
        area = raw_property.get('area_total', '')
        return self._parse_area(area)
    
    def _extract_terrace_area(self, raw_property: Dict[str, Any]) -> float:
        """Extract terrace area in m²"""
        area = raw_property.get('terrace_area', '')
        return self._parse_area(area)
    
    def _parse_area(self, area_str: str) -> float:
        """Parse area string to float"""
        if not area_str:
            return 0.0
        
        # Extract number from string like "80 m²" or "80m2"
        match = re.search(r'(\d+(?:\.\d+)?)', str(area_str))
        if match:
            return float(match.group(1))
        return 0.0
    
    def _extract_bedrooms(self, raw_property: Dict[str, Any]) -> int:
        """Extract number of bedrooms"""
        bedrooms = raw_property.get('bedrooms', '')
        return self._parse_integer(bedrooms)
    
    def _extract_bathrooms(self, raw_property: Dict[str, Any]) -> float:
        """Extract number of bathrooms"""
        bathrooms = raw_property.get('bathrooms', '')
        return self._parse_float(bathrooms)
    
    def _extract_parking(self, raw_property: Dict[str, Any]) -> int:
        """Extract number of parking spaces"""
        parking = raw_property.get('parking', '')
        return self._parse_integer(parking)
    
    def _extract_deposit(self, raw_property: Dict[str, Any]) -> int:
        """Extract number of storage rooms"""
        deposit = raw_property.get('deposit', '')
        return self._parse_integer(deposit)
    
    def _extract_floor(self, raw_property: Dict[str, Any]) -> int:
        """Extract floor number"""
        floor = raw_property.get('floor', '')
        return self._parse_integer(floor)
    
    def _extract_terrace(self, raw_property: Dict[str, Any]) -> bool:
        """Extract terrace information"""
        return self._extract_amenity(raw_property, 'terrace')
    
    def _extract_walking_closet(self, raw_property: Dict[str, Any]) -> bool:
        """Extract walking closet information"""
        return self._extract_amenity(raw_property, 'walking_closet')
    
    def _extract_loft(self, raw_property: Dict[str, Any]) -> bool:
        """Extract loft information"""
        return self._extract_amenity(raw_property, 'loft')
    
    def _extract_study_room(self, raw_property: Dict[str, Any]) -> bool:
        """Extract study room information"""
        return self._extract_amenity(raw_property, 'study_room')
    
    def _extract_elevator(self, raw_property: Dict[str, Any]) -> bool:
        """Extract elevator information"""
        return self._extract_amenity(raw_property, 'elevator')
    
    def _extract_amenity(self, raw_property: Dict[str, Any], amenity_type: str) -> bool:
        """Extract boolean amenity information"""
        # Check amenities field
        amenities = raw_property.get('amenities', '')
        if amenities:
            amenity_text = str(amenities).lower()
            keywords = self.amenity_keywords.get(amenity_type, [])
            for keyword in keywords:
                if keyword.lower() in amenity_text:
                    return True
        
        # Check specific field
        field_value = raw_property.get(amenity_type, '')
        if field_value:
            return str(field_value).upper() in ['SI', 'YES', 'TRUE', '1']
        
        return False
    
    def _extract_stratum(self, raw_property: Dict[str, Any]) -> int:
        """Extract socioeconomic stratum"""
        stratum = raw_property.get('stratum', '')
        return self._parse_integer(stratum)
    
    def _extract_finish_quality(self, raw_property: Dict[str, Any]) -> int:
        """Extract finish quality rating (1-5)"""
        quality = raw_property.get('finish_quality', '')
        return self._parse_integer(quality, default=3)
    
    def _extract_conservation_state(self, raw_property: Dict[str, Any]) -> int:
        """Extract conservation state rating (1-5)"""
        state = raw_property.get('conservation_state', '')
        return self._parse_integer(state, default=3)
    
    def _extract_location_quality(self, raw_property: Dict[str, Any]) -> int:
        """Extract location quality rating (1-5)"""
        quality = raw_property.get('location_quality', '')
        return self._parse_integer(quality, default=3)
    
    def _extract_construction_age(self, raw_property: Dict[str, Any]) -> int:
        """Extract construction age in years"""
        age = raw_property.get('construction_age', '')
        return self._parse_integer(age)
    
    def _extract_interior_exterior(self, raw_property: Dict[str, Any]) -> str:
        """Extract interior/exterior designation"""
        ie = raw_property.get('interior_exterior', '')
        if str(ie).upper() in ['I', 'INTERIOR']:
            return 'I'
        elif str(ie).upper() in ['E', 'EXTERIOR']:
            return 'E'
        return 'I'  # Default to Interior
    
    def _extract_observations(self, raw_property: Dict[str, Any]) -> str:
        """Extract observations"""
        return raw_property.get('observations', '')
    
    def _extract_contact_info(self, raw_property: Dict[str, Any]) -> str:
        """Extract contact information"""
        return raw_property.get('contact', '') or raw_property.get('contact_info', '')
    
    def _extract_contact_method(self, raw_property: Dict[str, Any]) -> str:
        """Extract contact method"""
        return raw_property.get('contact_method', '')
    
    def _extract_administration(self, raw_property: Dict[str, Any]) -> float:
        """Extract administration fee"""
        admin = raw_property.get('administration', '')
        return self._parse_float(admin)
    
    def _extract_pricing(self, raw_property: Dict[str, Any]) -> Dict[str, float]:
        """Extract pricing information"""
        # Extract price
        price_str = raw_property.get('price', '')
        total_price = self._parse_price(price_str)
        
        # Extract areas
        area_habitable = self._extract_area_habitable(raw_property)
        area_total = self._extract_area_total(raw_property) or area_habitable
        
        # Use price_per_m2 from orchestrator if available, otherwise calculate
        orchestrator_price_per_m2 = raw_property.get('price_per_m2', 0)
        try:
            orchestrator_price_per_m2 = float(orchestrator_price_per_m2)
            if orchestrator_price_per_m2 > 0:
                price_per_m2 = orchestrator_price_per_m2
            else:
                # Fallback to calculation
                price_per_m2 = total_price / area_habitable if area_habitable > 0 else 0
        except (ValueError, TypeError):
            # Fallback to calculation if conversion fails
            price_per_m2 = total_price / area_habitable if area_habitable > 0 else 0
        
        # Extract administration
        administration = self._extract_administration(raw_property)
        admin_per_m2 = administration / area_habitable if area_habitable > 0 else 0
        
        return {
            'area': area_habitable,
            'price_per_m2': price_per_m2,
            'total_area': area_total,
            'total_price_per_m2': price_per_m2,
            'admin_per_m2': admin_per_m2
        }
    
    def _parse_price(self, price_str: str) -> float:
        """Parse price string to float"""
        if not price_str:
            return 0.0
        
        # Remove common currency symbols and formatting
        price_clean = re.sub(r'[^\d.,]', '', str(price_str))
        
        # Handle different decimal separators
        if ',' in price_clean and '.' in price_clean:
            # Assume comma is thousands separator
            price_clean = price_clean.replace(',', '')
        elif ',' in price_clean:
            # Could be decimal separator
            if len(price_clean.split(',')[-1]) <= 2:
                price_clean = price_clean.replace(',', '.')
            else:
                price_clean = price_clean.replace(',', '')
        
        try:
            return float(price_clean)
        except ValueError:
            return 0.0
    
    def _parse_integer(self, value: str, default: int = 0) -> int:
        """Parse string to integer with default"""
        if not value:
            return default
        
        try:
            return int(float(str(value)))
        except (ValueError, TypeError):
            return default
    
    def _parse_float(self, value: str, default: float = 0.0) -> float:
        """Parse string to float with default"""
        if not value:
            return default
        
        try:
            return float(str(value))
        except (ValueError, TypeError):
            return default
    
    def _validate_required_fields(self, property_data: Dict[str, Any]) -> bool:
        """Validate that required fields are present"""
        required_fields = ['address', 'operation', 'area_habitable', 'bedrooms', 'bathrooms', 'pricing']
        
        for field in required_fields:
            if field not in property_data or property_data[field] is None:
                return False
        
        return True
    
    def _write_standardized_csv(self, properties: List[Dict[str, Any]], output_file: str) -> bool:
        """Write standardized properties to CSV file"""
        try:
            if not properties:
                logger.warning("No properties to write")
                return False
            
            # Define CSV headers based on property schema
            headers = [
                'address', 'operation', 'area_habitable', 'terrace', 'area_total',
                'administration', 'bedrooms', 'bathrooms', 'parking', 'walking_closet',
                'loft', 'study_room', 'floor', 'deposit', 'terrace_area',
                'construction_age', 'interior_exterior', 'elevator', 'finish_quality',
                'conservation_state', 'location_quality', 'stratum', 'observations',
                'contact_method', 'contact_info', 'pricing', 'price_per_m2', 
                'total_price_per_m2', 'admin_per_m2'
            ]
            
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                
                for prop in properties:
                    # Convert pricing dict to string for CSV
                    row = prop.copy()
                    if 'pricing' in row and isinstance(row['pricing'], dict):
                        row['pricing'] = json.dumps(row['pricing'])
                    
                    writer.writerow(row)
            
            logger.info(f"Successfully wrote {len(properties)} properties to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error writing CSV file: {str(e)}")
            return False
    
    def convert_multiple_files(self, input_files: List[str], output_dir: str) -> Dict[str, Any]:
        """
        Convert multiple CSV files to standardized format
        
        Args:
            input_files: List of input CSV file paths
            output_dir: Directory to save output files
            
        Returns:
            Dictionary with conversion results
        """
        results = {
            'success': True,
            'total_files': len(input_files),
            'converted_files': 0,
            'failed_files': 0,
            'file_results': [],
            'total_properties': 0,
            'total_converted': 0
        }
        
        for input_file in input_files:
            # Generate output filename
            import os
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_file = os.path.join(output_dir, f"{base_name}_standardized.csv")
            
            # Convert file
            file_result = self.convert_csv_file(input_file, output_file)
            results['file_results'].append(file_result)
            
            if file_result['success']:
                results['converted_files'] += 1
                results['total_properties'] += file_result['total_input_properties']
                results['total_converted'] += file_result['converted_properties']
            else:
                results['failed_files'] += 1
                results['success'] = False
        
        return results


if __name__ == "__main__":
    # Test the converter
    converter = CSVConverter()
    
    # Test with a sample file
    test_file = "fincaraiz_all_properties_20250919_191833.csv"
    output_file = "standardized_properties.csv"
    
    if os.path.exists(test_file):
        print("Testing CSV Converter...")
        result = converter.convert_csv_file(test_file, output_file)
        print(f"Conversion result: {result}")
    else:
        print(f"Test file {test_file} not found")
