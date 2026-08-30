"""
Weight Calculator Module
Calculates component weights based on dimensions
"""

import math
from typing import Optional, Dict, Tuple
from app.core import logger, settings
from app.models.bom import BOMItem
from app.models.component import ComponentType
from app.utils.units import UnitConverter


class WeightCalculator:
    """Service for calculating component weights"""
    
    # Standard steel section masses (kg/m)
    STANDARD_UB_MASSES = {
        "406x178x54": 54,
        "406x178x60": 60,
        "406x178x67": 67,
        "406x178x74": 74,
        "356x171x45": 45,
        "356x171x51": 51,
        "356x171x57": 57,
        "305x165x40": 40,
        "305x165x46": 46,
        "305x165x54": 54,
        "254x146x37": 37,
        "254x146x43": 43,
    }
    
    STANDARD_ANGLE_MASSES = {
        "50x50x5": 3.77,
        "65x65x6": 5.8,
        "75x75x6": 6.87,
        "100x100x8": 12.2,
        "125x125x10": 18.8,
    }
    
    def __init__(self):
        """Initialize weight calculator"""
        self.logger = logger
        self.steel_density = settings.STEEL_DENSITY  # kg/m³
    
    def calculate_weight(self, bom_item: BOMItem, component_type: ComponentType) -> Tuple[Optional[float], str, Optional[str]]:
        """
        Calculate weight for a component
        
        Returns:
            (weight_in_kg, calculation_status, calculation_method)
            calculation_status: "calculated", "insufficient_data", "manual_review"
        """
        try:
            if not bom_item.dimensions:
                return None, "insufficient_data", None
            
            # Route to component-specific calculator
            if component_type == ComponentType.PIPE:
                return self._calculate_pipe_weight(bom_item)
            elif component_type == ComponentType.PLATE:
                return self._calculate_plate_weight(bom_item)
            elif component_type == ComponentType.ANGLE:
                return self._calculate_angle_weight(bom_item)
            elif component_type == ComponentType.UB:
                return self._calculate_ub_weight(bom_item)
            elif component_type == ComponentType.FLAT_BAR:
                return self._calculate_flat_bar_weight(bom_item)
            elif component_type == ComponentType.ROUND_BAR:
                return self._calculate_round_bar_weight(bom_item)
            elif component_type == ComponentType.SQUARE_BAR:
                return self._calculate_square_bar_weight(bom_item)
            else:
                return None, "manual_review", None
        except Exception as e:
            self.logger.error(f"Error calculating weight: {str(e)}")
            return None, "insufficient_data", None
    
    def _calculate_pipe_weight(self, bom_item: BOMItem) -> Tuple[Optional[float], str, Optional[str]]:
        """Calculate weight for pipe"""
        try:
            dims = bom_item.dimensions
            
            # Need either OD/ID or nominal bore
            od = dims.outer_diameter
            id_ = dims.inner_diameter
            nb = dims.nominal_bore
            length = dims.length
            
            # Get length value
            if not length:
                return None, "insufficient_data", None
            
            # Convert length to meters
            length_m = UnitConverter.to_meters(length, bom_item.unit) or length / 1000
            
            # If we have OD and ID
            if od is not None and id_ is not None:
                od_m = UnitConverter.to_meters(od, "mm")
                id_m = UnitConverter.to_meters(id_, "mm")
                
                # Cross-sectional area
                area = math.pi / 4 * (od_m**2 - id_m**2)
                weight = area * self.steel_density * length_m
                
                return weight, "calculated", "od_id_formula"
            
            # If we have nominal bore, use standard mapping
            if nb is not None:
                # Standard pipe dimensions (simplified)
                # This is a fallback - in reality, need proper pipe schedule data
                return None, "insufficient_data", None
            
            return None, "insufficient_data", None
        except Exception as e:
            self.logger.error(f"Error calculating pipe weight: {str(e)}")
            return None, "insufficient_data", None
    
    def _calculate_plate_weight(self, bom_item: BOMItem) -> Tuple[Optional[float], str, Optional[str]]:
        """Calculate weight for plate"""
        try:
            dims = bom_item.dimensions
            length = dims.length
            width = dims.width
            thickness = dims.thickness
            
            if not thickness:
                return None, "insufficient_data", None
            
            # If we have length and width
            if length is not None and width is not None:
                # Convert to meters
                length_m = UnitConverter.to_meters(length, "mm")
                width_m = UnitConverter.to_meters(width, "mm")
                thickness_m = UnitConverter.to_meters(thickness, "mm")
                
                # Volume
                volume = length_m * width_m * thickness_m
                weight = volume * self.steel_density
                
                return weight, "calculated", "plate_volume_formula"
            
            # If only thickness is known
            return None, "insufficient_data", None
        except Exception as e:
            self.logger.error(f"Error calculating plate weight: {str(e)}")
            return None, "insufficient_data", None
    
    def _calculate_angle_weight(self, bom_item: BOMItem) -> Tuple[Optional[float], str, Optional[str]]:
        """Calculate weight for angle section"""
        try:
            dims = bom_item.dimensions
            leg1 = dims.leg1
            leg2 = dims.leg2
            thickness = dims.thickness
            length = dims.length
            
            if not all([leg1, leg2, thickness, length]):
                return None, "insufficient_data", None
            
            # Check for standard section
            angle_key = f"{int(leg1)}x{int(leg2)}x{int(thickness)}"
            if angle_key in self.STANDARD_ANGLE_MASSES:
                mass_per_meter = self.STANDARD_ANGLE_MASSES[angle_key]
                length_m = UnitConverter.to_meters(length, "mm")
                weight = mass_per_meter * length_m
                return weight, "calculated", "standard_section_mass"
            
            # Calculate from cross-sectional area
            # For equal angle: A = t × (2a - t)
            leg_m = UnitConverter.to_meters(leg1, "mm")
            thick_m = UnitConverter.to_meters(thickness, "mm")
            length_m = UnitConverter.to_meters(length, "mm")
            
            area = thick_m * (2 * leg_m - thick_m)
            weight = area * self.steel_density * length_m
            
            return weight, "calculated", "angle_cross_section_formula"
        except Exception as e:
            self.logger.error(f"Error calculating angle weight: {str(e)}")
            return None, "insufficient_data", None
    
    def _calculate_ub_weight(self, bom_item: BOMItem) -> Tuple[Optional[float], str, Optional[str]]:
        """Calculate weight for UB/I-beam section"""
        try:
            dims = bom_item.dimensions
            length = dims.length
            
            if not length:
                return None, "insufficient_data", None
            
            # Extract dimensions from description or use direct values
            height = getattr(dims, 'height', None)
            width = getattr(dims, 'width', None)
            
            # Try to match standard UB section
            # The description typically contains the mass
            desc = bom_item.description.upper()
            
            # Try to extract mass from description (last number often indicates mass)
            import re
            matches = re.findall(r'(\d+)', desc)
            if matches and len(matches) >= 3:
                # Format: UB 406x178x67 (height x width x mass)
                mass_per_meter = float(matches[-1])
                length_m = UnitConverter.to_meters(length, "mm")
                weight = mass_per_meter * length_m
                return weight, "calculated", "standard_section_mass"
            
            return None, "insufficient_data", None
        except Exception as e:
            self.logger.error(f"Error calculating UB weight: {str(e)}")
            return None, "insufficient_data", None
    
    def _calculate_flat_bar_weight(self, bom_item: BOMItem) -> Tuple[Optional[float], str, Optional[str]]:
        """Calculate weight for flat bar"""
        try:
            dims = bom_item.dimensions
            width = dims.width or dims.leg1
            thickness = dims.thickness
            length = dims.length
            
            if not all([width, thickness, length]):
                return None, "insufficient_data", None
            
            # Convert to meters
            width_m = UnitConverter.to_meters(width, "mm")
            thick_m = UnitConverter.to_meters(thickness, "mm")
            length_m = UnitConverter.to_meters(length, "mm")
            
            # Cross-sectional area
            area = width_m * thick_m
            weight = area * self.steel_density * length_m
            
            return weight, "calculated", "flat_bar_formula"
        except Exception as e:
            self.logger.error(f"Error calculating flat bar weight: {str(e)}")
            return None, "insufficient_data", None
    
    def _calculate_round_bar_weight(self, bom_item: BOMItem) -> Tuple[Optional[float], str, Optional[str]]:
        """Calculate weight for round bar"""
        try:
            dims = bom_item.dimensions
            diameter = dims.diameter
            length = dims.length
            
            if not all([diameter, length]):
                return None, "insufficient_data", None
            
            # Convert to meters
            diameter_m = UnitConverter.to_meters(diameter, "mm")
            length_m = UnitConverter.to_meters(length, "mm")
            
            # Cross-sectional area
            area = math.pi * (diameter_m / 2) ** 2
            weight = area * self.steel_density * length_m
            
            return weight, "calculated", "round_bar_formula"
        except Exception as e:
            self.logger.error(f"Error calculating round bar weight: {str(e)}")
            return None, "insufficient_data", None
    
    def _calculate_square_bar_weight(self, bom_item: BOMItem) -> Tuple[Optional[float], str, Optional[str]]:
        """Calculate weight for square bar"""
        try:
            dims = bom_item.dimensions
            side = dims.leg1 or dims.width
            length = dims.length
            
            if not all([side, length]):
                return None, "insufficient_data", None
            
            # Convert to meters
            side_m = UnitConverter.to_meters(side, "mm")
            length_m = UnitConverter.to_meters(length, "mm")
            
            # Cross-sectional area
            area = side_m ** 2
            weight = area * self.steel_density * length_m
            
            return weight, "calculated", "square_bar_formula"
        except Exception as e:
            self.logger.error(f"Error calculating square bar weight: {str(e)}")
            return None, "insufficient_data", None


# Create service instance
weight_calculator = WeightCalculator()
