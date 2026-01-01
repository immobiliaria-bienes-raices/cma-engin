"""
Portal-specific data adapters for Colombian real estate websites.
Each adapter maps portal-specific data structures to the unified JSON schema.
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from bs4 import BeautifulSoup


class BasePortalAdapter:
    """Base class for all portal adapters"""
    
    def __init__(self, portal_name: str):
        self.portal_name = portal_name
    
    def extract_property_data(self, html_content: str, url: str) -> Dict[str, Any]:
        """Extract property data from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        return self._normalize_data(self._extract_raw_data(soup, url))
    
    def _extract_raw_data(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Extract raw data from HTML - to be implemented by subclasses"""
        raise NotImplementedError
    
    def _normalize_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize raw data to unified schema"""
        return {
            "property_id": self._generate_property_id(raw_data),
            "address": self._extract_address(raw_data),
            "characteristics": self._extract_characteristics(raw_data),
            "pricing": self._extract_pricing(raw_data),
            "metadata": self._extract_metadata(raw_data, url)
        }
    
    def _generate_property_id(self, raw_data: Dict[str, Any]) -> str:
        """Generate unique property ID"""
        return f"{self.portal_name}_{raw_data.get('internal_id', 'unknown')}"
    
    def _extract_address(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract address information"""
        return {
            "street": raw_data.get('street', ''),
            "neighborhood": raw_data.get('neighborhood', ''),
            "city": raw_data.get('city', ''),
            "coordinates": raw_data.get('coordinates', {})
        }
    
    def _extract_characteristics(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract property characteristics"""
        return {
            "property_type": self._normalize_property_type(raw_data.get('property_type', '')),
            "sale_type": raw_data.get('sale_type', 'sale'),
            "area_habitable": self._parse_number(raw_data.get('area_habitable', 0)),
            "area_total": self._parse_number(raw_data.get('area_total', 0)),
            "area_terrace": self._parse_number(raw_data.get('area_terrace', 0)),
            "bedrooms": self._parse_int(raw_data.get('bedrooms', 0)),
            "bathrooms": self._parse_number(raw_data.get('bathrooms', 0)),
            "parking": self._parse_boolean(raw_data.get('parking', False)),
            "walking_closet": self._parse_boolean(raw_data.get('walking_closet', False)),
            "loft": self._parse_boolean(raw_data.get('loft', False)),
            "study_room": self._parse_boolean(raw_data.get('study_room', False)),
            "floor": self._parse_int(raw_data.get('floor', 0)),
            "service_room": self._parse_int(raw_data.get('service_room', 0)),
            "deposit": self._parse_number(raw_data.get('deposit', 0)),
            "construction_age": self._parse_int(raw_data.get('construction_age', 0)),
            "interior_exterior": raw_data.get('interior_exterior', 'exterior'),
            "elevator": self._parse_boolean(raw_data.get('elevator', False)),
            "finish_quality": self._parse_int(raw_data.get('finish_quality', 3)),
            "conservation_state": self._parse_int(raw_data.get('conservation_state', 3)),
            "stratum": self._parse_int(raw_data.get('stratum', 3)),
            "location_quality": self._parse_int(raw_data.get('location_quality', 3))
        }
    
    def _extract_pricing(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract pricing information"""
        sale_price = self._parse_number(raw_data.get('sale_price', 0))
        area_habitable = self._parse_number(raw_data.get('area_habitable', 1))
        
        return {
            "sale_price": sale_price,
            "price_per_m2": sale_price / area_habitable if area_habitable > 0 else 0,
            "administration": self._parse_number(raw_data.get('administration', 0)),
            "administration_per_m2": self._parse_number(raw_data.get('administration', 0)) / area_habitable if area_habitable > 0 else 0,
            "rent_price": self._parse_number(raw_data.get('rent_price', 0))
        }
    
    def _extract_metadata(self, raw_data: Dict[str, Any], url: str) -> Dict[str, Any]:
        """Extract metadata information"""
        return {
            "source_portal": self.portal_name,
            "listing_url": url,
            "contact_info": raw_data.get('contact_info', ''),
            "listing_date": raw_data.get('listing_date', ''),
            "last_updated": raw_data.get('last_updated', ''),
            "scraping_timestamp": datetime.now().isoformat()
        }
    
    def _normalize_property_type(self, property_type: str) -> str:
        """Normalize property type to standard values"""
        type_mapping = {
            'apartamento': 'apartment',
            'casa': 'house',
            'apartaestudio': 'studio',
            'comercial': 'commercial',
            'oficina': 'office',
            'bodega': 'warehouse'
        }
        return type_mapping.get(property_type.lower(), 'apartment')
    
    def _parse_number(self, value: Any) -> float:
        """Parse string/number to float"""
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            # Remove currency symbols and commas
            cleaned = re.sub(r'[^\d.,]', '', value)
            cleaned = cleaned.replace(',', '')
            try:
                return float(cleaned)
            except ValueError:
                return 0.0
        return 0.0
    
    def _parse_int(self, value: Any) -> int:
        """Parse string/number to int"""
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        if isinstance(value, str):
            try:
                return int(float(value))
            except ValueError:
                return 0
        return 0
    
    def _parse_boolean(self, value: Any) -> bool:
        """Parse value to boolean"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ['true', 'yes', 'si', 'sí', '1', 'on']
        return bool(value)


class CiencuadrasAdapter(BasePortalAdapter):
    """Adapter for Ciencuadras portal"""
    
    def __init__(self):
        super().__init__("ciencuadras")
    
    def _extract_raw_data(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Extract raw data from Ciencuadras HTML"""
        raw_data = {}
        
        # Extract property details from structured data
        script_tags = soup.find_all('script', type='application/ld+json')
        for script in script_tags:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and data.get('@type') == 'RealEstateAgent':
                    raw_data.update(self._extract_from_structured_data(data))
            except json.JSONDecodeError:
                continue
        
        # Extract from HTML elements
        raw_data.update(self._extract_from_html_elements(soup))
        
        return raw_data
    
    def _extract_from_structured_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract data from JSON-LD structured data"""
        result = {}
        
        if 'address' in data:
            address = data['address']
            result['street'] = address.get('streetAddress', '')
            result['neighborhood'] = address.get('addressLocality', '')
            result['city'] = address.get('addressRegion', '')
        
        if 'offers' in data:
            offers = data['offers']
            result['sale_price'] = offers.get('price', 0)
            result['sale_type'] = 'sale' if 'price' in offers else 'rent'
        
        return result
    
    def _extract_from_html_elements(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract data from HTML elements"""
        result = {}
        
        # Price extraction
        price_element = soup.find('span', class_='price')
        if price_element:
            result['sale_price'] = price_element.get_text(strip=True)
        
        # Property characteristics
        features = soup.find_all('div', class_='feature')
        for feature in features:
            label = feature.find('span', class_='label')
            value = feature.find('span', class_='value')
            if label and value:
                self._map_feature_to_raw_data(result, label.get_text(strip=True), value.get_text(strip=True))
        
        return result
    
    def _map_feature_to_raw_data(self, raw_data: Dict[str, Any], label: str, value: str):
        """Map feature labels to raw data fields"""
        label_lower = label.lower()
        
        if 'área' in label_lower or 'area' in label_lower:
            raw_data['area_habitable'] = value
        elif 'habitaciones' in label_lower or 'alcobas' in label_lower:
            raw_data['bedrooms'] = value
        elif 'baños' in label_lower:
            raw_data['bathrooms'] = value
        elif 'parqueadero' in label_lower:
            raw_data['parking'] = value
        elif 'piso' in label_lower:
            raw_data['floor'] = value
        elif 'estrato' in label_lower:
            raw_data['stratum'] = value


class ProperatiAdapter(BasePortalAdapter):
    """Adapter for Properati portal"""
    
    def __init__(self):
        super().__init__("properati")
    
    def _extract_raw_data(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Extract raw data from Properati HTML"""
        raw_data = {}
        
        # Extract from posting card
        posting_card = soup.find('div', class_='posting-card')
        if posting_card:
            raw_data.update(self._extract_from_posting_card(posting_card))
        
        # Extract from detailed view
        details = soup.find('div', class_='posting-details')
        if details:
            raw_data.update(self._extract_from_details(details))
        
        return raw_data
    
    def _extract_from_posting_card(self, card) -> Dict[str, Any]:
        """Extract data from posting card"""
        result = {}
        
        # Price
        price_element = card.find('div', class_='price')
        if price_element:
            result['sale_price'] = price_element.get_text(strip=True)
        
        # Address
        address_element = card.find('div', class_='location')
        if address_element:
            result['neighborhood'] = address_element.get_text(strip=True)
        
        # Features
        features = card.find_all('div', class_='feature')
        for feature in features:
            text = feature.get_text(strip=True)
            self._parse_feature_text(result, text)
        
        return result
    
    def _extract_from_details(self, details) -> Dict[str, Any]:
        """Extract data from detailed view"""
        result = {}
        
        # Extract all feature rows
        feature_rows = details.find_all('div', class_='feature-row')
        for row in feature_rows:
            label = row.find('span', class_='label')
            value = row.find('span', class_='value')
            if label and value:
                self._map_feature_to_raw_data(result, label.get_text(strip=True), value.get_text(strip=True))
        
        return result
    
    def _parse_feature_text(self, raw_data: Dict[str, Any], text: str):
        """Parse feature text to extract values"""
        # Look for patterns like "3 hab", "2 baños", "80 m²"
        patterns = {
            r'(\d+)\s*hab': 'bedrooms',
            r'(\d+)\s*baños?': 'bathrooms',
            r'(\d+(?:\.\d+)?)\s*m²': 'area_habitable',
            r'(\d+)\s*piso': 'floor'
        }
        
        for pattern, field in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                raw_data[field] = match.group(1)


class FincaraizAdapter(BasePortalAdapter):
    """Adapter for Fincaraiz portal"""
    
    def __init__(self):
        super().__init__("fincaraiz")
    
    def _extract_raw_data(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Extract raw data from Fincaraiz HTML"""
        raw_data = {}
        
        # Extract from property item
        property_item = soup.find('div', class_='property-item')
        if property_item:
            raw_data.update(self._extract_from_property_item(property_item))
        
        # Extract from property details
        property_details = soup.find('div', class_='property-details')
        if property_details:
            raw_data.update(self._extract_from_property_details(property_details))
        
        return raw_data
    
    def _extract_from_property_item(self, item) -> Dict[str, Any]:
        """Extract data from property item"""
        result = {}
        
        # Price
        price_element = item.find('div', class_='price')
        if price_element:
            result['sale_price'] = price_element.get_text(strip=True)
        
        # Address
        address_element = item.find('div', class_='address')
        if address_element:
            result['neighborhood'] = address_element.get_text(strip=True)
        
        # Features
        features = item.find_all('div', class_='feature')
        for feature in features:
            text = feature.get_text(strip=True)
            self._parse_feature_text(result, text)
        
        return result
    
    def _extract_from_property_details(self, details) -> Dict[str, Any]:
        """Extract data from property details"""
        result = {}
        
        # Extract characteristics table
        characteristics_table = details.find('table', class_='characteristics')
        if characteristics_table:
            rows = characteristics_table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 2:
                    label = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)
                    self._map_feature_to_raw_data(result, label, value)
        
        return result


class MetrocuadradoAdapter(BasePortalAdapter):
    """Adapter for Metrocuadrado portal"""
    
    def __init__(self):
        super().__init__("metrocuadrado")
    
    def _extract_raw_data(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Extract raw data from Metrocuadrado HTML"""
        raw_data = {}
        
        # Extract from property card
        property_card = soup.find('div', class_='property-card')
        if property_card:
            raw_data.update(self._extract_from_property_card(property_card))
        
        # Extract from specifications
        specifications = soup.find('div', class_='property-specifications')
        if specifications:
            raw_data.update(self._extract_from_specifications(specifications))
        
        return raw_data
    
    def _extract_from_property_card(self, card) -> Dict[str, Any]:
        """Extract data from property card"""
        result = {}
        
        # Price
        price_element = card.find('div', class_='property-pricing')
        if price_element:
            result['sale_price'] = price_element.get_text(strip=True)
        
        # Location
        location_element = card.find('div', class_='property-location')
        if location_element:
            result['neighborhood'] = location_element.get_text(strip=True)
        
        return result
    
    def _extract_from_specifications(self, specs) -> Dict[str, Any]:
        """Extract data from specifications"""
        result = {}
        
        # Extract specification items
        spec_items = specs.find_all('div', class_='spec-item')
        for item in spec_items:
            label = item.find('span', class_='label')
            value = item.find('span', class_='value')
            if label and value:
                self._map_feature_to_raw_data(result, label.get_text(strip=True), value.get_text(strip=True))
        
        return result


# Factory function to get the appropriate adapter
def get_portal_adapter(portal_name: str) -> BasePortalAdapter:
    """Get the appropriate adapter for a portal"""
    adapters = {
        'ciencuadras': CiencuadrasAdapter,
        'properati': ProperatiAdapter,
        'fincaraiz': FincaraizAdapter,
        'metrocuadrado': MetrocuadradoAdapter
    }
    
    adapter_class = adapters.get(portal_name.lower())
    if not adapter_class:
        raise ValueError(f"No adapter found for portal: {portal_name}")
    
    return adapter_class()


# Example usage
if __name__ == "__main__":
    # Test the adapters
    test_html = """
    <div class="property-card">
        <div class="price">$250,000,000</div>
        <div class="location">Cedritos, Bogotá</div>
        <div class="features">
            <span>3 hab</span>
            <span>2 baños</span>
            <span>80 m²</span>
        </div>
    </div>
    """
    
    adapter = get_portal_adapter('properati')
    result = adapter.extract_property_data(test_html, 'https://example.com')
    print(json.dumps(result, indent=2, ensure_ascii=False))
