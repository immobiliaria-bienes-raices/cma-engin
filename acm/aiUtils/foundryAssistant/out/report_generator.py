"""
Report generation system for real estate market analysis.
Generates CSV and Markdown reports based on analysis results.
"""

import csv
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import pandas as pd


class ReportGenerator:
    """Generates CSV and Markdown reports for real estate analysis"""
    
    def __init__(self, output_dir: str = "aiUtils/foundryAssistant/out"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_csv_report(self, properties: List[Dict[str, Any]], 
                          analysis_results: Dict[str, Any],
                          target_property: Dict[str, Any],
                          filename: Optional[str] = None) -> str:
        """Generate CSV report in the format specified in examples/ejemplo_venta.csv"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analisis_mercado_{timestamp}.csv"
        
        filepath = self.output_dir / filename
        
        # Prepare data for CSV
        csv_data = self._prepare_csv_data(properties, analysis_results, target_property)
        
        # Write CSV file
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header rows
            writer.writerow(['', '', 'ACM-  Análisis de Mercado Comparativo', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
            writer.writerow(['', '', f'Fecha: {datetime.now().strftime("%B %d - %Y").upper()}', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
            writer.writerow(['', '', target_property['address']['street'], '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
            writer.writerow(['', '', target_property['address']['city'], '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
            writer.writerow(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
            
            # Write column headers
            writer.writerow([
                'Dirección, links', '', 'VENTA', 'Area Habitable', '', 'Terraza', 'Area Total', '', 'administracion', '', 'Alcobas', 'Baños', 'Parqueadero', 'Walking closet', 'LOFT', 'Estudio/Sala TV', 'Piso', 'Alcob. Servic', 'Depósito', 'Terraza/Balcón (Área)', 'Edad construcción', 'Interior/Exterior', 'Ascensor', 'Calidad Acabados', 'Estado, Conservación *', 'Ubicación', 'Estrato', 'observaciones', 'Medio de Contacto', 'Contacto **'
            ])
            writer.writerow([
                '', '', '', 'Area', '$por m2', 'Area', 'm2', '$ x m2', '', '$ x m2', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
            ])
            
            # Write target property (En Estudio)
            target_row = self._format_property_row(target_property, is_target=True)
            writer.writerow(target_row)
            
            # Write comparable properties (En VENTA)
            for prop in properties:
                prop_row = self._format_property_row(prop, is_target=False)
                writer.writerow(prop_row)
            
            # Write empty rows for additional properties
            for _ in range(3):
                writer.writerow(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
            
            # Write statistics summary
            stats = analysis_results.get('market_statistics', {})
            writer.writerow([
                '', '', 'vlr promedio', '', '', '', f"{stats.get('mean_price', 0):.2f}", '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
            ])
            
            # Write final summary
            analysis = analysis_results.get('property_analysis', {})
            writer.writerow([
                'Elaborado por: Real Estate Analytics System', '', f'Fecha: {datetime.now().strftime("%B %d - %Y").upper()}', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
            ])
            writer.writerow([
                '', '', f'$  PROM  FINAL SUGERIDO INCLUIDA ADMINISTRACION', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', f"{analysis.get('market_price_estimate', 0):,.0f}", ''
            ])
        
        return str(filepath)
    
    def _prepare_csv_data(self, properties: List[Dict[str, Any]], 
                         analysis_results: Dict[str, Any],
                         target_property: Dict[str, Any]) -> List[List[str]]:
        """Prepare data for CSV formatting"""
        # This method is used internally by generate_csv_report
        return []
    
    def _format_property_row(self, property_data: Dict[str, Any], is_target: bool) -> List[str]:
        """Format a single property row for CSV"""
        chars = property_data['characteristics']
        pricing = property_data['pricing']
        address = property_data['address']
        metadata = property_data.get('metadata', {})
        
        # Determine status
        status = 'En Estudio' if is_target else 'En VENTA'
        
        # Format address and URL
        address_text = f"{address['street']}, {address['neighborhood']}"
        url = metadata.get('listing_url', '')
        
        # Format pricing
        sale_price = pricing.get('sale_price', 0)
        area_habitable = chars.get('area_habitable', 0)
        price_per_m2 = pricing.get('price_per_m2', 0)
        administration = pricing.get('administration', 0)
        administration_per_m2 = pricing.get('administration_per_m2', 0)
        
        # Format characteristics
        bedrooms = chars.get('bedrooms', 0)
        bathrooms = chars.get('bathrooms', 0)
        parking = 'SI' if chars.get('parking', False) else 'NO'
        walking_closet = 'SI' if chars.get('walking_closet', False) else 'NO'
        loft = 'SI' if chars.get('loft', False) else 'NO'
        study_room = 'SI' if chars.get('study_room', False) else 'NO'
        floor = chars.get('floor', 0)
        service_room = chars.get('service_room', 0)
        deposit = chars.get('deposit', 0)
        terrace_area = chars.get('area_terrace', 0)
        construction_age = chars.get('construction_age', 0)
        interior_exterior = chars.get('interior_exterior', 'E')
        elevator = 'SI' if chars.get('elevator', False) else 'NO'
        finish_quality = chars.get('finish_quality', 3)
        conservation_state = chars.get('conservation_state', 3)
        location_quality = chars.get('location_quality', 3)
        stratum = chars.get('stratum', 3)
        
        # Contact information
        contact_info = metadata.get('contact_info', '')
        source_portal = metadata.get('source_portal', '')
        
        return [
            address_text if is_target else url,  # Dirección, links
            '',  # Empty column
            status,  # VENTA
            area_habitable,  # Area Habitable
            price_per_m2,  # $por m2
            terrace_area,  # Terraza Area
            area_habitable,  # Area Total
            price_per_m2,  # $ x m2
            administration,  # administracion
            administration_per_m2,  # $ x m2
            bedrooms,  # Alcobas
            bathrooms,  # Baños
            parking,  # Parqueadero
            walking_closet,  # Walking closet
            loft,  # LOFT
            study_room,  # Estudio/Sala TV
            floor,  # Piso
            service_room,  # Alcob. Servic
            deposit,  # Depósito
            terrace_area,  # Terraza/Balcón (Área)
            construction_age,  # Edad construcción
            interior_exterior,  # Interior/Exterior
            elevator,  # Ascensor
            finish_quality,  # Calidad Acabados
            conservation_state,  # Estado, Conservación *
            location_quality,  # Ubicación
            stratum,  # Estrato
            '',  # observaciones
            source_portal,  # Medios de Contacto
            contact_info  # Contacto **
        ]
    
    def generate_markdown_report(self, properties: List[Dict[str, Any]], 
                               analysis_results: Dict[str, Any],
                               target_property: Dict[str, Any],
                               filename: Optional[str] = None) -> str:
        """Generate comprehensive Markdown report"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analisis_mercado_{timestamp}.md"
        
        filepath = self.output_dir / filename
        
        # Generate report content
        report_content = self._generate_markdown_content(properties, analysis_results, target_property)
        
        # Write Markdown file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return str(filepath)
    
    def _generate_markdown_content(self, properties: List[Dict[str, Any]], 
                                 analysis_results: Dict[str, Any],
                                 target_property: Dict[str, Any]) -> str:
        """Generate Markdown report content"""
        
        # Header
        content = f"""# Análisis de Mercado Comparativo - Propiedad Inmobiliaria

**Fecha de Análisis:** {datetime.now().strftime("%d de %B de %Y")}  
**Dirección:** {target_property['address']['street']}, {target_property['address']['neighborhood']}, {target_property['address']['city']}

---

## Resumen Ejecutivo

"""
        
        # Executive Summary
        analysis = analysis_results.get('property_analysis', {})
        stats = analysis_results.get('market_statistics', {})
        
        content += f"""### Propiedad en Análisis
- **Precio Actual:** ${analysis.get('original_price', 0):,.0f} COP
- **Precio Estimado de Mercado:** ${analysis.get('market_price_estimate', 0):,.0f} COP
- **Diferencia de Precio:** {analysis.get('price_difference_percentage', 0):.1f}%
- **Estado:** {'Sobrevalorada' if analysis.get('is_overpriced', False) else 'Subvalorada' if analysis.get('is_underpriced', False) else 'Precio de Mercado'}
- **Nivel de Confianza:** {analysis.get('confidence_score', 0):.1%}

### Estadísticas del Mercado
- **Precio Promedio:** ${stats.get('mean_price', 0):,.0f} COP
- **Precio Mediano:** ${stats.get('median_price', 0):,.0f} COP
- **Rango de Precios:** ${stats.get('price_range', (0, 0))[0]:,.0f} - ${stats.get('price_range', (0, 0))[1]:,.0f} COP
- **Precio por m² Promedio:** ${stats.get('price_per_m2_mean', 0):,.0f} COP/m²
- **Propiedades Comparables:** {analysis.get('comparable_properties_count', 0)}

---

## Análisis Detallado

### Características de la Propiedad
"""
        
        # Property characteristics
        chars = target_property['characteristics']
        content += f"""
| Característica | Valor |
|----------------|-------|
| Tipo de Propiedad | {chars.get('property_type', 'N/A').title()} |
| Área Habitable | {chars.get('area_habitable', 0):.1f} m² |
| Área Total | {chars.get('area_total', 0):.1f} m² |
| Dormitorios | {chars.get('bedrooms', 0)} |
| Baños | {chars.get('bathrooms', 0)} |
| Piso | {chars.get('floor', 0)} |
| Estrato | {chars.get('stratum', 0)} |
| Parqueadero | {'Sí' if chars.get('parking', False) else 'No'} |
| Ascensor | {'Sí' if chars.get('elevator', False) else 'No'} |
| Edad de Construcción | {chars.get('construction_age', 0)} años |

### Análisis de Precios
"""
        
        # Price analysis
        content += f"""
- **Precio por m² Actual:** ${target_property['pricing'].get('price_per_m2', 0):,.0f} COP/m²
- **Precio por m² Promedio del Mercado:** ${stats.get('price_per_m2_mean', 0):,.0f} COP/m²
- **Administración Mensual:** ${target_property['pricing'].get('administration', 0):,.0f} COP
- **Administración por m²:** ${target_property['pricing'].get('administration_per_m2', 0):,.0f} COP/m²

### Tendencias del Mercado
- **Tendencia:** {analysis.get('market_trend', 'N/A')}
- **Volatilidad:** {'Alta' if stats.get('coefficient_of_variation', 0) > 0.2 else 'Moderada' if stats.get('coefficient_of_variation', 0) > 0.1 else 'Baja'}

---

## Propiedades Comparables

### Resumen de Propiedades Analizadas
"""
        
        # Comparable properties table
        content += """
| Portal | Dirección | Precio | Área | Precio/m² | Dormitorios | Baños | Estrato |
|--------|-----------|--------|------|-----------|-------------|-------|---------|
"""
        
        for prop in properties:
            prop_chars = prop['characteristics']
            prop_pricing = prop['pricing']
            prop_address = prop['address']
            prop_metadata = prop.get('metadata', {})
            
            content += f"| {prop_metadata.get('source_portal', 'N/A')} | {prop_address.get('street', 'N/A')} | ${prop_pricing.get('sale_price', 0):,.0f} | {prop_chars.get('area_habitable', 0):.1f} m² | ${prop_pricing.get('price_per_m2', 0):,.0f} | {prop_chars.get('bedrooms', 0)} | {prop_chars.get('bathrooms', 0)} | {prop_chars.get('stratum', 0)} |\n"
        
        # Recommendations
        content += "\n---\n\n## Recomendaciones\n\n"
        
        recommendations = analysis_results.get('recommendations', [])
        for i, rec in enumerate(recommendations, 1):
            content += f"{i}. {rec}\n"
        
        # Methodology
        content += """
---

## Metodología

### Criterios de Comparabilidad
- Tipo de propiedad idéntico
- Área habitable dentro del rango ±30%
- Número de dormitorios ±1
- Estrato socioeconómico ±1
- Misma zona geográfica

### Fuentes de Datos
- Ciencuadras (www.ciencuadras.com)
- Properati (www.properati.com.co)
- Fincaraiz (www.fincaraiz.com.co)
- Metrocuadrado (www.metrocuadrado.com)

### Métodos de Análisis
- Promedio simple de precios
- Análisis de precio por metro cuadrado
- Promedio ponderado por similitud
- Análisis estadístico de tendencias

---

## Información Legal

Este análisis es proporcionado únicamente con fines informativos y no constituye asesoría financiera o inmobiliaria profesional. Los precios y estimaciones se basan en datos de mercado disponibles en el momento del análisis y pueden variar según condiciones del mercado.

**Fecha de Generación:** {datetime.now().strftime("%d de %B de %Y a las %H:%M")}  
**Sistema:** Real Estate Analytics Platform v1.0
"""
        
        return content
    
    def generate_summary_report(self, analysis_results: Dict[str, Any],
                              target_property: Dict[str, Any],
                              filename: Optional[str] = None) -> str:
        """Generate a concise summary report"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resumen_analisis_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        # Create summary data
        summary = {
            "timestamp": datetime.now().isoformat(),
            "target_property": {
                "address": target_property['address'],
                "characteristics": target_property['characteristics'],
                "pricing": target_property['pricing']
            },
            "analysis_results": analysis_results,
            "recommendations": analysis_results.get('recommendations', [])
        }
        
        # Write JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        return str(filepath)


# Example usage
if __name__ == "__main__":
    # Sample data for testing
    sample_properties = [
        {
            "property_id": "prop_1",
            "address": {
                "street": "Calle 123 #45-67",
                "neighborhood": "Cedritos",
                "city": "Bogotá"
            },
            "characteristics": {
                "property_type": "apartment",
                "area_habitable": 80,
                "bedrooms": 3,
                "bathrooms": 2,
                "stratum": 4
            },
            "pricing": {
                "sale_price": 250000000,
                "price_per_m2": 3125000
            },
            "metadata": {
                "source_portal": "fincaraiz",
                "listing_url": "https://example.com",
                "contact_info": "123-456-7890"
            }
        }
    ]
    
    target_property = {
        "property_id": "target_1",
        "address": {
            "street": "Carrera 17 No. 134-79",
            "neighborhood": "Cedritos",
            "city": "Bogotá"
        },
        "characteristics": {
            "property_type": "apartment",
            "area_habitable": 85,
            "bedrooms": 3,
            "bathrooms": 2,
            "stratum": 4
        },
        "pricing": {
            "sale_price": 280000000,
            "price_per_m2": 3294118
        }
    }
    
    analysis_results = {
        "property_analysis": {
            "original_price": 280000000,
            "market_price_estimate": 260000000,
            "price_difference_percentage": 7.7,
            "is_overpriced": True,
            "is_underpriced": False,
            "confidence_score": 0.85,
            "comparable_properties_count": 5,
            "market_trend": "Stable"
        },
        "market_statistics": {
            "mean_price": 250000000,
            "median_price": 245000000,
            "price_range": (200000000, 300000000),
            "price_per_m2_mean": 3000000
        },
        "recommendations": [
            "Property appears overpriced by 7.7%",
            "Consider reducing price to $260,000,000 for better market positioning"
        ]
    }
    
    # Generate reports
    generator = ReportGenerator()
    
    try:
        csv_file = generator.generate_csv_report(sample_properties, analysis_results, target_property)
        print(f"CSV report generated: {csv_file}")
        
        md_file = generator.generate_markdown_report(sample_properties, analysis_results, target_property)
        print(f"Markdown report generated: {md_file}")
        
        summary_file = generator.generate_summary_report(analysis_results, target_property)
        print(f"Summary report generated: {summary_file}")
        
    except Exception as e:
        print(f"Report generation failed: {e}")
