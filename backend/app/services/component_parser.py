"""
Component Parser Module
Identifies and classifies component types
"""

import re
from typing import Tuple, Optional
from app.core import logger
from app.models.component import ComponentType, ComponentIdentification
from app.models.bom import BOMItem


class ComponentParser:
    """Service for parsing and identifying components"""
    
    def __init__(self):
        """Initialize component parser"""
        self.logger = logger
        
        # Component type patterns
        self.patterns = {
            ComponentType.PIPE: [
                r'PIPE\s*(\d+)\s*NB',
                r'^\s*PIPE\s+',
                r'TUBE\s*(\d+)',
            ],
            ComponentType.PLATE: [
                r'PLATE\s*(\d+(?:\.\d+)?)\s*(?:MM|M|X)?',
                r'PL\s*(\d+)',
                r'^\s*PLATE\s+',
            ],
            ComponentType.ANGLE: [
                r'[AL]\s*(\d+)X(\d+)X(\d+)',
                r'ANGLE\s+',
                r'^\s*L\s+\d+',
            ],
            ComponentType.CHANNEL: [
                r'[C]\s*(\d+)(?:X)?',
                r'CHANNEL\s+',
                r'^\s*C\s+\d+',
            ],
            ComponentType.I_BEAM: [
                r'I[\s-]?BEAM',
                r'IBEAM',
            ],
            ComponentType.UB: [
                r'UB\s*(\d+)X(\d+)X(\d+)',
                r'^\s*UB\s+',
            ],
            ComponentType.FLAT_BAR: [
                r'FLAT\s*BAR',
                r'FB\s*(\d+)X(\d+)',
                r'^\s*F\.B\s+',
            ],
            ComponentType.ROUND_BAR: [
                r'ROUND\s*BAR',
                r'ROD\s+',
                r'^\s*\u00D8\s*(\d+)',
            ],
            ComponentType.SQUARE_BAR: [
                r'SQUARE\s*BAR',
                r'SB\s*(\d+)',
            ],
            ComponentType.BRACKET: [
                r'BRACKET',
                r'BRKT',
                r'BRK\s*-?\s*\d+',
            ],
            ComponentType.GUSSET: [
                r'GUSSET',
                r'GUST',
            ],
        }
    
    def identify_component(self, bom_item: BOMItem) -> ComponentIdentification:
        """
        Identify component type from BOM item
        
        Args:
            bom_item: BOM item to identify
            
        Returns:
            ComponentIdentification object
        """
        try:
            description = bom_item.description
            if not description:
                return ComponentIdentification(
                    component_type=ComponentType.OTHER,
                    normalized_description=description,
                    original_description=description,
                    confidence=0.5
                )
            
            # Normalize description
            normalized = description.upper().strip()
            
            # Check patterns
            component_type, confidence = self._match_component_type(normalized)
            normalized_desc = self._normalize_description(normalized, component_type)
            
            return ComponentIdentification(
                component_type=component_type,
                normalized_description=normalized_desc,
                original_description=description,
                confidence=confidence
            )
        except Exception as e:
            self.logger.error(f"Error identifying component: {str(e)}")
            return ComponentIdentification(
                component_type=ComponentType.OTHER,
                normalized_description=bom_item.description,
                original_description=bom_item.description,
                confidence=0.0
            )
    
    def _match_component_type(self, description: str) -> Tuple[ComponentType, float]:
        """
        Match description against component type patterns
        
        Returns:
            (component_type, confidence)
        """
        # Check each component type
        for comp_type, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, description, re.IGNORECASE):
                    confidence = 0.95
                    return comp_type, confidence
        
        # Default to OTHER
        return ComponentType.OTHER, 0.5
    
    def _normalize_description(self, description: str, component_type: ComponentType) -> str:
        """Normalize description for a component type"""
        try:
            # Remove extra whitespace
            normalized = ' '.join(description.split())
            
            # Component-specific normalization
            if component_type == ComponentType.PIPE:
                # Extract nominal bore and length
                match = re.search(r'(\d+)\s*NB', normalized)
                if match:
                    nb = match.group(1)
                    return f"PIPE {nb} NB"
            
            elif component_type == ComponentType.PLATE:
                # Extract thickness
                match = re.search(r'(\d+(?:\.\d+)?)\s*MM', normalized)
                if match:
                    thickness = match.group(1)
                    return f"PLATE {thickness}MM"
            
            elif component_type == ComponentType.ANGLE:
                # Extract dimensions
                match = re.search(r'(\d+)\s*X\s*(\d+)\s*X\s*(\d+)', normalized)
                if match:
                    leg1, leg2, thickness = match.groups()
                    return f"L {leg1}x{leg2}x{thickness}"
            
            elif component_type == ComponentType.UB:
                # Extract dimensions
                match = re.search(r'(\d+)\s*X\s*(\d+)\s*X\s*(\d+)', normalized)
                if match:
                    height, width, mass = match.groups()
                    return f"UB {height}x{width}x{mass}"
            
            return normalized
        except Exception as e:
            self.logger.error(f"Error normalizing description: {str(e)}")
            return description


# Create service instance
component_parser = ComponentParser()
