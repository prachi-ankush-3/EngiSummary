"""
Component Classification Models
Defines component types and their properties
"""

from enum import Enum
from pydantic import BaseModel
from typing import Optional


class ComponentType(str, Enum):
    """Enumeration of component types"""
    PIPE = "PIPE"
    PLATE = "PLATE"
    ANGLE = "ANGLE"
    CHANNEL = "CHANNEL"
    I_BEAM = "I_BEAM"
    UB = "UB"
    FLAT_BAR = "FLAT_BAR"
    ROUND_BAR = "ROUND_BAR"
    SQUARE_BAR = "SQUARE_BAR"
    BRACKET = "BRACKET"
    GUSSET = "GUSSET"
    OTHER = "OTHER"


class ComponentIdentification(BaseModel):
    """Identified component information"""
    component_type: ComponentType
    normalized_description: str
    original_description: str
    confidence: float = 0.95
