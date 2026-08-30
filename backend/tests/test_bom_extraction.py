"""
Tests for BOM Extraction and Parsing
"""

import pytest
from app.models.bom import BOMItem, Dimensions, BOM
from app.models.component import ComponentType
from app.services.component_parser import component_parser


class TestComponentParsing:
    """Tests for component identification"""
    
    def test_identify_pipe(self):
        """Test identifying pipe component"""
        bom_item = BOMItem(
            part_no="1",
            description="PIPE 100 NB",
            dimensions=None
        )
        
        identification = component_parser.identify_component(bom_item)
        
        assert identification.component_type == ComponentType.PIPE
        assert identification.confidence > 0.8
    
    def test_identify_plate(self):
        """Test identifying plate component"""
        bom_item = BOMItem(
            part_no="2",
            description="PLATE 20MM",
            dimensions=None
        )
        
        identification = component_parser.identify_component(bom_item)
        
        assert identification.component_type == ComponentType.PLATE
        assert identification.confidence > 0.8
    
    def test_identify_angle(self):
        """Test identifying angle component"""
        bom_item = BOMItem(
            part_no="3",
            description="L 65x65x6",
            dimensions=None
        )
        
        identification = component_parser.identify_component(bom_item)
        
        assert identification.component_type == ComponentType.ANGLE
        assert identification.confidence > 0.8
    
    def test_identify_ub(self):
        """Test identifying UB section"""
        bom_item = BOMItem(
            part_no="4",
            description="UB 406x178x67",
            dimensions=None
        )
        
        identification = component_parser.identify_component(bom_item)
        
        assert identification.component_type == ComponentType.UB
        assert identification.confidence > 0.8
    
    def test_identify_bracket(self):
        """Test identifying bracket"""
        bom_item = BOMItem(
            part_no="5",
            description="BRACKET-1",
            dimensions=None
        )
        
        identification = component_parser.identify_component(bom_item)
        
        assert identification.component_type == ComponentType.BRACKET
        assert identification.confidence > 0.8
    
    def test_identify_unknown(self):
        """Test identifying unknown component"""
        bom_item = BOMItem(
            part_no="99",
            description="UNKNOWN PART",
            dimensions=None
        )
        
        identification = component_parser.identify_component(bom_item)
        
        assert identification.component_type == ComponentType.OTHER
    
    def test_normalize_description_pipe(self):
        """Test normalizing pipe description"""
        bom_item = BOMItem(
            part_no="1",
            description="PIPE 100 NB",
            dimensions=None
        )
        
        identification = component_parser.identify_component(bom_item)
        
        assert "PIPE" in identification.normalized_description
        assert "100" in identification.normalized_description


class TestBOMModel:
    """Tests for BOM data model"""
    
    def test_create_bom_item(self):
        """Test creating a BOM item"""
        dims = Dimensions(
            length=1000,
            width=500,
            thickness=20
        )
        
        item = BOMItem(
            part_no="1",
            description="PLATE",
            material="STEEL",
            dimensions=dims,
            quantity=1,
            unit="NOS"
        )
        
        assert item.part_no == "1"
        assert item.description == "PLATE"
        assert item.dimensions.length == 1000
    
    def test_create_bom(self):
        """Test creating a BOM"""
        items = [
            BOMItem(
                part_no="1",
                description="PIPE 100 NB",
                quantity=10,
                unit="M"
            ),
            BOMItem(
                part_no="2",
                description="L 65x65x6",
                quantity=5,
                unit="M"
            )
        ]
        
        bom = BOM(bom=items)
        
        assert len(bom.bom) == 2
        assert bom.bom[0].part_no == "1"
        assert bom.bom[1].part_no == "2"
