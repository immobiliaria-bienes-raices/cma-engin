# ACM System Architecture - Property to Portal Mapping

## System Overview

The ACM (Analisis Comparativo de Mercado) system transforms property data from a unified schema into portal-specific search queries for Colombian real estate websites.

## Architecture Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           ACM SYSTEM ARCHITECTURE                              │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────────────────┐
│   INPUT LAYER   │    │  MAPPING LAYER   │    │      OUTPUT LAYER               │
│                 │    │                  │    │                                 │
│ Property Schema │───▶│ Portal Mappers   │───▶│ Portal-Specific Search Queries │
│ (Unified JSON)  │    │                  │    │                                 │
└─────────────────┘    └──────────────────┘    └─────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────────────────┐
                    │     Web Scraping Layer      │
                    │                             │
                    │  ┌─────────┐ ┌─────────┐   │
                    │  │Fincaraiz│ │Metrocuad│   │
                    │  │ Mapper  │ │ Mapper  │   │
                    │  └─────────┘ └─────────┘   │
                    │                             │
                    │  ┌─────────┐ ┌─────────┐   │
                    │  │Ciencuadr│ │Properati│   │
                    │  │ Mapper  │ │ Mapper  │   │
                    │  └─────────┘ └─────────┘   │
                    └─────────────────────────────┘
```

## Detailed Component Flow

### 1. Input: Property Schema (property_schema.json)

```json
{
  "address": "CALLE 145 #23-06 Edf Genesis Cedritos",
  "operation": "ARRIENDO",
  "area_habitable": 37.42,
  "bedrooms": 1,
  "bathrooms": 1.0,
  "parking": 1,
  "stratum": 4,
  "construction_age": 29,
  "elevator": true,
  "floor": 4,
  "pricing": {
    "price_per_m2": 49439,
    "area": 37.42
  }
}
```

### 2. Mapping Layer: Portal Mappers

Each mapper transforms the unified schema into portal-specific parameters:

#### Fincaraiz Mapper (Implemented)
- **Input**: Property schema JSON
- **Output**: Fincaraiz search URL with parameters
- **Key Transformations**:
  - `operation: "ARRIENDO"` → `tipo_operacion: "arriendo"`
  - `area_habitable: 37.42` → `area_min: 29, area_max: 44` (with tolerance)
  - `price_per_m2: 49439` → `precio_min: 1387505, precio_max: 2312509` (with tolerance)
  - `bedrooms: 1` → `alcobas_min: 1, alcobas_max: 2` (with tolerance)

#### Example Fincaraiz Output:
```
https://www.fincaraiz.com.co/buscar?tipo_operacion=arriendo&tipo_inmueble=apartamento&precio_min=1387505&precio_max=2312509&area_min=29&area_max=44&alcobas_min=1&alcobas_max=2&banos_min=1&banos_max=1.5&parqueadero=si&estrato=4&antiguedad=usado&ascensor=si&piso=4
```

### 3. Portal-Specific Mappers (To Be Implemented)

#### Metrocuadrado Mapper
- **Parameter Mapping**:
  - `operation` → `operacion`
  - `bedrooms` → `alcobas`
  - `bathrooms` → `banos`
  - `stratum` → `estrato`

#### Ciencuadras Mapper
- **Parameter Mapping**:
  - `operation` → `tipo_operacion`
  - `bedrooms` → `alcobas`
  - `bathrooms` → `banos`
  - `stratum` → `estrato`

#### Properati Mapper
- **Parameter Mapping**:
  - `operation` → `operation`
  - `bedrooms` → `bedrooms`
  - `bathrooms` → `bathrooms`
  - `stratum` → `stratum`

## Implementation Status

### ✅ Completed
- **Fincaraiz Mapper**: Fully implemented with comprehensive parameter mapping
- **Test Suite**: Complete test coverage for Fincaraiz mapper
- **Tolerance Logic**: Smart price and area range calculations
- **Location Extraction**: City and neighborhood parsing from addresses

### 🔄 In Progress
- **Package Structure**: Organized Python package following best practices
- **Base Mapper Class**: Abstract base class for all mappers

### 📋 To Do
- **Metrocuadrado Mapper**: Portal-specific parameter mapping
- **Ciencuadras Mapper**: Portal-specific parameter mapping
- **Properati Mapper**: Portal-specific parameter mapping
- **Web Scraping Orchestrator**: Coordinate all mappers
- **Results Processor**: Normalize scraped data back to unified schema

## Key Features

### 1. Smart Tolerance Calculation
- **Price Tolerance**: ±25% around target price
- **Area Tolerance**: ±20% around target area
- **Bedroom Tolerance**: ±1 bedroom
- **Bathroom Tolerance**: ±0.5 bathroom

### 2. Location Intelligence
- **City Extraction**: Parses city from address strings
- **Neighborhood Detection**: Identifies neighborhood indicators
- **Geographic Mapping**: Maps to portal-specific location codes

### 3. Parameter Normalization
- **Operation Types**: Maps ARRIENDO/VENTA to portal-specific values
- **Property Types**: Maps apartment/house to portal-specific categories
- **Quality Ratings**: Maps 1-5 scales to portal-specific values

## Usage Example

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

# Access search URL
search_url = search_result['search_url']
print(f"Fincaraiz Search URL: {search_url}")
```

## Next Steps

1. **Implement remaining mappers** for Metrocuadrado, Ciencuadras, and Properati
2. **Create web scraping orchestrator** that uses all mappers
3. **Build results processor** that normalizes scraped data
4. **Add comprehensive error handling** and logging
5. **Create CLI interface** for easy usage

## File Structure

```
src/real_estate_analytics/
├── __init__.py
├── mappers/
│   ├── __init__.py
│   ├── fincaraiz_mapper.py      ✅ Implemented
│   ├── metrocuadrado_mapper.py  📋 To Do
│   ├── ciencuadras_mapper.py    📋 To Do
│   └── properati_mapper.py      📋 To Do
├── adapters/
│   ├── __init__.py
│   └── base_adapter.py
├── analysis/
│   ├── __init__.py
│   └── property_analyzer.py
├── reports/
│   ├── __init__.py
│   └── report_generator.py
└── utils/
    ├── __init__.py
    └── property_schema.json
```
