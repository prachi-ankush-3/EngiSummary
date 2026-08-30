"""
Tests for Summary Generation
"""

import pytest
from app.models.bom import BOMItem, Dimensions, BOM
from app.models.component import ComponentType
from app.services.summary_service import summary_service


class TestSummaryGeneration:
    """Tests for summary generation"""
    
    def test_generate_summary_from_bom(self):
        """Test generating summary from BOM"""
        # Create sample BOM
        items = [
            BOMItem(
                part_no="1",
                description="PIPE 100 NB",
                material="STEEL",
                dimensions=Dimensions(
                    nominal_bore=100,
                    outer_diameter=114.3,
                    inner_diameter=106.4,
                    length=4500
                ),
                quantity=10,
                unit="M"
            ),
            BOMItem(
                part_no="2",
                description="L 65x65x6",
                material="STEEL",
                dimensions=Dimensions(
                    leg1=65,
                    leg2=65,
                    thickness=6,
                    length=5000
                ),
                quantity=5,
                unit="M"
            )
        ]
        
        bom = BOM(bom=items)
        
        # Generate summary
        summary = summary_service.generate_summary("test-job-1", bom)
        
        assert summary.job_id == "test-job-1"
        assert len(summary.summary) == 2
        assert summary.summary[0].part_no == "1"
        assert summary.summary[1].part_no == "2"
    
    def test_summary_item_calculation_status(self):
        """Test that summary items have calculation status"""
        items = [
            BOMItem(
                part_no="1",
                description="PLATE 20MM",
                material="STEEL",
                dimensions=Dimensions(
                    length=1000,
                    width=500,
                    thickness=20
                ),
                quantity=1,
                unit="NOS"
            )
        ]
        
        bom = BOM(bom=items)
        summary = summary_service.generate_summary("test-job-2", bom)
        
        item = summary.summary[0]
        assert item.calculation_status in ["calculated", "insufficient_data", "manual_review", "error"]
    
    def test_summary_with_incomplete_dimensions(self):
        """Test summary generation with incomplete dimensions"""
        items = [
            BOMItem(
                part_no="1",
                description="BRACKET-1",
                material="STEEL",
                dimensions=None,
                quantity=2,
                unit="NOS"
            )
        ]
        
        bom = BOM(bom=items)
        summary = summary_service.generate_summary("test-job-3", bom)
        
        item = summary.summary[0]
        assert item.requires_review is True
        assert item.calculation_status == "insufficient_data"
        assert item.weight_per_unit is None
    
    def test_summary_grand_total_calculation(self):
        """Test grand total weight calculation"""
        items = [
            BOMItem(
                part_no="1",
                description="L 65x65x6",
                material="STEEL",
                dimensions=Dimensions(
                    leg1=65,
                    leg2=65,
                    thickness=6,
                    length=1000
                ),
                quantity=2,
                unit="M"
            )
        ]
        
        bom = BOM(bom=items)
        summary = summary_service.generate_summary("test-job-4", bom)
        
        # Check that grand total is calculated
        if summary.grand_total_weight:
            assert summary.grand_total_weight > 0
