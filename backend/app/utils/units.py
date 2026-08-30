"""
Units Module
Contains unit conversion utilities
"""

from enum import Enum
from typing import Dict, Optional


class LengthUnit(str, Enum):
    """Length unit enumeration"""
    MM = "mm"
    CM = "cm"
    M = "m"
    INCH = "in"


class WeightUnit(str, Enum):
    """Weight unit enumeration"""
    KG = "kg"
    G = "g"
    TON = "ton"
    LB = "lb"


class UnitConverter:
    """Utility class for unit conversions"""
    
    # Length conversions to meters
    LENGTH_TO_METERS: Dict[str, float] = {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1.0,
        "in": 0.0254,
        "inch": 0.0254,
    }
    
    # Weight conversions to kg
    WEIGHT_TO_KG: Dict[str, float] = {
        "kg": 1.0,
        "g": 0.001,
        "ton": 1000.0,
        "lb": 0.453592,
    }
    
    @staticmethod
    def to_meters(value: Optional[float], unit: Optional[str]) -> Optional[float]:
        """Convert length value to meters"""
        if value is None or unit is None:
            return None
        
        normalized_unit = unit.lower().strip()
        multiplier = UnitConverter.LENGTH_TO_METERS.get(normalized_unit)
        
        if multiplier is None:
            return None
        
        return value * multiplier
    
    @staticmethod
    def to_kg(value: Optional[float], unit: Optional[str]) -> Optional[float]:
        """Convert weight value to kilograms"""
        if value is None or unit is None:
            return None
        
        normalized_unit = unit.lower().strip()
        multiplier = UnitConverter.WEIGHT_TO_KG.get(normalized_unit)
        
        if multiplier is None:
            return None
        
        return value * multiplier
    
    @staticmethod
    def normalize_unit(unit: Optional[str]) -> Optional[str]:
        """Normalize unit string"""
        if unit is None:
            return None
        
        normalized = unit.lower().strip()
        
        # Common unit mappings
        unit_mappings = {
            "m": "M",
            "mm": "MM",
            "cm": "CM",
            "in": "IN",
            "inch": "IN",
            "kg": "KG",
            "g": "G",
            "nos": "NOS",
            "no": "NOS",
            "pcs": "PCS",
            "pc": "PCS",
        }
        
        return unit_mappings.get(normalized, unit)
