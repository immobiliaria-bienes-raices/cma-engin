# Real Estate Analytics Components Documentation

## Overview

This document provides comprehensive documentation for all components in the Real Estate Analytics system, including mappers, orchestrators, and converters.

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Fincaraiz Mapper](#fincaraiz-mapper)
3. [Fincaraiz Orchestrator](#fincaraiz-orchestrator)
4. [CSV Converter](#csv-converter)
5. [Complete Workflow](#complete-workflow)
6. [API Reference](#api-reference)

## System Architecture

The system follows a modular architecture with three main components:

```
Property Schema → Mapper → Search URL → Orchestrator → Raw CSV → Converter → Standardized CSV
```

### Component Responsibilities

- **Mapper**: Converts property schema to portal-specific search URLs
- **Orchestrator**: Scrapes property data from search URLs and outputs raw CSV
- **Converter**: Transforms raw CSV data to standardized schema format

## Fincaraiz Mapper

### Purpose
Maps unified property schema data to Fincaraiz-specific search queries using path-based URLs.

### Key Features
- **Path-Based URLs**: Uses Fincaraiz's path structure for filtering
- **Location Handling**: City and neighborhood as path segments
- **Advanced Filters**: Supports amenities, parking, floor, construction age
- **Tolerance-Based Search**: Calculates search ranges with configurable tolerance
- **Exact Parameter Mapping**: Uses Fincaraiz's exact parameter names

### URL Structure
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

### Usage Example
```python
from real_estate_analytics.mappers.fincaraiz_mapper import FincaraizMapper

mapper = FincaraizMapper()
property_data = {
    "address": "Calle 100 #15-20, Bogotá",
    "operation": "VENTA",
    "area_habitable": 80.0,
    "bedrooms": 2,
    "bathrooms": 2.0,
    "stratum": 4,
    "pricing": {"price_per_m2": 5000000}
}

result = mapper.map_property_to_search(property_data)
print(result['search_url'])
```

### Configuration
- **Price Tolerance**: 25% (configurable)
- **Area Tolerance**: 20% (configurable)
- **Bedroom Tolerance**: ±1 (configurable)
- **Bathroom Tolerance**: ±0.5 (configurable)

## Fincaraiz Orchestrator

### Purpose
Scrapes property data from Fincaraiz search URLs and outputs structured CSV files.

### Key Features
- **Web Scraping**: Uses requests and BeautifulSoup for data extraction
- **Error Handling**: Comprehensive retry logic and error management
- **Rate Limiting**: Configurable delays between requests
- **Data Extraction**: Extracts property details, amenities, contact info
- **CSV Output**: Generates structured CSV files with property data

### Data Extraction Capabilities
- **Basic Info**: Title, price, address, area, bedrooms, bathrooms
- **Amenities**: Elevator, terrace, pool, gym, security, parking
- **Contact Info**: Phone numbers, email addresses
- **Images**: Property image URLs
- **Metadata**: Property URLs, operation type, stratum

### Usage Example
```python
from real_estate_analytics.orchestrators.fincaraiz_orchestrator import FincaraizOrchestrator

orchestrator = FincaraizOrchestrator(delay_between_requests=1.0, max_retries=3)
search_url = "https://www.fincaraiz.com.co/venta/apartamentos/bogota/2-o-mas-habitaciones"

result = orchestrator.process_search_url(search_url, "properties.csv")
print(f"Found {len(result['properties'])} properties")
```

### Configuration
- **Delay Between Requests**: 1.0 seconds (configurable)
- **Max Retries**: 3 attempts (configurable)
- **User Agent**: Mozilla/5.0 (Windows NT 10.0; Win64; x64)...
- **Timeout**: 30 seconds per request

### Output Format
Raw CSV with columns:
```
title, price, address, area, bedrooms, bathrooms, parking, stratum, 
property_type, operation, amenities, contact, property_url, images
```

## CSV Converter

### Purpose
Transforms raw scraped CSV data into the standardized property schema format used for analysis.

### Key Features
- **Schema Compliance**: Outputs data matching the exact property schema
- **Data Type Conversion**: Converts strings to appropriate types (int, float, bool)
- **Amenity Detection**: Intelligently extracts boolean amenities from text
- **Data Cleaning**: Handles missing values and invalid data
- **Validation**: Ensures required fields are present

### Field Mappings

| Raw Field | Standardized Field | Conversion |
|-----------|-------------------|------------|
| `title` | `address` | Use title as address if no specific address |
| `area` | `area_habitable` | Parse area string to float |
| `bedrooms` | `bedrooms` | Convert to integer |
| `bathrooms` | `bathrooms` | Convert to float |
| `amenities` | `elevator`, `terrace`, etc. | Extract boolean amenities |
| `price` | `pricing.price_per_m2` | Calculate price per m² |

### Amenity Detection
The converter intelligently detects amenities from text descriptions:

```python
amenity_keywords = {
    'terrace': ['terraza', 'balcon', 'balcón'],
    'elevator': ['ascensor', 'elevador'],
    'parking': ['parqueadero', 'garaje'],
    'pool': ['piscina'],
    'gym': ['gimnasio'],
    'security': ['vigilancia', 'seguridad']
}
```

### Usage Example
```python
from real_estate_analytics.converters.csv_converter import CSVConverter

converter = CSVConverter()
result = converter.convert_csv_file("raw_properties.csv", "standardized_properties.csv")

print(f"Converted {result['converted_properties']} properties")
print(f"Conversion rate: {result['conversion_rate']:.2%}")
```

### Output Schema
Standardized CSV with columns matching the property schema:
```
address, operation, area_habitable, terrace, area_total, administration,
bedrooms, bathrooms, parking, walking_closet, loft, study_room, floor,
deposit, terrace_area, construction_age, interior_exterior, elevator,
finish_quality, conservation_state, location_quality, stratum, observations,
contact_method, contact_info, pricing
```

## Complete Workflow

### End-to-End Process
1. **Property Schema** → **Mapper** → **Search URL**
2. **Search URL** → **Orchestrator** → **Raw CSV**
3. **Raw CSV** → **Converter** → **Standardized CSV**

### Workflow Example
```python
from real_estate_analytics.mappers.fincaraiz_mapper import FincaraizMapper
from real_estate_analytics.orchestrators.fincaraiz_orchestrator import FincaraizOrchestrator
from real_estate_analytics.converters.csv_converter import CSVConverter

# Initialize components
mapper = FincaraizMapper()
orchestrator = FincaraizOrchestrator()
converter = CSVConverter()

# 1. Generate search URL
property_data = {...}  # Your property data
search_result = mapper.map_property_to_search(property_data)
search_url = search_result['search_url']

# 2. Scrape properties
scrape_result = orchestrator.process_search_url(search_url, "raw_properties.csv")
raw_properties = scrape_result['properties']

# 3. Convert to standardized format
convert_result = converter.convert_csv_file("raw_properties.csv", "standardized_properties.csv")
standardized_properties = convert_result['converted_properties']
```

### Performance Metrics
- **URL Generation**: ~0.1 seconds per property
- **Web Scraping**: ~1-2 seconds per search URL (with rate limiting)
- **CSV Conversion**: ~0.01 seconds per property
- **Total Processing**: ~2-3 seconds per search URL

## API Reference

### FincaraizMapper

#### `__init__(self)`
Initialize the mapper with default tolerance settings.

#### `map_property_to_search(self, property_data: Dict[str, Any]) -> Dict[str, Any]`
Convert property schema to Fincaraiz search URL.

**Parameters:**
- `property_data`: Dictionary containing property information

**Returns:**
- Dictionary with `search_url` and `search_params`

### FincaraizOrchestrator

#### `__init__(self, delay_between_requests: float = 1.0, max_retries: int = 3)`
Initialize the orchestrator with configuration.

**Parameters:**
- `delay_between_requests`: Delay in seconds between requests
- `max_retries`: Maximum number of retries for failed requests

#### `process_search_url(self, search_url: str, output_filename: str = None) -> Dict[str, Any]`
Complete process: scrape search results and save to CSV.

**Parameters:**
- `search_url`: Fincaraiz search URL
- `output_filename`: Optional output CSV filename

**Returns:**
- Dictionary with processing results

### CSVConverter

#### `__init__(self)`
Initialize the converter with field mappings.

#### `convert_csv_file(self, input_file: str, output_file: str) -> Dict[str, Any]`
Convert a raw CSV file to standardized format.

**Parameters:**
- `input_file`: Path to input CSV file
- `output_file`: Path to output CSV file

**Returns:**
- Dictionary with conversion results

#### `convert_multiple_files(self, input_files: List[str], output_dir: str) -> Dict[str, Any]`
Convert multiple CSV files to standardized format.

**Parameters:**
- `input_files`: List of input CSV file paths
- `output_dir`: Directory to save output files

**Returns:**
- Dictionary with conversion results

## Testing

### Test Coverage
- **Unit Tests**: All components have comprehensive unit tests
- **Integration Tests**: End-to-end workflow testing
- **Real Data Testing**: Tests with actual Fincaraiz data
- **Error Handling**: Tests for various error conditions

### Running Tests
```bash
# Run all tests
python3 tests/unit/test_fincaraiz_mapper.py
python3 tests/unit/test_fincaraiz_orchestrator.py
python3 tests/unit/test_csv_converter.py

# Run complete workflow example
python3 examples/complete_workflow_example.py
```

### Test Results
- **Mapper Tests**: ✅ All passing
- **Orchestrator Tests**: ✅ All passing
- **Converter Tests**: ✅ All passing
- **Integration Tests**: ✅ All passing

## Error Handling

### Common Error Scenarios
1. **Invalid Property Data**: Missing required fields
2. **Network Errors**: Failed HTTP requests
3. **Parsing Errors**: Invalid data format
4. **File I/O Errors**: Missing or inaccessible files

### Error Recovery
- **Retry Logic**: Automatic retry for network errors
- **Default Values**: Graceful handling of missing data
- **Logging**: Comprehensive error logging
- **Validation**: Data validation before processing

## Performance Considerations

### Optimization Tips
1. **Rate Limiting**: Respect website rate limits
2. **Batch Processing**: Process multiple files together
3. **Memory Management**: Process large datasets in chunks
4. **Caching**: Cache frequently accessed data

### Scalability
- **Horizontal Scaling**: Multiple orchestrator instances
- **Parallel Processing**: Concurrent file processing
- **Resource Management**: Efficient memory and CPU usage

## Future Enhancements

### Planned Features
1. **Additional Portals**: Support for other real estate websites
2. **Data Validation**: Enhanced data quality checks
3. **Performance Monitoring**: Real-time performance metrics
4. **API Endpoints**: REST API for external access

### Extensibility
- **Plugin Architecture**: Easy addition of new portals
- **Custom Mappers**: User-defined mapping rules
- **Data Transformations**: Custom data processing pipelines

## Conclusion

The Real Estate Analytics system provides a complete solution for property data collection and standardization. All components are production-ready and thoroughly tested with real-world data.

For more information, see the individual component documentation and examples in the `examples/` directory.
