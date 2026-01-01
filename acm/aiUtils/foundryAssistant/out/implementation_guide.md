# Real Estate Analytics Implementation Guide

## Overview
This guide provides step-by-step instructions for implementing and using the real estate data analytics workflow using MCP scraping servers.

## System Architecture

### Components
1. **Property Schema** (`property_schema.json`) - Unified data structure
2. **Portal Adapters** (`portal_adapters.py`) - Data extraction from each portal
3. **Scraping Strategy** (`scraping_strategy.md`) - Bright Data MCP integration
4. **Analysis Engine** (`analysis_engine.py`) - Statistical analysis and comparison
5. **Report Generator** (`report_generator.py`) - CSV and Markdown output
6. **Main Workflow** (`main_workflow.py`) - Orchestrates entire process

## Installation and Setup

### Prerequisites
```bash
# Python 3.8+ required
python --version

# Install required packages
pip install beautifulsoup4 pandas asyncio requests
```

### MCP Server Setup
1. **Bright Data MCP Server** - For web scraping
2. **Google Maps API** - For geocoding and neighborhood analysis

### Directory Structure
```
aiUtils/foundryAssistant/out/
├── property_schema.json
├── portal_adapters.py
├── analysis_engine.py
├── report_generator.py
├── main_workflow.py
├── real_estate_analytics_workflow.md
├── scraping_strategy.md
└── implementation_guide.md
```

## Usage Examples

### Basic Usage
```python
import asyncio
from main_workflow import RealEstateWorkflow

# Define target property
target_property = {
    "property_id": "target_001",
    "address": {
        "street": "Carrera 17 No. 134-79",
        "neighborhood": "Cedritos",
        "city": "Bogotá"
    },
    "characteristics": {
        "property_type": "apartment",
        "sale_type": "sale",
        "area_habitable": 85.0,
        "bedrooms": 3,
        "bathrooms": 2.0,
        "stratum": 4
    },
    "pricing": {
        "sale_price": 280000000,
        "price_per_m2": 3294118
    }
}

# Run analysis
async def run_analysis():
    workflow = RealEstateWorkflow()
    results = await workflow.run_analysis(target_property)
    return results

# Execute
results = asyncio.run(run_analysis())
```

### Advanced Configuration
```python
# Custom search parameters
results = await workflow.run_analysis(
    target_property=target_property,
    search_radius_km=10.0,  # 10km search radius
    max_properties_per_portal=25  # Max 25 properties per portal
)
```

## Portal Integration

### Supported Portals
1. **Ciencuadras** - https://www.ciencuadras.com/
2. **Properati** - https://www.properati.com.co/
3. **Fincaraiz** - https://www.fincaraiz.com.co/
4. **Metrocuadrado** - https://www.metrocuadrado.com/

### Adding New Portals
1. Create new adapter class inheriting from `BasePortalAdapter`
2. Implement `_extract_raw_data()` method
3. Add portal to `get_portal_adapter()` factory function
4. Update portal configuration in `main_workflow.py`

### Example: Adding New Portal
```python
class NewPortalAdapter(BasePortalAdapter):
    def __init__(self):
        super().__init__("new_portal")
    
    def _extract_raw_data(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        # Implement extraction logic
        return raw_data
```

## Bright Data MCP Integration

### Configuration
```python
# Bright Data MCP configuration
brightdata_config = {
    "concurrent_requests": 4,
    "request_delay": 1000,  # 1 second
    "retry_attempts": 3,
    "timeout": 30000,  # 30 seconds
    "user_agent": "RealEstateAnalytics/1.0"
}
```

### Portal-Specific Settings
```python
portal_configs = {
    "ciencuadras": {
        "requires_javascript": True,
        "wait_for_element": ".property-card",
        "rate_limit": 2000  # 2 seconds between requests
    },
    "properati": {
        "requires_javascript": False,
        "wait_for_element": ".posting-card",
        "rate_limit": 1500
    }
}
```

## Analysis Features

### Statistical Analysis
- Mean, median, mode calculations
- Standard deviation and variance
- Price range and quartiles
- Coefficient of variation
- Price per m² analysis

