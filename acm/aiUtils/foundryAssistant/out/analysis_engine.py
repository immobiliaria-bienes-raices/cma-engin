"""
Statistical analysis and pricing comparison engine for real estate properties.
Performs comprehensive market analysis and generates insights.
"""

import statistics
import math
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class PropertyAnalysis:
    """Container for property analysis results"""
    property_id: str
    original_price: float
    market_price_estimate: float
    price_difference: float
    price_difference_percentage: float
    is_overpriced: bool
    is_underpriced: bool
    confidence_score: float
    comparable_properties_count: int
    market_trend: str
    recommendations: List[str]


@dataclass
class MarketStatistics:
    """Container for market statistics"""
    mean_price: float
    median_price: float
    mode_price: float
    standard_deviation: float
    variance: float
    price_range: Tuple[float, float]
    quartiles: Tuple[float, float, float]
    coefficient_of_variation: float
    price_per_m2_mean: float
    price_per_m2_median: float
    price_per_m2_std: float


class RealEstateAnalyzer:
    """Main analysis engine for real estate market comparison"""
    
    def __init__(self):
        self.properties: List[Dict[str, Any]] = []
        self.target_property: Optional[Dict[str, Any]] = None
        self.analysis_results: Optional[PropertyAnalysis] = None
        self.market_stats: Optional[MarketStatistics] = None
    
    def add_properties(self, properties: List[Dict[str, Any]]):
        """Add properties for analysis"""
        self.properties.extend(properties)
    
    def set_target_property(self, property_data: Dict[str, Any]):
        """Set the target property for analysis"""
        self.target_property = property_data
    
    def analyze_market(self) -> PropertyAnalysis:
        """Perform comprehensive market analysis"""
        if not self.target_property:
            raise ValueError("Target property not set")
        
        if not self.properties:
            raise ValueError("No properties available for comparison")
        
        # Filter comparable properties
        comparable_properties = self._filter_comparable_properties()
        
        if not comparable_properties:
            raise ValueError("No comparable properties found")
        
        # Calculate market statistics
        self.market_stats = self._calculate_market_statistics(comparable_properties)
        
        # Analyze target property
        self.analysis_results = self._analyze_target_property(comparable_properties)
        
        return self.analysis_results
    
    def _filter_comparable_properties(self) -> List[Dict[str, Any]]:
        """Filter properties that are comparable to the target property"""
        if not self.target_property:
            return []
        
        target_chars = self.target_property['characteristics']
        comparable = []
        
        for prop in self.properties:
            if self._is_comparable(prop, target_chars):
                comparable.append(prop)
        
        return comparable
    
    def _is_comparable(self, property_data: Dict[str, Any], target_chars: Dict[str, Any]) -> bool:
        """Determine if a property is comparable to the target"""
        prop_chars = property_data['characteristics']
        
        # Property type must match
        if prop_chars.get('property_type') != target_chars.get('property_type'):
            return False
        
        # Sale type must match
        if prop_chars.get('sale_type') != target_chars.get('sale_type'):
            return False
        
        # Area within reasonable range (±30%)
        target_area = target_chars.get('area_habitable', 0)
        prop_area = prop_chars.get('area_habitable', 0)
        
        if target_area > 0 and prop_area > 0:
            area_ratio = prop_area / target_area
            if area_ratio < 0.7 or area_ratio > 1.3:
                return False
        
        # Bedrooms within ±1
        target_bedrooms = target_chars.get('bedrooms', 0)
        prop_bedrooms = prop_chars.get('bedrooms', 0)
        
        if abs(target_bedrooms - prop_bedrooms) > 1:
            return False
        
        # Stratum within ±1
        target_stratum = target_chars.get('stratum', 3)
        prop_stratum = prop_chars.get('stratum', 3)
        
        if abs(target_stratum - prop_stratum) > 1:
            return False
        
        return True
    
    def _calculate_market_statistics(self, properties: List[Dict[str, Any]]) -> MarketStatistics:
        """Calculate comprehensive market statistics"""
        prices = [prop['pricing']['sale_price'] for prop in properties]
        prices_per_m2 = [prop['pricing']['price_per_m2'] for prop in properties]
        
        # Basic statistics
        mean_price = statistics.mean(prices)
        median_price = statistics.median(prices)
        mode_price = statistics.mode(prices) if len(set(prices)) < len(prices) else mean_price
        std_price = statistics.stdev(prices) if len(prices) > 1 else 0
        variance = statistics.variance(prices) if len(prices) > 1 else 0
        
        # Range and quartiles
        sorted_prices = sorted(prices)
        price_range = (min(prices), max(prices))
        quartiles = (
            sorted_prices[len(sorted_prices) // 4],
            sorted_prices[len(sorted_prices) // 2],
            sorted_prices[3 * len(sorted_prices) // 4]
        )
        
        # Coefficient of variation
        cv = (std_price / mean_price) * 100 if mean_price > 0 else 0
        
        # Price per m² statistics
        mean_price_per_m2 = statistics.mean(prices_per_m2)
        median_price_per_m2 = statistics.median(prices_per_m2)
        std_price_per_m2 = statistics.stdev(prices_per_m2) if len(prices_per_m2) > 1 else 0
        
        return MarketStatistics(
            mean_price=mean_price,
            median_price=median_price,
            mode_price=mode_price,
            standard_deviation=std_price,
            variance=variance,
            price_range=price_range,
            quartiles=quartiles,
            coefficient_of_variation=cv,
            price_per_m2_mean=mean_price_per_m2,
            price_per_m2_median=median_price_per_m2,
            price_per_m2_std=std_price_per_m2
        )
    
    def _analyze_target_property(self, comparable_properties: List[Dict[str, Any]]) -> PropertyAnalysis:
        """Analyze the target property against comparable properties"""
        target_price = self.target_property['pricing']['sale_price']
        target_chars = self.target_property['characteristics']
        
        # Calculate market price estimate using multiple methods
        market_estimate = self._calculate_market_price_estimate(comparable_properties, target_chars)
        
        # Calculate price difference
        price_difference = target_price - market_estimate
        price_difference_percentage = (price_difference / market_estimate) * 100 if market_estimate > 0 else 0
        
        # Determine if overpriced/underpriced
        is_overpriced = price_difference_percentage > 10  # More than 10% above market
        is_underpriced = price_difference_percentage < -10  # More than 10% below market
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(comparable_properties, target_chars)
        
        # Determine market trend
        market_trend = self._determine_market_trend(comparable_properties)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            target_price, market_estimate, price_difference_percentage, 
            is_overpriced, is_underpriced, confidence_score
        )
        
        return PropertyAnalysis(
            property_id=self.target_property['property_id'],
            original_price=target_price,
            market_price_estimate=market_estimate,
            price_difference=price_difference,
            price_difference_percentage=price_difference_percentage,
            is_overpriced=is_overpriced,
            is_underpriced=is_underpriced,
            confidence_score=confidence_score,
            comparable_properties_count=len(comparable_properties),
            market_trend=market_trend,
            recommendations=recommendations
        )
    
    def _calculate_market_price_estimate(self, comparable_properties: List[Dict[str, Any]], target_chars: Dict[str, Any]) -> float:
        """Calculate market price estimate using multiple methods"""
        # Method 1: Simple average
        prices = [prop['pricing']['sale_price'] for prop in comparable_properties]
        simple_average = statistics.mean(prices)
        
        # Method 2: Price per m² method
        target_area = target_chars.get('area_habitable', 0)
        if target_area > 0:
            prices_per_m2 = [prop['pricing']['price_per_m2'] for prop in comparable_properties]
            avg_price_per_m2 = statistics.mean(prices_per_m2)
            price_per_m2_estimate = avg_price_per_m2 * target_area
        else:
            price_per_m2_estimate = simple_average
        
        # Method 3: Weighted average by similarity
        weighted_estimate = self._calculate_weighted_estimate(comparable_properties, target_chars)
        
        # Combine methods (weighted average)
        market_estimate = (simple_average * 0.4 + price_per_m2_estimate * 0.4 + weighted_estimate * 0.2)
        
        return market_estimate
    
    def _calculate_weighted_estimate(self, comparable_properties: List[Dict[str, Any]], target_chars: Dict[str, Any]) -> float:
        """Calculate weighted price estimate based on property similarity"""
        total_weight = 0
        weighted_sum = 0
        
        for prop in comparable_properties:
            weight = self._calculate_similarity_weight(prop, target_chars)
            total_weight += weight
            weighted_sum += prop['pricing']['sale_price'] * weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0
    
    def _calculate_similarity_weight(self, property_data: Dict[str, Any], target_chars: Dict[str, Any]) -> float:
        """Calculate similarity weight between properties"""
        prop_chars = property_data['characteristics']
        weight = 1.0
        
        # Area similarity (most important)
        target_area = target_chars.get('area_habitable', 0)
        prop_area = prop_chars.get('area_habitable', 0)
        if target_area > 0 and prop_area > 0:
            area_ratio = min(target_area, prop_area) / max(target_area, prop_area)
            weight *= area_ratio
        
        # Bedrooms similarity
        target_bedrooms = target_chars.get('bedrooms', 0)
        prop_bedrooms = prop_chars.get('bedrooms', 0)
        bedroom_diff = abs(target_bedrooms - prop_bedrooms)
        weight *= max(0.5, 1.0 - (bedroom_diff * 0.2))
        
        # Stratum similarity
        target_stratum = target_chars.get('stratum', 3)
        prop_stratum = prop_chars.get('stratum', 3)
        stratum_diff = abs(target_stratum - prop_stratum)
        weight *= max(0.7, 1.0 - (stratum_diff * 0.15))
        
        # Floor similarity
        target_floor = target_chars.get('floor', 0)
        prop_floor = prop_chars.get('floor', 0)
        if target_floor > 0 and prop_floor > 0:
            floor_diff = abs(target_floor - prop_floor)
            weight *= max(0.8, 1.0 - (floor_diff * 0.1))
        
        return weight
    
    def _calculate_confidence_score(self, comparable_properties: List[Dict[str, Any]], target_chars: Dict[str, Any]) -> float:
        """Calculate confidence score for the analysis"""
        # Base confidence on number of comparable properties
        base_confidence = min(1.0, len(comparable_properties) / 10.0)
        
        # Adjust based on price consistency
        prices = [prop['pricing']['sale_price'] for prop in comparable_properties]
        if len(prices) > 1:
            cv = statistics.stdev(prices) / statistics.mean(prices)
            consistency_factor = max(0.5, 1.0 - cv)
        else:
            consistency_factor = 0.5
        
        # Adjust based on area similarity
        target_area = target_chars.get('area_habitable', 0)
        if target_area > 0:
            area_diffs = []
            for prop in comparable_properties:
                prop_area = prop['characteristics'].get('area_habitable', 0)
                if prop_area > 0:
                    area_diff = abs(target_area - prop_area) / target_area
                    area_diffs.append(area_diff)
            
            if area_diffs:
                avg_area_diff = statistics.mean(area_diffs)
                area_factor = max(0.5, 1.0 - avg_area_diff)
            else:
                area_factor = 0.5
        else:
            area_factor = 0.5
        
        confidence = base_confidence * consistency_factor * area_factor
        return min(1.0, max(0.0, confidence))
    
    def _determine_market_trend(self, comparable_properties: List[Dict[str, Any]]) -> str:
        """Determine market trend based on comparable properties"""
        if len(comparable_properties) < 3:
            return "Insufficient data"
        
        # Sort by listing date if available
        properties_with_dates = [p for p in comparable_properties if 'metadata' in p and 'listing_date' in p['metadata']]
        
        if len(properties_with_dates) < 3:
            return "Stable"
        
        # Simple trend analysis based on price distribution
        prices = [prop['pricing']['sale_price'] for prop in comparable_properties]
        prices_per_m2 = [prop['pricing']['price_per_m2'] for prop in comparable_properties]
        
        # Calculate coefficient of variation
        cv = statistics.stdev(prices_per_m2) / statistics.mean(prices_per_m2) if statistics.mean(prices_per_m2) > 0 else 0
        
        if cv < 0.1:
            return "Stable"
        elif cv < 0.2:
            return "Moderate volatility"
        else:
            return "High volatility"
    
    def _generate_recommendations(self, target_price: float, market_estimate: float, 
                                price_diff_percentage: float, is_overpriced: bool, 
                                is_underpriced: bool, confidence_score: float) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if is_overpriced:
            recommendations.append(f"Property appears overpriced by {abs(price_diff_percentage):.1f}%")
            recommendations.append(f"Consider reducing price to ${market_estimate:,.0f} for better market positioning")
        elif is_underpriced:
            recommendations.append(f"Property appears underpriced by {abs(price_diff_percentage):.1f}%")
            recommendations.append(f"Consider increasing price to ${market_estimate:,.0f} to maximize value")
        else:
            recommendations.append("Property is priced within market range")
        
        if confidence_score < 0.5:
            recommendations.append("Low confidence in analysis - consider gathering more comparable properties")
        elif confidence_score > 0.8:
            recommendations.append("High confidence in analysis - reliable market positioning")
        
        if price_diff_percentage > 20:
            recommendations.append("Significant price deviation - verify property characteristics and market conditions")
        
        return recommendations
    
    def get_market_summary(self) -> Dict[str, Any]:
        """Get comprehensive market summary"""
        if not self.market_stats or not self.analysis_results:
            return {}
        
        return {
            "market_statistics": {
                "mean_price": self.market_stats.mean_price,
                "median_price": self.market_stats.median_price,
                "price_range": self.market_stats.price_range,
                "standard_deviation": self.market_stats.standard_deviation,
                "coefficient_of_variation": self.market_stats.coefficient_of_variation,
                "price_per_m2_mean": self.market_stats.price_per_m2_mean,
                "price_per_m2_median": self.market_stats.price_per_m2_median
            },
            "property_analysis": {
                "original_price": self.analysis_results.original_price,
                "market_estimate": self.analysis_results.market_price_estimate,
                "price_difference": self.analysis_results.price_difference,
                "price_difference_percentage": self.analysis_results.price_difference_percentage,
                "is_overpriced": self.analysis_results.is_overpriced,
                "is_underpriced": self.analysis_results.is_underpriced,
                "confidence_score": self.analysis_results.confidence_score,
                "comparable_properties_count": self.analysis_results.comparable_properties_count,
                "market_trend": self.analysis_results.market_trend
            },
            "recommendations": self.analysis_results.recommendations
        }


# Example usage and testing
if __name__ == "__main__":
    # Create sample data
    sample_properties = [
        {
            "property_id": "prop_1",
            "characteristics": {
                "property_type": "apartment",
                "sale_type": "sale",
                "area_habitable": 80,
                "bedrooms": 3,
                "bathrooms": 2,
                "stratum": 4
            },
            "pricing": {
                "sale_price": 250000000,
                "price_per_m2": 3125000
            }
        },
        {
            "property_id": "prop_2",
            "characteristics": {
                "property_type": "apartment",
                "sale_type": "sale",
                "area_habitable": 75,
                "bedrooms": 3,
                "bathrooms": 2,
                "stratum": 4
            },
            "pricing": {
                "sale_price": 240000000,
                "price_per_m2": 3200000
            }
        }
    ]
    
    target_property = {
        "property_id": "target_1",
        "characteristics": {
            "property_type": "apartment",
            "sale_type": "sale",
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
    
    # Run analysis
    analyzer = RealEstateAnalyzer()
    analyzer.add_properties(sample_properties)
    analyzer.set_target_property(target_property)
    
    try:
        analysis = analyzer.analyze_market()
        summary = analyzer.get_market_summary()
        
        print("Analysis Results:")
        print(f"Original Price: ${analysis.original_price:,.0f}")
        print(f"Market Estimate: ${analysis.market_price_estimate:,.0f}")
        print(f"Price Difference: {analysis.price_difference_percentage:.1f}%")
        print(f"Overpriced: {analysis.is_overpriced}")
        print(f"Confidence: {analysis.confidence_score:.2f}")
        print(f"Recommendations: {analysis.recommendations}")
        
    except Exception as e:
        print(f"Analysis failed: {e}")
