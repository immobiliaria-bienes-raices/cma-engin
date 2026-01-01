"""
Main workflow implementation for real estate data analytics.
Orchestrates the entire process from property input to report generation.
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging

# Import our custom modules
from portal_adapters import get_portal_adapter
from analysis_engine import RealEstateAnalyzer
from report_generator import ReportGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RealEstateWorkflow:
    """Main workflow orchestrator for real estate analytics"""
    
    def __init__(self, output_dir: str = "aiUtils/foundryAssistant/out"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.analyzer = RealEstateAnalyzer()
        self.report_generator = ReportGenerator(str(self.output_dir))
        
        # Portal configuration
        self.portals = {
            'ciencuadras': 'https://www.ciencuadras.com/',
            'properati': 'https://www.properati.com.co/',
            'fincaraiz': 'https://www.fincaraiz.com.co/',
            'metrocuadrado': 'https://www.metrocuadrado.com/'
        }
    
    async def run_analysis(self, target_property: Dict[str, Any], 
                          search_radius_km: float = 5.0,
                          max_properties_per_portal: int = 20) -> Dict[str, Any]:
        """
        Run complete real estate analysis workflow
        
        Args:
            target_property: Property data in unified JSON schema format
            search_radius_km: Search radius in kilometers
            max_properties_per_portal: Maximum properties to fetch per portal
            
        Returns:
            Dictionary containing analysis results and generated files
        """
        
        logger.info("Starting real estate analysis workflow")
        
        try:
            # Step 1: Validate input property
            self._validate_property(target_property)
            logger.info("Property validation successful")
            
            # Step 2: Generate search queries for all portals
            search_queries = self._generate_search_queries(target_property, search_radius_km)
            logger.info(f"Generated search queries for {len(search_queries)} portals")
            
            # Step 3: Scrape properties from all portals
            scraped_properties = await self._scrape_all_portals(search_queries, max_properties_per_portal)
            logger.info(f"Scraped {len(scraped_properties)} properties from portals")
            
            # Step 4: Perform market analysis
            analysis_results = await self._perform_analysis(target_property, scraped_properties)
            logger.info("Market analysis completed")
            
            # Step 5: Generate reports
            report_files = await self._generate_reports(target_property, scraped_properties, analysis_results)
            logger.info(f"Generated {len(report_files)} report files")
            
            # Step 6: Return comprehensive results
            return {
                "success": True,
                "target_property": target_property,
                "scraped_properties": scraped_properties,
                "analysis_results": analysis_results,
                "report_files": report_files,
                "summary": self._generate_summary(analysis_results)
            }
            
        except Exception as e:
            logger.error(f"Workflow failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "target_property": target_property
            }
    
    def _validate_property(self, property_data: Dict[str, Any]) -> None:
        """Validate property data against schema"""
        required_fields = ['property_id', 'address', 'characteristics', 'pricing']
        
        for field in required_fields:
            if field not in property_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate address
        address = property_data['address']
        if not address.get('street') or not address.get('city'):
            raise ValueError("Address must include street and city")
        
        # Validate characteristics
        chars = property_data['characteristics']
        if not chars.get('property_type') or not chars.get('area_habitable'):
            raise ValueError("Characteristics must include property_type and area_habitable")
        
        # Validate pricing
        pricing = property_data['pricing']
        if not pricing.get('sale_price') or pricing['sale_price'] <= 0:
            raise ValueError("Pricing must include valid sale_price")
    
    def _generate_search_queries(self, target_property: Dict[str, Any], 
                                search_radius_km: float) -> Dict[str, Dict[str, Any]]:
        """Generate search queries for all portals"""
        address = target_property['address']
        chars = target_property['characteristics']
        pricing = target_property['pricing']
        
        # Calculate price range (±30%)
        base_price = pricing['sale_price']
        min_price = int(base_price * 0.7)
        max_price = int(base_price * 1.3)
        
        # Calculate area range (±30%)
        base_area = chars['area_habitable']
        min_area = int(base_area * 0.7)
        max_area = int(base_area * 1.3)
        
        queries = {}
        
        for portal_name, portal_url in self.portals.items():
            queries[portal_name] = {
                'url': portal_url,
                'search_params': {
                    'location': f"{address['neighborhood']}, {address['city']}",
                    'property_type': chars['property_type'],
                    'sale_type': chars['sale_type'],
                    'min_price': min_price,
                    'max_price': max_price,
                    'min_area': min_area,
                    'max_area': max_area,
                    'bedrooms': chars.get('bedrooms', 0),
                    'stratum': chars.get('stratum', 3)
                }
            }
        
        return queries
    
    async def _scrape_all_portals(self, search_queries: Dict[str, Dict[str, Any]], 
                                 max_properties: int) -> List[Dict[str, Any]]:
        """Scrape properties from all portals using Bright Data MCP"""
        all_properties = []
        
        # This would integrate with Bright Data MCP servers
        # For now, we'll simulate the scraping process
        
        for portal_name, query in search_queries.items():
            try:
                logger.info(f"Scraping {portal_name}...")
                
                # Simulate scraping delay
                await asyncio.sleep(1)
                
                # In real implementation, this would use Bright Data MCP:
                # properties = await self._scrape_portal_with_brightdata(portal_name, query)
                
                # For demo purposes, generate sample properties
                sample_properties = self._generate_sample_properties(portal_name, query, max_properties)
                all_properties.extend(sample_properties)
                
                logger.info(f"Scraped {len(sample_properties)} properties from {portal_name}")
                
            except Exception as e:
                logger.error(f"Failed to scrape {portal_name}: {str(e)}")
                continue
        
        return all_properties
    
    def _generate_sample_properties(self, portal_name: str, query: Dict[str, Any], 
                                   count: int) -> List[Dict[str, Any]]:
        """Generate sample properties for demonstration"""
        import random
        
        base_price = query['search_params']['min_price']
        price_range = query['search_params']['max_price'] - base_price
        base_area = query['search_params']['min_area']
        area_range = query['search_params']['max_area'] - base_area
        
        properties = []
        
        for i in range(min(count, 5)):  # Generate up to 5 sample properties
            price = base_price + random.randint(0, price_range)
            area = base_area + random.randint(0, area_range)
            
            property_data = {
                "property_id": f"{portal_name}_sample_{i+1}",
                "address": {
                    "street": f"Calle {random.randint(1, 200)} #{random.randint(1, 200)}-{random.randint(1, 200)}",
                    "neighborhood": query['search_params']['location'].split(',')[0],
                    "city": query['search_params']['location'].split(',')[1].strip()
                },
                "characteristics": {
                    "property_type": query['search_params']['property_type'],
                    "sale_type": query['search_params']['sale_type'],
                    "area_habitable": area,
                    "area_total": area + random.randint(0, 20),
                    "bedrooms": query['search_params']['bedrooms'] + random.randint(-1, 1),
                    "bathrooms": 2 + random.randint(-1, 1),
                    "stratum": query['search_params']['stratum'] + random.randint(-1, 1),
                    "parking": random.choice([True, False]),
                    "elevator": random.choice([True, False]),
                    "floor": random.randint(1, 10),
                    "construction_age": random.randint(0, 30)
                },
                "pricing": {
                    "sale_price": price,
                    "price_per_m2": price / area if area > 0 else 0,
                    "administration": random.randint(100000, 500000)
                },
                "metadata": {
                    "source_portal": portal_name,
                    "listing_url": f"https://{portal_name}.com/property/{i+1}",
                    "contact_info": f"Contact-{i+1}",
                    "scraping_timestamp": "2025-01-27T10:00:00Z"
                }
            }
            
            properties.append(property_data)
        
        return properties
    
    async def _perform_analysis(self, target_property: Dict[str, Any], 
                               scraped_properties: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform market analysis using the analysis engine"""
        
        # Add properties to analyzer
        self.analyzer.add_properties(scraped_properties)
        self.analyzer.set_target_property(target_property)
        
        # Run analysis
        analysis_results = self.analyzer.analyze_market()
        
        # Get market summary
        market_summary = self.analyzer.get_market_summary()
        
        return market_summary
    
    async def _generate_reports(self, target_property: Dict[str, Any], 
                               scraped_properties: List[Dict[str, Any]], 
                               analysis_results: Dict[str, Any]) -> Dict[str, str]:
        """Generate all report files"""
        
        report_files = {}
        
        try:
            # Generate CSV report
            csv_file = self.report_generator.generate_csv_report(
                scraped_properties, analysis_results, target_property
            )
            report_files['csv'] = csv_file
            
            # Generate Markdown report
            md_file = self.report_generator.generate_markdown_report(
                scraped_properties, analysis_results, target_property
            )
            report_files['markdown'] = md_file
            
            # Generate JSON summary
            json_file = self.report_generator.generate_summary_report(
                analysis_results, target_property
            )
            report_files['json'] = json_file
            
        except Exception as e:
            logger.error(f"Report generation failed: {str(e)}")
            raise
        
        return report_files
    
    def _generate_summary(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate workflow summary"""
        analysis = analysis_results.get('property_analysis', {})
        
        return {
            "total_properties_analyzed": analysis.get('comparable_properties_count', 0),
            "market_price_estimate": analysis.get('market_price_estimate', 0),
            "price_difference_percentage": analysis.get('price_difference_percentage', 0),
            "is_overpriced": analysis.get('is_overpriced', False),
            "is_underpriced": analysis.get('is_underpriced', False),
            "confidence_score": analysis.get('confidence_score', 0),
            "market_trend": analysis.get('market_trend', 'Unknown'),
            "recommendations_count": len(analysis_results.get('recommendations', []))
        }


# Example usage and CLI interface
async def main():
    """Main function for testing the workflow"""
    
    # Sample target property
    target_property = {
        "property_id": "target_cedritos_001",
        "address": {
            "street": "Carrera 17 No. 134-79",
            "neighborhood": "Cedritos",
            "city": "Bogotá",
            "coordinates": {
                "lat": 4.7110,
                "lng": -74.0721
            }
        },
        "characteristics": {
            "property_type": "apartment",
            "sale_type": "sale",
            "area_habitable": 85.0,
            "area_total": 85.0,
            "area_terrace": 0.0,
            "bedrooms": 3,
            "bathrooms": 2.0,
            "parking": True,
            "walking_closet": False,
            "loft": False,
            "study_room": False,
            "floor": 4,
            "service_room": 1,
            "deposit": 0.0,
            "construction_age": 15,
            "interior_exterior": "exterior",
            "elevator": True,
            "finish_quality": 4,
            "conservation_state": 4,
            "stratum": 4,
            "location_quality": 4
        },
        "pricing": {
            "sale_price": 280000000,
            "price_per_m2": 3294118,
            "administration": 350000,
            "administration_per_m2": 4118
        },
        "metadata": {
            "source_portal": "manual_input",
            "listing_url": "",
            "contact_info": "Propietario",
            "listing_date": "2025-01-27T00:00:00Z"
        }
    }
    
    # Initialize workflow
    workflow = RealEstateWorkflow()
    
    # Run analysis
    print("Starting real estate analysis workflow...")
    results = await workflow.run_analysis(
        target_property=target_property,
        search_radius_km=5.0,
        max_properties_per_portal=10
    )
    
    # Display results
    if results['success']:
        print("\n✅ Analysis completed successfully!")
        print(f"📊 Properties analyzed: {results['summary']['total_properties_analyzed']}")
        print(f"💰 Market price estimate: ${results['summary']['market_price_estimate']:,.0f}")
        print(f"📈 Price difference: {results['summary']['price_difference_percentage']:.1f}%")
        print(f"🎯 Confidence score: {results['summary']['confidence_score']:.1%}")
        print(f"📁 Reports generated: {len(results['report_files'])}")
        
        for report_type, file_path in results['report_files'].items():
            print(f"   - {report_type.upper()}: {file_path}")
    else:
        print(f"❌ Analysis failed: {results['error']}")


if __name__ == "__main__":
    # Run the workflow
    asyncio.run(main())