### Property Comparison
- Similarity scoring based on characteristics
- Weighted price estimation
- Confidence scoring
- Market trend analysis

### Recommendations
- Overpriced/underpriced detection
- Price adjustment suggestions
- Market positioning advice
- Confidence level indicators

## Output Formats

### CSV Report
- Follows format from `examples/ejemplo_venta.csv`
- Includes all comparable properties
- Statistical summary rows
- Price analysis and recommendations

### Markdown Report
- Executive summary
- Detailed property analysis
- Market statistics
- Recommendations
- Methodology explanation

### JSON Summary
- Machine-readable format
- Complete analysis results
- Metadata and timestamps
- API-friendly structure

## Error Handling

### Common Issues
1. **Portal Access Denied** - Implement retry with delays
2. **Data Parsing Errors** - Validate data quality
3. **Rate Limiting** - Respect portal limits
4. **Network Timeouts** - Implement retry logic

### Best Practices
```python
# Implement retry mechanism
async def scrape_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await scrape_url(url)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

## Performance Optimization

### Parallel Processing
```python
# Process multiple portals simultaneously
async def scrape_all_portals(queries):
    tasks = [scrape_portal(portal, query) for portal, query in queries.items()]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

### Caching
```python
# Implement property caching
class PropertyCache:
    def __init__(self, ttl=3600):  # 1 hour TTL
        self.cache = {}
        self.ttl = ttl
```

## Testing

### Unit Tests
```python
import unittest
from analysis_engine import RealEstateAnalyzer

class TestAnalysisEngine(unittest.TestCase):
    def setUp(self):
        self.analyzer = RealEstateAnalyzer()
    
    def test_property_comparison(self):
        # Test property comparison logic
        pass
```

### Integration Tests
```python
# Test complete workflow
async def test_workflow():
    workflow = RealEstateWorkflow()
    results = await workflow.run_analysis(sample_property)
    assert results['success'] == True
```

## Deployment

### Docker Configuration
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main_workflow.py"]
```

### Environment Variables
```bash
# Required environment variables
BRIGHTDATA_API_KEY=your_api_key
GOOGLE_MAPS_API_KEY=your_google_maps_key
OUTPUT_DIR=/app/output
LOG_LEVEL=INFO
```

## Monitoring and Logging

### Logging Configuration
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('real_estate_analytics.log'),
        logging.StreamHandler()
    ]
)
```

### Metrics Collection
```python
class WorkflowMetrics:
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.properties_found = 0
        self.analysis_time = 0
```

## Legal and Compliance

### Data Usage
- Respect robots.txt files
- Implement reasonable delays
- Use proper User-Agent headers
- Follow terms of service

### Privacy
- Anonymize personal data
- Implement data retention policies
- Provide opt-out mechanisms
- Comply with data protection laws

## Troubleshooting

### Common Problems

1. **No Properties Found**
   - Check search parameters
   - Verify portal accessibility
   - Adjust search radius

2. **Low Confidence Scores**
   - Increase comparable properties
   - Refine search criteria
   - Check data quality

3. **Scraping Failures**
   - Check network connectivity
   - Verify portal selectors
   - Implement retry logic

### Debug Mode
```python
# Enable debug logging
logging.getLogger().setLevel(logging.DEBUG)

# Add debug information
debug_info = {
    "search_queries": queries,
    "scraped_properties": properties,
    "analysis_steps": analysis_steps
}
```

## Future Enhancements

### Planned Features
1. Machine learning price prediction
2. Real-time market monitoring
3. Investment analysis tools
4. Mobile application
5. API endpoints

### Integration Opportunities
1. CRM systems
2. Property management software
3. Financial analysis tools
4. Market research platforms

## Support and Maintenance

### Regular Updates
- Portal selector updates
- Schema versioning
- Performance optimizations
- Security patches

### Monitoring
- Portal availability
- Data quality metrics
- Performance benchmarks
- Error rates

## Conclusion

This implementation provides a comprehensive solution for real estate market analysis using MCP scraping servers. The modular design allows for easy extension and customization while maintaining high performance and reliability.

For questions or support, refer to the documentation or contact the development team.
