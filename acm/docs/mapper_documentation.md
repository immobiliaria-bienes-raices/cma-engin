# Mapper Documentation

## Overview

The mapper system transforms property data from the unified `property_schema.json` format into portal-specific search queries for Colombian real estate websites. Each portal has its own parameter naming conventions, URL structures, and search requirements.

## Architecture

```
Property Schema (JSON) → Portal Mapper → Portal-Specific Search URL
```

## Base Mapper Interface

All mappers should implement the following interface:

```python
class BaseMapper:
    def map_property_to_search(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map property schema data to portal-specific search query
        
        Args:
            property_data: Property data matching property_schema.json
            
        Returns:
            Dictionary containing:
            - search_url: Complete search URL
            - search_params: Dictionary of search parameters
            - metadata: Search metadata and original property info
        """
        pass
```

## Fincaraiz Mapper

### Implementation Status: ✅ Complete

**File**: `src/real_estate_analytics/mappers/fincaraiz_mapper.py`

### Key Features

1. **Path-Based URLs**: Uses Fincaraiz's path structure for location and filters
2. **Parameter Mapping**: Maps unified schema to Fincaraiz-specific parameters
3. **Tolerance Calculation**: Smart price and area range calculations
4. **Location Extraction**: Parses city and neighborhood from addresses
5. **Error Handling**: Comprehensive error handling and validation

### URL Structure

Fincaraiz uses path-based URLs with location as path segments:

```
/venta/apartamentos/bogota/cedritos/2-o-mas-habitaciones/2-o-mas-banos/con-ascensor/desde-300000000/hasta-500000000/m2-desde-64/m2-hasta-96/edificados/publicado-ultimos-7-dias?IDmoneda=4&stratum[]=4
```

### Parameter Mappings

| Property Schema | Fincaraiz Format | Description |
|----------------|------------------|-------------|
| `operation` | Path: `venta`/`arriendo` | ARRIENDO → arriendo, VENTA → venta |
| `address` | Path: `bogota`/`cedritos` | City and neighborhood as path segments |
| `bedrooms` | Path: `2-o-mas-habitaciones` | Bedroom filter in path |
| `bathrooms` | Path: `2-o-mas-banos` | Bathroom filter in path |
| `area_habitable` | Path: `m2-desde-64/m2-hasta-96` | Area range in path |
| `pricing.price_per_m2` | Path: `desde-300000000/hasta-500000000` | Price range in path |
| `elevator` | Path: `con-ascensor` | Amenities with "con-" prefix |
| `stratum` | Query: `stratum[]=4` | Stratum as array parameter |

### Tolerance Settings

```python
self.price_tolerance = 0.25    # ±25% price range
self.area_tolerance = 0.20     # ±20% area range
self.bedroom_tolerance = 1     # ±1 bedroom
self.bathroom_tolerance = 0.5  # ±0.5 bathroom
```

### Usage Example

```python
from src.real_estate_analytics.mappers.fincaraiz_mapper import FincaraizMapper

# Initialize mapper
mapper = FincaraizMapper()

# Property data following property_schema.json
property_data = {
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

# Generate search query
search_result = mapper.map_property_to_search(property_data)

# Access results
search_url = search_result['search_url']
search_params = search_result['search_params']
metadata = search_result['metadata']
```

### Generated Search URL Example

```
https://www.fincaraiz.com.co/arriendo/apartamentos/1-o-mas-habitaciones/1-o-mas-banos/con-ascensor-y-con-vigilancia/1-parqueaderos/De-16-a-30-anios/2do-al-5to-piso/desde-1387505/hasta-2312509/m2-desde-29/m2-hasta-44/edificados/publicado-ultimos-7-dias?IDmoneda=4&stratum[]=4
```

## Future Mappers (To Implement)

### Metrocuadrado Mapper

**Status**: 📋 To Implement

**Key Differences from Fincaraiz**:
- Parameter names: `operacion` instead of `tipo_operacion`
- URL structure: `/buscar` endpoint
- Some parameter value differences

