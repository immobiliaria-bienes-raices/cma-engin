"""
Property Type Specific CSV Generator

This module generates CSV files with specific column structures based on property type:
- Apartments and Houses: Standard columns from ejemplo_venta.csv
- Lotes (Lots): Specialized columns for land properties
"""

import csv
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class PropertyTypeCSVGenerator:
    """Generate CSV files with property-type-specific column structures"""
    
    def __init__(self):
        self.apartment_house_columns = [
            'Dirección, links', 'VENTA', 'Area Habitable', 'Terraza', 'Area Total',
            'administracion', 'Alcobas', 'Baños', 'Parqueadero', 'Walking closet',
            'LOFT', 'Estudio/Sala TV', 'Piso', 'Alcob. Servic', 'Depósito',
            'Terraza/Balcón (Área)', 'Edad construcción', 'Interior/Exterior',
            'Ascensor', 'Calidad Acabados', 'Estado, Conservación *', 'Ubicación',
            'Estrato', 'observaciones', 'Medio de Contacto', 'Contacto **'
        ]
        
        self.lote_columns = [
            'Dirección, links', 'VENTA', 'Area Util m2', 'Precio Incluido',
            'Administración', 'Area deposito', 'Area Total', 'Mezanine',
            'Baños', 'Cocina', 'Bodega', 'Piso', 'Parqueadero', 'Año construcción',
            'Estrato', 'Código inmueble', 'observaciones', 'Medio de Contacto', 'Contacto **'
        ]
    
    def generate_csv(self, properties: List[Dict[str, Any]], output_file: str, 
                    property_type: str = 'apartment') -> Dict[str, Any]:
        """
        Generate CSV file with property-type-specific columns
        
        Args:
            properties: List of property dictionaries
            output_file: Output CSV file path
            property_type: Type of property ('apartment', 'house', 'lote')
        
        Returns:
            Dictionary with success status and metadata
        """
        try:
            if not properties:
                logger.warning("No properties to process")
                return {'success': False, 'error': 'No properties provided'}
            
            # Determine column structure based on property type
            if property_type.lower() in ['lote', 'lotes', 'terreno', 'terrenos']:
                columns = self.lote_columns
                processed_properties = self._process_lote_properties(properties)
            else:
                columns = self.apartment_house_columns
                processed_properties = self._process_apartment_house_properties(properties)
            
            # Write CSV file
            success = self._write_csv(processed_properties, columns, output_file)
            
            if success:
                logger.info(f"Successfully generated {property_type} CSV with {len(processed_properties)} properties")
                return {
                    'success': True,
                    'output_file': output_file,
                    'property_type': property_type,
                    'properties_count': len(processed_properties),
                    'columns': columns
                }
            else:
                return {'success': False, 'error': 'Failed to write CSV file'}
                
        except Exception as e:
            logger.error(f"Error generating CSV: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _process_apartment_house_properties(self, properties: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process properties for apartment/house CSV format"""
        processed = []
        
        for prop in properties:
            try:
                # Extract basic information
                address = prop.get('address', '')
                property_url = prop.get('property_url', '')
                direccion_links = f"{address}, {property_url}" if property_url else address
                
                # Extract pricing information
                price = self._extract_price_value(prop.get('price', ''))
                area_habitable = self._extract_area_value(prop.get('area', ''))
                price_per_m2 = prop.get('price_per_m2', 0)
                
                # Extract areas
                area_total = area_habitable  # Use habitable area as total if no separate total
                terraza_area = 0  # Default, would need specific extraction
                
                # Extract administration
                administration = self._extract_administration(prop)
                admin_per_m2 = administration / area_habitable if area_habitable > 0 else 0
                
                # Extract room counts
                bedrooms = prop.get('bedrooms', 0) or 0
                bathrooms = prop.get('bathrooms', 0) or 0
                parking = prop.get('parking', 0) or 0
                
                # Extract amenities (convert to YES/NO)
                amenities = prop.get('amenities', [])
                walking_closet = 'SI' if 'walking_closet' in amenities else 'NO'
                loft = 'SI' if 'loft' in amenities else 'NO'
                estudio = 'SI' if 'study_room' in amenities else 'NO'
                elevator = 'SI' if 'elevator' in amenities else 'NO'
                
                # Extract other details
                floor = self._extract_floor(prop)
                deposit = 'NO'  # Default, would need specific extraction
                terrace_balcon = 'NO'  # Default, would need specific extraction
                construction_age = self._extract_construction_age(prop)
                interior_exterior = self._extract_interior_exterior(prop)
                
                # Quality ratings (default values)
                finish_quality = 4  # Default
                conservation_state = 4  # Default
                location_quality = 5  # Default
                
                # Extract stratum
                stratum = prop.get('stratum', 0) or 0
                
                # Extract contact information
                contact = prop.get('contact', '')
                contact_method = 'F.R.'  # Default
                
                processed_prop = {
                    'Dirección, links': direccion_links,
                    'VENTA': price,
                    'Area Habitable': area_habitable,
                    'Terraza': terraza_area,
                    'Area Total': area_total,
                    'administracion': administration,
                    'Alcobas': bedrooms,
                    'Baños': bathrooms,
                    'Parqueadero': parking,
                    'Walking closet': walking_closet,
                    'LOFT': loft,
                    'Estudio/Sala TV': estudio,
                    'Piso': floor,
                    'Alcob. Servic': 1,  # Default
                    'Depósito': deposit,
                    'Terraza/Balcón (Área)': terrace_balcon,
                    'Edad construcción': construction_age,
                    'Interior/Exterior': interior_exterior,
                    'Ascensor': elevator,
                    'Calidad Acabados': finish_quality,
                    'Estado, Conservación *': conservation_state,
                    'Ubicación': location_quality,
                    'Estrato': stratum,
                    'observaciones': '',
                    'Medio de Contacto': contact_method,
                    'Contacto **': contact
                }
                
                processed.append(processed_prop)
                
            except Exception as e:
                logger.warning(f"Error processing apartment/house property: {str(e)}")
                continue
        
        return processed
    
    def _process_lote_properties(self, properties: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process properties for lote CSV format"""
        processed = []
        
        for prop in properties:
            try:
                # Extract basic information
                address = prop.get('address', '')
                property_url = prop.get('property_url', '')
                direccion_links = f"{address}, {property_url}" if property_url else address
                
                # Extract pricing information
                price = self._extract_price_value(prop.get('price', ''))
                area_util = self._extract_area_value(prop.get('area', ''))
                area_total = area_util  # For lots, util area is typically the total
                
                # Extract administration
                administration = self._extract_administration(prop)
                
                # Extract areas
                area_deposito = 0  # Default, would need specific extraction
                
                # Extract boolean amenities
                amenities = prop.get('amenities', [])
                mezanine = 'SI' if 'mezanine' in amenities else 'NO'
                cocina = 'SI' if 'cocina' in amenities else 'NO'
                bodega = 'SI' if 'bodega' in amenities else 'NO'
                
                # Extract numeric values
                bathrooms = prop.get('bathrooms', 0) or 0
                floor = self._extract_floor(prop)
                parking = prop.get('parking', 0) or 0
                construction_year = self._extract_construction_year(prop)
                
                # Extract stratum
                stratum = prop.get('stratum', 0) or 0
                
                # Extract property code (from URL or title)
                codigo_inmueble = self._extract_property_code(prop)
                
                # Extract contact information
                contact = prop.get('contact', '')
                contact_method = 'F.R.'  # Default
                
                processed_prop = {
                    'Dirección, links': direccion_links,
                    'VENTA': price,
                    'Area Util m2': area_util,
                    'Precio Incluido': price,
                    'Administración': administration,
                    'Area deposito': area_deposito,
                    'Area Total': area_total,
                    'Mezanine': mezanine,
                    'Baños': bathrooms,
                    'Cocina': cocina,
                    'Bodega': bodega,
                    'Piso': floor,
                    'Parqueadero': parking,
                    'Año construcción': construction_year,
                    'Estrato': stratum,
                    'Código inmueble': codigo_inmueble,
                    'observaciones': '',
                    'Medio de Contacto': contact_method,
                    'Contacto **': contact
                }
                
                processed.append(processed_prop)
                
            except Exception as e:
                logger.warning(f"Error processing lote property: {str(e)}")
                continue
        
        return processed
    
    def _extract_price_value(self, price_str: str) -> float:
        """Extract numeric price value from price string"""
        if not price_str:
            return 0.0
        
        # Remove common currency symbols and text
        import re
        price_clean = re.sub(r'[^\d]', '', price_str)
        try:
            return float(price_clean) if price_clean else 0.0
        except ValueError:
            return 0.0
    
    def _extract_area_value(self, area_str: str) -> float:
        """Extract numeric area value from area string"""
        if not area_str:
            return 0.0
        
        import re
        area_match = re.search(r'(\d+(?:\.\d+)?)', area_str)
        try:
            return float(area_match.group(1)) if area_match else 0.0
        except (ValueError, AttributeError):
            return 0.0
    
    def _extract_administration(self, prop: Dict[str, Any]) -> float:
        """Extract administration fee"""
        # This would need to be extracted from the property data
        # For now, return a default value
        return 0.0
    
    def _extract_floor(self, prop: Dict[str, Any]) -> int:
        """Extract floor number"""
        # This would need to be extracted from the property data
        return 0
    
    def _extract_construction_age(self, prop: Dict[str, Any]) -> int:
        """Extract construction age in years"""
        # This would need to be extracted from the property data
        return 0
    
    def _extract_construction_year(self, prop: Dict[str, Any]) -> int:
        """Extract construction year"""
        # This would need to be extracted from the property data
        return 0
    
    def _extract_interior_exterior(self, prop: Dict[str, Any]) -> str:
        """Extract interior/exterior classification"""
        # This would need to be extracted from the property data
        return 'I'  # Default to Interior
    
    def _extract_property_code(self, prop: Dict[str, Any]) -> str:
        """Extract property code from URL or title"""
        property_url = prop.get('property_url', '')
        if property_url:
            # Extract code from URL (e.g., last part of URL)
            import re
            code_match = re.search(r'/(\d+)/?$', property_url)
            if code_match:
                return code_match.group(1)
        
        # Fallback to title or return empty
        return prop.get('title', '')[:20] if prop.get('title') else ''
    
    def _write_csv(self, properties: List[Dict[str, Any]], columns: List[str], output_file: str) -> bool:
        """Write properties to CSV file"""
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns)
                writer.writeheader()
                
                for prop in properties:
                    # Ensure all columns are present
                    row = {col: prop.get(col, '') for col in columns}
                    writer.writerow(row)
            
            return True
            
        except Exception as e:
            logger.error(f"Error writing CSV file: {str(e)}")
            return False
