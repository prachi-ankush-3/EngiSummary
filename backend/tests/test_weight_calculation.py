"""
Tests for Weight Calculator
"""

import pytest
from app.models.bom import BOMItem, Dimensions
from app.models.component import ComponentType
from app.services.weight_calculator import weight_calculator


class TestWeightCalculator:
    """Tests for weight calculations"""
    
    def test_calculate_plate_weight(self):
        """Test plate weight calculation"""
        # Create a plate: 1000mm x 500mm x 20mm
        dims = Dimensions(
            length=1000,
            width=500,
            thickness=20
        )
        
        bom_item = BOMItem(
            part_no="1",
            description="PLATE 20MM",
            material="STEEL",
            dimensions=dims,
            quantity=1,
            unit="NOS"
        )
        
        weight, status, method = weight_calculator.calculate_weight(
            bom_item, ComponentType.PLATE
        )
        
        assert status == "calculated"
        assert weight is not None
        assert weight > 0
        assert method == "plate_volume_formula"
    
    def test_angle_weight_standard_section(self):
        """Test angle weight for standard section"""
        # Create angle: 65x65x6
        dims = Dimensions(
            leg1=65,
            leg2=65,
            thickness=6,
            length=1000
        )
        
        bom_item = BOMItem(
            part_no="2",
            description="L 65x65x6",
            material="STEEL",
            dimensions=dims,
            quantity=1,
            unit="M"
        )
        
        weight, status, method = weight_calculator.calculate_weight(
            bom_item, ComponentType.ANGLE
        )
        
        assert status == "calculated"
        assert weight is not None
        assert weight > 0
        assert method == "standard_section_mass"
    
    def test_insufficient_data(self):
        """Test with insufficient data"""
        # Create BOM item with no dimensions
        bom_item = BOMItem(
            part_no="3",
            description="BRACKET-1",
            material="STEEL",
            dimensions=None,
            quantity=1,
            unit="NOS"
        )
        
        weight, status, method = weight_calculator.calculate_weight(
            bom_item, ComponentType.BRACKET
        )
        
        assert status == "insufficient_data"
        assert weight is None
    
    def test_missing_dimensions(self):
        """Test with partially missing dimensions"""
        # Create plate with missing width
        dims = Dimensions(
            length=1000,
            thickness=20
            # width missing
        )
        
        bom_item = BOMItem(
            part_no="4",
            description="PLATE 20MM",
            material="STEEL",
            dimensions=dims,
            quantity=1,
            unit="NOS"
        )
        
        weight, status, method = weight_calculator.calculate_weight(
            bom_item, ComponentType.PLATE
        )
        
        assert status == "insufficient_data"
        assert weight is None
    
    def test_round_bar_weight(self):
        """Test round bar weight calculation"""
        # Create round bar: 25mm diameter, 1000mm length
        dims = Dimensions(
            diameter=25,
            length=1000
        )
        
        bom_item = BOMItem(
            part_no="5",
            description="ROUND BAR 25MM",
            material="STEEL",
            dimensions=dims,
            quantity=1,
            unit="M"
        )
        
        weight, status, method = weight_calculator.calculate_weight(
            bom_item, ComponentType.ROUND_BAR
        )
        
        assert status == "calculated"
        assert weight is not None
        assert weight > 0
        assert method == "round_bar_formula"
