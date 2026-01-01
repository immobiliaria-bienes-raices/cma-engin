# Quick Reference Guide

## Component Overview

| Component | Purpose | Input | Output |
|-----------|---------|-------|--------|
| **FincaraizMapper** | Generate search URLs | Property Schema | Fincaraiz Search URL |
| **FincaraizOrchestrator** | Scrape property data | Search URL | Raw CSV |
| **CSVConverter** | Standardize data | Raw CSV | Standardized CSV |

## Quick Start

### 1. Basic Usage
```python
from real_estate_analytics.mappers.fincaraiz_mapper import FincaraizMapper
from real_estate_analytics.orchestrators.fincaraiz_orchestrator import FincaraizOrchestrator
from real_estate_analytics.converters.csv_converter import CSVConverter

# Initialize components
mapper = FincaraizMapper()
orchestrator = FincaraizOrchestrator()
converter = CSVConverter()

# Complete workflow
property_data = {...}
search_url = mapper.map_property_to_search(property_data)['search_url']
orchestrator.process_search_url(search_url, "raw.csv")
converter.convert_csv_file("raw.csv", "standardized.csv")
```

### 2. Property Schema Format
```python
property_data = {
    "address": "Calle 100 #15-20, Bogotá",
    "operation": "VENTA",  # or "ARRIENDO"
    "area_habitable": 80.0,
    "bedrooms": 2,
    "bathrooms": 2.0,
    "stratum": 4,
    "elevator": True,
    "terrace": True,
    "pricing": {
        "price_per_m2": 5000000,
        "area": 80.0
    }
}
```

### 3. Generated URLs
```
https://www.fincaraiz.com.co/venta/apartamentos/bogota/2-o-mas-habitaciones/2-o-mas-banos/con-ascensor/desde-300000000/hasta-500000000/m2-desde-64/m2-hasta-96/edificados/publicado-ultimos-7-dias?IDmoneda=4&stratum[]=4
```

## Configuration

### Mapper Settings
```python
mapper = FincaraizMapper()
# Default tolerances:
# - Price: 25%
# - Area: 20%
# - Bedrooms: ±1
# - Bathrooms: ±0.5
```

### Orchestrator Settings
```python
orchestrator = FincaraizOrchestrator(
    delay_between_requests=1.0,  # seconds
    max_retries=3
)
```

### Converter Settings
```python
converter = CSVConverter()
# No configuration needed - uses intelligent field mapping
```

## Common Patterns

### 1. Batch Processing
```python
# Process multiple properties
properties = [property1, property2, property3]
for prop in properties:
    search_url = mapper.map_property_to_search(prop)['search_url']
    orchestrator.process_search_url(search_url, f"raw_{prop['address']}.csv")
```

### 2. Multiple File Conversion
```python
input_files = ["raw1.csv", "raw2.csv", "raw3.csv"]
converter.convert_multiple_files(input_files, "output_dir/")
```

### 3. Error Handling
```python
try:
    result = mapper.map_property_to_search(property_data)
    if 'error' in result:
        print(f"Error: {result['error']}")
    else:
        search_url = result['search_url']
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Output Formats

### Raw CSV (Orchestrator Output)
```csv
title,price,address,area,bedrooms,bathrooms,parking,stratum,property_type,operation,amenities,contact,property_url,images
"Apartamento en venta",$500000000,"Calle 100 #15-20",80 m²,2,2.0,1,4,Apartamento,VENTA,"Ascensor; Balcón",3001234567,https://...,https://...
```

### Standardized CSV (Converter Output)
```csv
address,operation,area_habitable,terrace,area_total,administration,bedrooms,bathrooms,parking,walking_closet,loft,study_room,floor,deposit,terrace_area,construction_age,interior_exterior,elevator,finish_quality,conservation_state,location_quality,stratum,observations,contact_method,contact_info,pricing
"Calle 100 #15-20",VENTA,80.0,True,80.0,0.0,2,2.0,1,False,False,False,0,0,0.0,0,I,True,3,3,3,4,,,,"{""area"": 80.0, ""price_per_m2"": 6250000.0, ""total_area"": 80.0, ""total_price_per_m2"": 6250000.0, ""admin_per_m2"": 0.0}"
```

## Troubleshooting

### Common Issues

1. **No properties found**
   - Check if search URL is valid
   - Verify property criteria are not too restrictive
   - Check if website structure has changed

2. **Conversion errors**
   - Verify input CSV has required columns
   - Check data format consistency
   - Review error logs for specific issues

3. **Network errors**
   - Increase delay between requests
   - Check internet connection
   - Verify website accessibility

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run your code - will show detailed logs
```

## Performance Tips

1. **Use appropriate delays** to avoid being blocked
2. **Process files in batches** for better memory management
3. **Validate data early** to catch issues quickly
4. **Monitor conversion rates** to ensure data quality

## Examples

See the `examples/` directory for complete working examples:
- `fincaraiz_workflow_example.py` - Basic workflow
- `complete_workflow_example.py` - Full end-to-end process
