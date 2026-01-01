"""
Fincaraiz.com.co Property Search Mapper
Maps property_schema.json data to Fincaraiz-specific search queries
"""

import json
import urllib.parse
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import re


class FincaraizMapper:
    """Maps property schema data to Fincaraiz search queries"""
    
    def __init__(self):
        self.base_url = "https://www.fincaraiz.com.co"
        
        # Fincaraiz uses path-based URLs with specific structure
        # Structure: /{operation}/{city}/{neighborhoods_combined}/{publication_date}?{other_filters}
        # Example: /arriendo/bogota-dc/bella-suiza-y-en-santa-barbara/publicado-ultimos-30-dias?&stratum[]=2
        
        # Operation type mapping
        self.operation_mapping = {
            'ARRIENDO': 'arriendo',
            'VENTA': 'venta'
        }
        
        # Property type mapping (Fincaraiz specific values)
        self.property_type_mapping = {
            'Casa': 'casas',
            'Apartamento': 'apartamentos',
            'Apartaestudio': 'apartaestudios',
            'Cabaña': 'cabanas',
            'Casa Campestre': 'casas-campestres',
            'Casa Lote': 'casas-lote',
            'Finca': 'fincas',
            'Habitación': 'habitaciones',
            'Lote': 'lotes',
            'Bodega': 'bodegas',
            'Consultorio': 'consultorios',
            'Local': 'locales',
            'Oficina': 'oficinas',
            'Parqueadero': 'parqueaderos',
            'Edificio': 'edificios',
            # Legacy mappings for backward compatibility
            'apartment': 'apartamentos',
            'house': 'casas',
            'studio': 'apartaestudios',
            'commercial': 'comercial',
            'office': 'oficinas',
            'warehouse': 'bodegas'
        }
        
        # Fixed to Bogotá only - using correct Fincaraiz format
        self.fixed_city = 'bogota-dc'
        
        # Bogotá zones mapping (localidades)
        self.zone_mapping = {
            'usaquen': 'usaquen',
            'chapinero': 'chapinero',
            'santa fe': 'santa-fe',
            'san cristobal': 'san-cristobal',
            'usme': 'usme',
            'tunjuelito': 'tunjuelito',
            'bosa': 'bosa',
            'kennedy': 'kennedy',
            'fontibon': 'fontibon',
            'engativa': 'engativa',
            'suba': 'suba',
            'barrios unidos': 'barrios-unidos',
            'teusaquillo': 'teusaquillo',
            'los martires': 'los-martires',
            'antonio nariño': 'antonio-narino',
            'puente aranda': 'puente-aranda',
            'candelaria': 'candelaria',
            'rafael uribe uribe': 'rafael-uribe-uribe',
            'ciudad bolivar': 'ciudad-bolivar',
            'sumapaz': 'sumapaz'
        }
        
        # Bogotá neighborhoods mapping (barrios populares)
        self.neighborhood_mapping = {
            # Zona Norte
            'cedritos': 'cedritos',
            'niza': 'niza',
            'suba': 'suba',
            'cajica': 'cajica',
            'chico': 'chico',
            'rosales': 'rosales',
            'zona rosa': 'zona-rosa',
            'chapinero': 'chapinero',
            'teusaquillo': 'teusaquillo',
            'la macarena': 'la-macarena',
            'candelaria': 'candelaria',
            'la candelaria': 'la-candelaria',
            
            # Zona Centro
            'santa fe': 'santa-fe',
            'los martires': 'los-martires',
            'antonio nariño': 'antonio-narino',
            'puente aranda': 'puente-aranda',
            
            # Zona Sur
            'kennedy': 'kennedy',
            'bosa': 'bosa',
            'fontibon': 'fontibon',
            'engativa': 'engativa',
            'suba': 'suba',
            'barrios unidos': 'barrios-unidos',
            'tunjuelito': 'tunjuelito',
            'usme': 'usme',
            'san cristobal': 'san-cristobal',
            'rafael uribe uribe': 'rafael-uribe-uribe',
            'ciudad bolivar': 'ciudad-bolivar',
            
            # Zona Occidente
            'fontibon': 'fontibon',
            'engativa': 'engativa',
            'suba': 'suba',
            'barrios unidos': 'barrios-unidos',
            
            # Zona Oriente
            'usaquen': 'usaquen',
            'chapinero': 'chapinero',
            'santa fe': 'santa-fe',
            'san cristobal': 'san-cristobal',
            'usme': 'usme',
            'tunjuelito': 'tunjuelito',
            'bosa': 'bosa',
            'kennedy': 'kennedy',
            'fontibon': 'fontibon',
            'engativa': 'engativa',
            'suba': 'suba',
            'barrios unidos': 'barrios-unidos',
            'teusaquillo': 'teusaquillo',
            'los martires': 'los-martires',
            'antonio nariño': 'antonio-narino',
            'puente aranda': 'puente-aranda',
            'candelaria': 'candelaria',
            'rafael uribe uribe': 'rafael-uribe-uribe',
            'ciudad bolivar': 'ciudad-bolivar'
        }
        
        # Bedroom filter mapping (Fincaraiz path format)
        self.bedroom_filter_mapping = {
            0: 'sin-habitaciones',
            1: '1-o-mas-habitaciones',
            2: '2-o-mas-habitaciones', 
            3: '3-o-mas-habitaciones',
            4: '4-o-mas-habitaciones',
            5: '5-o-mas-habitaciones'
        }
        
        # Bathroom filter mapping
        self.bathroom_filter_mapping = {
            0: 'sin-banos',
            1: '1-o-mas-banos',
            2: '2-o-mas-banos',
            3: '3-o-mas-banos',
            4: '4-o-mas-banos',
            5: '5-o-mas-banos'
        }
        
        # Amenities mapping (exact Fincaraiz parameter names with "con-" prefix)
        self.amenities_mapping = {
            'elevator': 'con-ascensor',
            'balcony': 'con-balcon',
            'garden': 'con-jardin',
            'pool': 'con-piscina',
            'gym': 'con-gimnasio',
            'security': 'con-vigilancia',
            'parking_visitors': 'con-parqueadero-visitantes',
            'children_area': 'con-zona-infantil',
            'social_room': 'con-salon-comunal',
            'laundry': 'con-lavanderia',
            'closet': 'con-closet',
            'study': 'con-estudio',
            'loft': 'con-loft',
            'bbq': 'con-zona-bbq',
            'parking': 'con-parqueadero',
            'porteria': 'con-porteria',
            'alarm': 'con-alarma',
            'air_conditioning': 'con-aire-acondicionado',
            'furnished': 'con-amoblado',
            'kitchen': 'con-cocina-integral',
            'deposit': 'con-deposito',
            'service_room': 'con-cuarto-servicio',
            'terrace': 'con-terraza',
            'view': 'con-vista-panoramica'
        }
        
        # Construction age mapping (exact Fincaraiz values)
        self.construction_age_mapping = {
            'nuevo': 'Menor a 1 año',
            'semi-nuevo': 'De 1 a 8 años', 
            'usado': 'De 9 a 15 años',
            'antiguo': 'De 16 a 30 años',
            'muy_antiguo': 'Más de 30 años'
        }
        
        # Property status mapping
        self.property_status_mapping = {
            'built': 'edificados',
            'under_construction': 'en-construccion',
            'plans': 'sobre-planos'
        }
        
        # Publication date mapping
        self.publication_date_mapping = {
            'Indiferente': '',  # No filter
            'Hoy': 'publicado-hoy',
            'Desde ayer': 'publicado-desde-ayer',
            'Última Semana': 'publicado-ultimos-7-dias',
            'Últimos 15 días': 'publicado-ultimos-15-dias',
            'Últimos 30 días': 'publicado-ultimos-30-dias',
            'Últimos 40 días': 'publicado-ultimos-40-dias'
        }
        
        # Floor mapping (exact Fincaraiz values)
        self.floor_mapping = {
            'ground': 'Primer Piso',
            'low': '2do al 5to piso',
            'mid': '6to al 10mo piso',
            'high': '+10mo piso',
            'penthouse': 'Penthouse'
        }
        
        # Stratum mapping (exact Fincaraiz values)
        self.stratum_mapping = {
            1: '1',
            2: '2',
            3: '3',
            4: '4',
            5: '5',
            6: '6',
            'campestre': 'Campestre'
        }
        
        # Search tolerance settings
        self.price_tolerance = 0.25  # 25% price range tolerance
        self.area_tolerance = 0.20   # 20% area range tolerance
        self.bedroom_tolerance = 1   # ±1 bedroom tolerance
        self.bathroom_tolerance = 0.5 # ±0.5 bathroom tolerance
    
    def map_property_to_search(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map property schema data to Fincaraiz search query
        
        Args:
            property_data: Property data matching property_schema.json
            
        Returns:
            Dictionary containing search URL, parameters, and metadata
        """
        try:
            # Extract and validate property data
            search_params = self._extract_search_parameters(property_data)
            
            # Build search URL (handles single or multiple neighborhoods)
            search_url = self._build_search_url(search_params)
            
            # Generate search metadata
            search_metadata = self._generate_search_metadata(property_data, search_params)
            
            return {
                'search_url': search_url,
                'search_params': search_params,
                'metadata': search_metadata,
                'portal': 'fincaraiz',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'error': f"Failed to map property to Fincaraiz search: {str(e)}",
                'portal': 'fincaraiz',
                'timestamp': datetime.now().isoformat()
            }
    
    def _extract_search_parameters(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract search parameters from property data for path-based URLs"""
        
        # Basic operation and property type
        operation = self.operation_mapping.get(property_data.get('operation', 'VENTA'), 'venta')
        
        # Use property type from form data directly
        property_type_key = property_data.get('property_type', 'Apartamento')
        property_type = self.property_type_mapping.get(property_type_key, 'apartamentos')  # Default to apartments
        
        # Location extraction - fixed to Bogotá
        address = property_data.get('address', '')
        city = self.fixed_city  # Always Bogotá
        
        # Use form data if available, otherwise extract from address
        zone = property_data.get('zone') or self._extract_zone_from_address(address)
        
        # Handle multiple neighborhoods
        neighborhoods = property_data.get('neighborhoods', [])
        if not neighborhoods:
            # Fallback to single neighborhood for backward compatibility
            single_neighborhood = property_data.get('neighborhood') or self._extract_neighborhood_from_address(address)
            if single_neighborhood:
                neighborhoods = [single_neighborhood]
        
        # Price calculation with tolerance
        price_params = self._calculate_price_range(property_data)
        
        # Area calculation with tolerance
        area_params = self._calculate_area_range(property_data)
        
        # Property characteristics
        characteristics = self._extract_characteristics(property_data)
        
        # Combine all parameters for path-based URL
        search_params = {
            'tipo_operacion': operation,
            'tipo_inmueble': property_type,
            'bedrooms': property_data.get('bedrooms', 1),  # For bedroom filter
            'bathrooms': property_data.get('bathrooms', 1),  # For bathroom filter
            **price_params,
            **area_params,
            **characteristics
        }
        
        # Add location if available
        if city:
            search_params['ciudad'] = city
        if zone:
            search_params['zona'] = zone
        if neighborhoods:
            search_params['barrios'] = neighborhoods  # Changed to plural for multiple neighborhoods
            
        # Add advanced filters
        advanced_filters = self._extract_advanced_filters(property_data)
        search_params.update(advanced_filters)
            
        return search_params
    
    def _calculate_price_range(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate price range with user-specified tolerance"""
        pricing = property_data.get('pricing', {})
        price_per_m2 = pricing.get('price_per_m2', 0)
        # Use area_total as primary, fallback to area_habitable if area_total is not available
        area = property_data.get('area_total', property_data.get('area_habitable', 0))
        
        # Use user-specified price tolerance, fallback to default
        price_tolerance = property_data.get('price_tolerance', self.price_tolerance)
        # Convert percentage to decimal (e.g., 20% -> 0.2)
        tolerance_decimal = price_tolerance / 100.0
        
        if price_per_m2 and area:
            total_price = price_per_m2 * area
            min_price = int(total_price * (1 - tolerance_decimal))
            max_price = int(total_price * (1 + tolerance_decimal))
            
            return {
                'precio_min': min_price,
                'precio_max': max_price
            }
        
        return {}
    
    def _calculate_area_range(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate area range with user-specified tolerance"""
        # Use area_total as primary, fallback to area_habitable if area_total is not available
        area = property_data.get('area_total', property_data.get('area_habitable', 0))
        
        # Use user-specified area tolerance, fallback to default
        area_tolerance = property_data.get('area_tolerance', self.area_tolerance)
        # Convert percentage to decimal (e.g., 20% -> 0.2)
        tolerance_decimal = area_tolerance / 100.0
        
        if area:
            min_area = round(area * (1 - tolerance_decimal))
            max_area = round(area * (1 + tolerance_decimal))
            
            return {
                'area_min': min_area,
                'area_max': max_area
            }
        
        return {}
    
    def _extract_characteristics(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract property characteristics for search (simplified for path-based URLs)"""
        characteristics = {}
        
        # For path-based URLs, we mainly need the basic characteristics
        # Complex filtering will be handled by the path structure
        
        # Stratum (can be used in query parameters if needed)
        stratum = property_data.get('stratum')
        if stratum:
            characteristics['estrato'] = stratum
        
        # Construction age (can be used in query parameters if needed)
        construction_age = property_data.get('construction_age')
        if construction_age:
            characteristics['antiguedad'] = self._map_construction_age(construction_age)
        
        # Elevator (can be used in query parameters if needed)
        elevator = property_data.get('elevator', False)
        if elevator:
            characteristics['ascensor'] = 'si'
        
        return characteristics
    
    def _extract_advanced_filters(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract advanced filters for enhanced search capabilities"""
        advanced_filters = {}
        
        # Amenities
        amenities = self._extract_amenities(property_data)
        if amenities:
            advanced_filters['amenities'] = amenities
        
        # Parking spaces
        parking = property_data.get('parking', 0)
        if parking and parking > 0:
            advanced_filters['parking_spaces'] = f"{parking}-parqueaderos"
        
        # Floor number
        floor = property_data.get('floor')
        if floor and floor > 0:
            floor_category = self._map_floor_to_category(floor)
            advanced_filters['floor'] = floor_category
        
        # Construction age
        construction_age = property_data.get('construction_age')
        if construction_age:
            age_category = self._map_construction_age(construction_age)
            advanced_filters['construction_age'] = self.construction_age_mapping.get(age_category, 'usados')
        
        # Property status (default to built)
        advanced_filters['property_status'] = 'edificados'
        
        # Publication date (use user-specified or default to last 7 days)
        publication_date = property_data.get('publication_date', 'Última Semana')
        advanced_filters['publication_date'] = self.publication_date_mapping.get(publication_date, 'publicado-ultimos-7-dias')
        
        return advanced_filters
    
    def _extract_amenities(self, property_data: Dict[str, Any]) -> str:
        """Extract amenities and format them for Fincaraiz path"""
        amenities = []
        
        # Check for specific amenities using exact Fincaraiz parameter names
        if property_data.get('elevator', False):
            amenities.append(self.amenities_mapping['elevator'])
        
        if property_data.get('terrace', False) or property_data.get('terrace_area', 0) > 0:
            amenities.append(self.amenities_mapping['balcony'])
        
        if property_data.get('walking_closet', False):
            amenities.append(self.amenities_mapping['closet'])
        
        if property_data.get('study_room', False):
            amenities.append(self.amenities_mapping['study'])
        
        if property_data.get('loft', False):
            amenities.append(self.amenities_mapping['loft'])
        
        # Add more amenities based on property data
        # Note: Removed automatic security addition based on stratum
        
        if property_data.get('area_total', 0) > 100:
            amenities.append(self.amenities_mapping['garden'])
        
        # Add parking if available
        if property_data.get('parking', 0) > 0:
            amenities.append(self.amenities_mapping['parking'])
        
        # Add deposit if available
        if property_data.get('deposit', 0) > 0:
            amenities.append(self.amenities_mapping['deposit'])
        
        # Join amenities with '-y-' separator for path-based URLs
        return '-y-'.join(amenities) if amenities else None
    
    def _map_construction_age(self, age: int) -> str:
        """Map construction age to Fincaraiz categories"""
        if age < 1:
            return 'nuevo'
        elif age <= 8:
            return 'semi-nuevo'
        elif age <= 15:
            return 'usado'
        elif age <= 30:
            return 'antiguo'
        else:
            return 'muy_antiguo'
    
    def _map_floor_to_category(self, floor: int) -> str:
        """Map floor number to Fincaraiz floor categories"""
        if floor == 1:
            return self.floor_mapping['ground']
        elif 2 <= floor <= 5:
            return self.floor_mapping['low']
        elif 6 <= floor <= 10:
            return self.floor_mapping['mid']
        elif floor > 10:
            return self.floor_mapping['high']
        else:
            return self.floor_mapping['ground']
    
    def _infer_property_type(self, property_data: Dict[str, Any]) -> str:
        """Infer property type from property data"""
        # Check if it's explicitly specified
        if 'property_type' in property_data:
            return property_data['property_type']
        
        # Infer from characteristics
        floor = property_data.get('floor', None)
        area_total = property_data.get('area_total', 0)
        area_habitable = property_data.get('area_habitable', 0)
        
        # Use area_total as primary, fallback to area_habitable
        primary_area = area_total if area_total > 0 else area_habitable
        
        # Houses typically have floor 0 and larger areas
        if floor == 0 and area_total > 100:
            return 'house'
        
        # Studios typically have small areas
        if primary_area < 30:
            return 'studio'
        
        # Default to apartment
        return 'apartment'
    
    def _extract_zone_from_address(self, address: str) -> Optional[str]:
        """Extract zone (localidad) from address string for Bogotá"""
        address_lower = address.lower()
        
        # Look for zone indicators
        zone_indicators = ['localidad', 'zona', 'sector']
        
        # First, try to find explicit zone mentions
        for zone_key, zone_value in self.zone_mapping.items():
            if zone_key in address_lower:
                return zone_value
        
        # Try to extract from common patterns
        # Look for patterns like "Localidad X" or "Zona X"
        for indicator in zone_indicators:
            pattern = rf'{indicator}\s+([a-zA-Z\s]+)'
            match = re.search(pattern, address_lower)
            if match:
                zone_name = match.group(1).strip().lower()
                if zone_name in self.zone_mapping:
                    return self.zone_mapping[zone_name]
        
        # Try to infer zone from neighborhood
        neighborhood = self._extract_neighborhood_from_address(address)
        if neighborhood:
            # Map neighborhood to zone based on common knowledge
            return self._map_neighborhood_to_zone(neighborhood)
        
        return None
    
    def _map_neighborhood_to_zone(self, neighborhood: str) -> Optional[str]:
        """Map neighborhood to zone based on Bogotá geography"""
        neighborhood_lower = neighborhood.lower()
        
        # Zona Norte
        norte_neighborhoods = ['cedritos', 'niza', 'suba', 'cajica', 'chico', 'rosales', 'zona rosa']
        if any(nb in neighborhood_lower for nb in norte_neighborhoods):
            return 'usaquen'  # Most northern neighborhoods are in Usaquén
        
        # Zona Centro
        centro_neighborhoods = ['chapinero', 'teusaquillo', 'la macarena', 'candelaria', 'la candelaria']
        if any(nb in neighborhood_lower for nb in centro_neighborhoods):
            return 'chapinero'  # Most central neighborhoods are in Chapinero
        
        # Zona Sur
        sur_neighborhoods = ['kennedy', 'bosa', 'fontibon', 'engativa', 'tunjuelito', 'usme', 'san cristobal']
        if any(nb in neighborhood_lower for nb in sur_neighborhoods):
            if 'kennedy' in neighborhood_lower:
                return 'kennedy'
            elif 'bosa' in neighborhood_lower:
                return 'bosa'
            elif 'fontibon' in neighborhood_lower:
                return 'fontibon'
            elif 'engativa' in neighborhood_lower:
                return 'engativa'
            elif 'tunjuelito' in neighborhood_lower:
                return 'tunjuelito'
            elif 'usme' in neighborhood_lower:
                return 'usme'
            elif 'san cristobal' in neighborhood_lower:
                return 'san-cristobal'
        
        return None
    
    def _extract_neighborhood_from_address(self, address: str) -> Optional[str]:
        """Extract neighborhood from address string using Bogotá neighborhood mapping"""
        address_lower = address.lower()
        
        # First, try to find explicit neighborhood mentions using our mapping
        for neighborhood_key, neighborhood_value in self.neighborhood_mapping.items():
            if neighborhood_key in address_lower:
                return neighborhood_value
        
        # Common neighborhood indicators
        neighborhood_indicators = ['barrio', 'sector', 'zona', 'localidad']
        
        words = address.split()
        for i, word in enumerate(words):
            if word.lower() in neighborhood_indicators and i + 1 < len(words):
                neighborhood = words[i + 1].lower().rstrip(',')
                # Check if the extracted neighborhood is in our mapping
                if neighborhood in self.neighborhood_mapping:
                    return self.neighborhood_mapping[neighborhood]
                return neighborhood
        
        # Try to extract from common patterns
        # Look for patterns like "Calle X #Y-Z Barrio Name"
        pattern = r'(?:barrio|sector|zona)\s+([a-zA-Z\s]+)'
        match = re.search(pattern, address, re.IGNORECASE)
        if match:
            neighborhood = match.group(1).strip().lower().rstrip(',')
            # Check if the extracted neighborhood is in our mapping
            if neighborhood in self.neighborhood_mapping:
                return self.neighborhood_mapping[neighborhood]
            return neighborhood
        
        return None
    
    def _build_search_url(self, search_params: Dict[str, Any]) -> str:
        """Build Fincaraiz search URL using correct structure: /operation/city/neighborhoods/publication_date?filters"""

        # Start with base URL
        url_parts = [self.base_url]

        # Add operation (required)
        operation = search_params.get('tipo_operacion', 'venta')
        url_parts.append(operation)

        # Add city (required) - always Bogotá DC
        city = search_params.get('ciudad', 'bogota-dc')
        url_parts.append(city)

        # Add neighborhoods combined with -y-en-
        neighborhoods = search_params.get('barrios', [])
        if neighborhoods:
            # Format neighborhoods: lowercase and replace spaces with hyphens
            formatted_neighborhoods = []
            for neighborhood in neighborhoods:
                # Convert to lowercase and replace spaces with hyphens
                formatted = neighborhood.lower().replace(' ', '-')
                formatted_neighborhoods.append(formatted)
            
            # Combine neighborhoods with -y-en- separator
            neighborhoods_str = '-y-en-'.join(formatted_neighborhoods)
            url_parts.append(neighborhoods_str)

        # Add publication date (only if not empty)
        publication_date = search_params.get('publication_date', 'publicado-ultimos-7-dias')
        if publication_date:  # Only add if not empty (for "Indiferente")
            url_parts.append(publication_date)
        
        # Build base URL
        base_url = '/'.join(url_parts)
        
        # Add query parameters for all other filters
        query_params = self._build_query_params(search_params)
        if query_params:
            return f"{base_url}?{query_params}"
        
        return base_url
    
    def _get_bedroom_filter(self, bedrooms: int) -> str:
        """Get bedroom filter for path-based URL"""
        # If bedrooms is None or 0, return "todos" (no filter)
        if bedrooms is None or bedrooms <= 0:
            return 'todos'
        elif bedrooms >= 5:
            return self.bedroom_filter_mapping.get(5, '5-o-mas-habitaciones')
        else:
            return self.bedroom_filter_mapping.get(bedrooms, '1-o-mas-habitaciones')
    
    def _get_bathroom_filter(self, bathrooms: float) -> str:
        """Get bathroom filter for path-based URL"""
        # If bathrooms is None or 0, return "todos" (no filter)
        if bathrooms is None or bathrooms <= 0:
            return 'todos'
        
        bathroom_count = int(bathrooms)
        if bathroom_count >= 5:
            return self.bathroom_filter_mapping.get(5, '5-o-mas-banos')
        else:
            return self.bathroom_filter_mapping.get(bathroom_count, '1-o-mas-banos')
    
    def _get_age_range(self, search_params: Dict[str, Any]) -> str:
        """Get age range filter for path-based URL"""
        # This could be based on construction age or other criteria
        construction_age = search_params.get('construction_age')
        if construction_age == 'Menor a 1 año':
            return 'de-0-a-1-anios'
        elif construction_age == 'De 1 a 8 años':
            return 'de-1-a-8-anios'
        elif construction_age == 'De 9 a 15 años':
            return 'de-9-a-15-anios'
        elif construction_age == 'De 16 a 30 años':
            return 'de-16-a-30-anios'
        elif construction_age == 'Más de 30 años':
            return 'de-31-a-50-anios'
        return None
    
    def _build_query_params(self, search_params: Dict[str, Any]) -> str:
        """Build query parameters for the URL using exact Fincaraiz parameter names"""
        query_params = []
        
        # Add currency ID (default to Colombian Peso)
        query_params.append('IDmoneda=4')
        
        # Add property type as query parameter
        property_type = search_params.get('tipo_inmueble')
        if property_type:
            query_params.append(f'tipo[]={property_type}')
        
        # Add stratum if available (exact Fincaraiz parameter as array)
        stratum = search_params.get('estrato')
        if stratum:
            stratum_value = self.stratum_mapping.get(stratum, str(stratum))
            query_params.append(f'stratum[]={stratum_value}')
        
        # Add bedroom filter
        bedrooms = search_params.get('bedrooms')
        if bedrooms and bedrooms > 0:
            query_params.append(f'habitaciones[]={bedrooms}')
        
        # Add bathroom filter
        bathrooms = search_params.get('bathrooms')
        if bathrooms and bathrooms > 0:
            query_params.append(f'banos[]={bathrooms}')
        
        # Add price range filters
        price_from = search_params.get('precio_min')
        price_to = search_params.get('precio_max')
        if price_from:
            query_params.append(f'precio_desde={price_from}')
        if price_to:
            query_params.append(f'precio_hasta={price_to}')
        
        # Add area range filters
        area_from = search_params.get('area_min')
        area_to = search_params.get('area_max')
        if area_from:
            query_params.append(f'area_desde={area_from}')
        if area_to:
            query_params.append(f'area_hasta={area_to}')
        
        # Add amenities as query parameters
        amenities = search_params.get('amenities')
        if amenities:
            # Split amenities and add each as a separate parameter
            amenity_list = amenities.split('-y-')
            for amenity in amenity_list:
                query_params.append(f'extras[]={amenity}')
        
        # Add parking spaces
        parking = search_params.get('parking')
        if parking and parking > 0:
            query_params.append(f'parqueaderos[]={parking}')
        
        # Add construction age
        construction_age = search_params.get('construction_age')
        if construction_age:
            # URL encode the construction age value (e.g., "De 16 a 30 años")
            encoded_age = urllib.parse.quote(str(construction_age), safe='')
            query_params.append(f'antiguedad[]={encoded_age}')
        
        # Add floor
        floor = search_params.get('floor')
        if floor:
            query_params.append(f'piso[]={floor}')
        
        return '&'.join(query_params)
    
    def _generate_search_metadata(self, property_data: Dict[str, Any], search_params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate search metadata"""
        return {
            'original_property': {
                'address': property_data.get('address', ''),
                'operation': property_data.get('operation', ''),
                'area_habitable': property_data.get('area_habitable', 0),
                'area_total': property_data.get('area_total', 0),
                'bedrooms': property_data.get('bedrooms', 0),
                'bathrooms': property_data.get('bathrooms', 0),
                'stratum': property_data.get('stratum', 0)
            },
            'search_criteria': {
                'price_range': {
                    'min': search_params.get('precio_min'),
                    'max': search_params.get('precio_max')
                },
                'area_range': {
                    'min': search_params.get('area_min'),
                    'max': search_params.get('area_max')
                },
                'location': {
                    'city': search_params.get('ciudad'),
                    'zone': search_params.get('zona'),
                    'neighborhood': search_params.get('barrio')
                }
            },
            'tolerance_settings': {
                'price_tolerance': self.price_tolerance,
                'area_tolerance': self.area_tolerance,
                'bedroom_tolerance': self.bedroom_tolerance,
                'bathroom_tolerance': self.bathroom_tolerance
            }
        }
    
    def get_search_headers(self) -> Dict[str, str]:
        """Get appropriate headers for Fincaraiz requests"""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.fincaraiz.com.co/',
            'Origin': 'https://www.fincaraiz.com.co'
        }


# Example usage and testing
if __name__ == "__main__":
    # Example property data matching property_schema.json
    example_property = {
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
    
    # Test the mapper
    mapper = FincaraizMapper()
    search_result = mapper.map_property_to_search(example_property)
    
    print("Fincaraiz Search Mapping Result:")
    print(json.dumps(search_result, indent=2, ensure_ascii=False))
    
    print(f"\nGenerated Search URL (Path-based):")
    print(search_result['search_url'])
    
    # Test with different property types
    print(f"\n" + "="*50)
    print("TESTING DIFFERENT PROPERTY TYPES")
    print("="*50)
    
    # Test rental apartment
    rental_apt = {
        "address": "Calle 80 #11-42, Bogotá",
        "operation": "ARRIENDO",
        "area_habitable": 50.0,
        "bedrooms": 2,
        "bathrooms": 1,
        "stratum": 3,
        "pricing": {"price_per_m2": 30000}
    }
    
    rental_result = mapper.map_property_to_search(rental_apt)
    print(f"Rental Apartment URL: {rental_result['search_url']}")
    
    # Test sale house
    sale_house = {
        "address": "Carrera 15 #93-47, Medellín",
        "operation": "VENTA",
        "area_habitable": 120.0,
        "bedrooms": 3,
        "bathrooms": 2,
        "stratum": 5,
        "pricing": {"price_per_m2": 5000000}
    }
    
    sale_result = mapper.map_property_to_search(sale_house)
    print(f"Sale House URL: {sale_result['search_url']}")
