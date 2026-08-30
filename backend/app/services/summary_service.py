"""
Summary Service Module
Generates summary data from BOM with calculated weights
"""

from typing import Optional
from app.core import logger
from app.models.bom import BOM, BOMItem, Summary, SummaryItem
from app.models.component import ComponentType
from app.services.component_parser import component_parser
from app.services.weight_calculator import weight_calculator
from app.utils.units import UnitConverter


class SummaryService:
    """Service for generating summary data from BOM"""
    
    def __init__(self):
        """Initialize summary service"""
        self.logger = logger
        self.component_parser = component_parser
        self.weight_calculator = weight_calculator
    
    def generate_summary(self, job_id: str, bom: BOM) -> Summary:
        """
        Generate summary from BOM data
        
        Args:
            job_id: Job ID
            bom: Extracted BOM
            
        Returns:
            Summary object with calculated weights
        """
        try:
            self.logger.info(f"Generating summary for job {job_id}")
            
            summary_items = []
            grand_total_weight = 0.0
            
            bom_items = bom.bom or []
            if not bom_items and bom.title_block:
                title_block = bom.title_block
                bom_items = [
                    BOMItem(
                        part_no=str(title_block.get("part_no") or title_block.get("partNumber") or ""),
                        description=str(title_block.get("drawing_title") or title_block.get("drawingTitle") or "Generated Summary"),
                        material=title_block.get("material"),
                        quantity=title_block.get("quantity"),
                        unit=title_block.get("unit") or "NOS"
                    )
                ]

            for bom_item in bom_items:
                try:
                    summary_item = self._process_bom_item(bom_item)
                    summary_items.append(summary_item)
                    
                    # Add to grand total if weight available
                    if summary_item.total_weight:
                        grand_total_weight += summary_item.total_weight
                except Exception as e:
                    self.logger.error(f"Error processing BOM item {bom_item.part_no}: {str(e)}")
                    summary_item = SummaryItem(
                        part_no=bom_item.part_no,
                        description=bom_item.description,
                        material=bom_item.material,
                        quantity=bom_item.quantity,
                        unit=bom_item.unit,
                        calculation_status="error",
                        requires_review=True
                    )
                    summary_items.append(summary_item)
            
            # Create summary
            summary = Summary(
                job_id=job_id,
                summary=summary_items,
                grand_total_weight=grand_total_weight if grand_total_weight > 0 else None,
                extraction_method="gemini_vision",
                processing_status="completed"
            )
            
            self.logger.info(f"Generated summary with {len(summary_items)} items, "
                           f"total weight: {grand_total_weight:.2f} kg")
            
            return summary
        except Exception as e:
            self.logger.error(f"Error generating summary: {str(e)}")
            return Summary(job_id=job_id, summary=[])
    
    def _process_bom_item(self, bom_item: BOMItem) -> SummaryItem:
        """Process a single BOM item and calculate its weight"""
        
        # Identify component type
        component_identification = self.component_parser.identify_component(bom_item)
        component_type = component_identification.component_type
        
        # Calculate weight per unit
        weight_per_unit = None
        calculation_status = "calculated"
        calculation_method = None
        requires_review = False
        
        try:
            weight_per_unit, calc_status, calc_method = self.weight_calculator.calculate_weight(
                bom_item, component_type
            )
            calculation_status = calc_status
            calculation_method = calc_method
            
            if calc_status in ["insufficient_data", "manual_review"]:
                requires_review = True
        except Exception as e:
            self.logger.error(f"Error calculating weight for {bom_item.part_no}: {str(e)}")
            calculation_status = "insufficient_data"
            requires_review = True
        
        # Calculate total weight
        total_weight = None
        if weight_per_unit is not None and bom_item.quantity is not None:
            try:
                # Handle different unit types
                if bom_item.unit and bom_item.unit.upper() in ["M", "MM"]:
                    # For length-based quantities
                    total_weight = weight_per_unit * bom_item.quantity
                else:
                    # For count-based quantities (NOS, PCS)
                    total_weight = weight_per_unit * bom_item.quantity
            except Exception as e:
                self.logger.error(f"Error calculating total weight: {str(e)}")
                requires_review = True
        
        # Create summary item
        summary_item = SummaryItem(
            part_no=bom_item.part_no,
            description=bom_item.description,
            material=bom_item.material,
            quantity=bom_item.quantity,
            unit=bom_item.unit,
            weight_per_unit=weight_per_unit,
            total_weight=total_weight,
            calculation_status=calculation_status,
            calculation_method=calculation_method,
            requires_review=requires_review
        )
        
        return summary_item


# Create service instance
summary_service = SummaryService()