### Ciencuadras Mapper

**Status**: 📋 To Implement

**Key Differences from Fincaraiz**:
- URL structure: `/buscar-inmuebles` endpoint
- Parameter names: Similar to Fincaraiz but with variations
- Different search parameter requirements

### Properati Mapper

**Status**: 📋 To Implement

**Key Differences from Fincaraiz**:
- English parameter names: `operation`, `bedrooms`, `bathrooms`
- URL structure: `/buscar` endpoint
- Different parameter value mappings

## Testing

### Test Structure

```
tests/unit/
├── test_fincaraiz_mapper.py      ✅ Complete
├── test_metrocuadrado_mapper.py  📋 To Implement
├── test_ciencuadras_mapper.py    📋 To Implement
└── test_properati_mapper.py      📋 To Implement
```

### Test Coverage

Each mapper should have tests for:
- **Parameter Mapping**: Verify correct parameter transformations
- **Tolerance Calculation**: Test price and area range calculations
- **Location Extraction**: Test city and neighborhood parsing
- **Error Handling**: Test with invalid or missing data
- **URL Generation**: Verify correct URL construction
- **Edge Cases**: Test with minimal data and boundary conditions

### Running Tests

```bash
# Run all mapper tests
pytest tests/unit/test_*_mapper.py

# Run specific mapper tests
pytest tests/unit/test_fincaraiz_mapper.py

# Run with coverage
pytest tests/unit/test_*_mapper.py --cov=src.real_estate_analytics.mappers
```

## Error Handling

### Common Error Scenarios

1. **Invalid Property Data**: Missing required fields
2. **Invalid Address Format**: Cannot extract city/neighborhood
3. **Invalid Price Data**: Cannot calculate price ranges
4. **Portal-Specific Errors**: Invalid parameter values for specific portal

### Error Response Format

```python
{
    'error': 'Error message describing what went wrong',
    'portal': 'portal_name',
    'timestamp': '2024-01-01T12:00:00Z',
    'original_property': {...}  # Original property data that caused error
}
```

## Configuration

### Mapper Configuration

Each mapper can be configured with:

```python
mapper = FincaraizMapper(
    price_tolerance=0.25,    # Override default price tolerance
    area_tolerance=0.20,     # Override default area tolerance
    bedroom_tolerance=1,     # Override default bedroom tolerance
    bathroom_tolerance=0.5   # Override default bathroom tolerance
)
```

### Portal-Specific Settings

```python
# Fincaraiz-specific settings
fincaraiz_config = {
    'base_url': 'https://www.fincaraiz.com.co',
    'path_structure': True,  # Uses path-based URLs
    'rate_limit_delay': 1.0,  # Seconds between requests
    'max_retries': 3
}
```

## Performance Considerations

### Optimization Strategies

1. **Parameter Caching**: Cache frequently used parameter mappings
2. **Lazy Loading**: Only load portal-specific configurations when needed
3. **Batch Processing**: Process multiple properties in batches
4. **Connection Pooling**: Reuse HTTP connections for multiple requests

### Memory Usage

- **Mapper Instances**: Lightweight, can be reused
- **Parameter Mappings**: Static dictionaries, minimal memory usage
- **Search Results**: Temporary, should be cleaned up after processing

## Future Enhancements

### Planned Features

1. **Dynamic Parameter Discovery**: Automatically detect portal parameter changes
2. **A/B Testing**: Test different parameter combinations
3. **Performance Monitoring**: Track mapper performance and success rates
4. **Configuration Management**: External configuration files for easy updates
5. **Multi-Language Support**: Support for different languages and regions

### Integration Points

1. **Web Scraping Orchestrator**: Uses mappers to generate search URLs
2. **Result Processors**: Use mapper metadata to normalize scraped results
3. **Analysis Engine**: Use mapper tolerance settings for analysis
4. **Report Generator**: Include mapper metadata in reports
