"""
Pydantic Models for BOM Data
Defines the data structures for Bill of Materials components
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel


class Dimensions(BaseModel):
    """Component dimensions model"""
    length: Optional[float] = None
    width: Optional[float] = None
    thickness: Optional[float] = None
    diameter: Optional[float] = None
    outer_diameter: Optional[float] = None
    inner_diameter: Optional[float] = None
    nominal_bore: Optional[float] = None
    leg1: Optional[float] = None
    leg2: Optional[float] = None
    height: Optional[float] = None
    custom: Optional[Dict[str, Any]] = None


class BOMItem(BaseModel):
    """Individual Bill of Materials item"""
    part_no: str
    description: str
    material: Optional[str] = None
    dimensions: Optional[Dimensions] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    confidence: Optional[float] = None
    requires_review: Optional[bool] = False


class BOM(BaseModel):
    """Complete Bill of Materials"""
    bom: list[BOMItem]
    title_block: Optional[Dict[str, Any]] = None


class SummaryItem(BaseModel):
    """Summary item with calculated weights"""
    part_no: str
    description: str
    material: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    weight_per_unit: Optional[float] = None
    total_weight: Optional[float] = None
    calculation_status: str = "calculated"
    calculation_method: Optional[str] = None
    requires_review: Optional[bool] = False


class Summary(BaseModel):
    """Complete summary with all calculated data"""
    job_id: str
    summary: list[SummaryItem]
    grand_total_weight: Optional[float] = None
    extraction_method: str = "gemini_vision"
    processing_status: str = "completed"
