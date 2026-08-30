"""
Gemini Service Module
Handles integration with Google Gemini Vision API for BOM extraction
"""

import google.generativeai as genai
import base64
import json
from pathlib import Path
from typing import Optional, Dict, Any
from app.core import logger, settings
from app.models.bom import BOM, BOMItem, Dimensions


class GeminiService:
    """Service for Gemini Vision API integration"""
    
    def __init__(self):
        """Initialize Gemini service"""
        self.logger = logger
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            self.logger.warning("Gemini API key not configured")
    
    def encode_image_to_base64(self, image_path: str) -> Optional[str]:
        """Encode image file to base64 string"""
        try:
            if not Path(image_path).exists():
                self.logger.error(f"Image file not found: {image_path}")
                return None
            
            with open(image_path, 'rb') as image_file:
                return base64.standard_b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            self.logger.error(f"Error encoding image to base64: {str(e)}")
            return None
    
    def get_bom_extraction_prompt(self) -> str:
        """Get the prompt for BOM extraction"""
        return """You are an expert at reading engineering drawings and extracting Bill of Materials (BOM) and title-block information.

Your job is to read the provided technical drawing and return structured JSON only.

IMPORTANT RULES:
1. Read only what is visibly present in the drawing.
2. Do not invent missing dimensions, weights, or materials.
3. Keep part numbers, descriptions, and material names as they appear in the drawing.
4. Distinguish BOM rows from drawing notes, dimensions, and annotations.
5. If a field is not visible, use null.
6. If no BOM table is visible, return {"bom": [], "title_block": { ...visible title block data... }}
7. Return valid JSON only, no markdown fences and no prose.

Extract the following information from the title block and BOM table if present:
- part_no
- drawing_title
- material
- quantity
- scale
- revision
- tolerance
- surface_finish
- weight
- generated_by
- date

JSON schema:
{
  "title_block": {
    "part_no": "ENG-4471-B",
    "drawing_title": "Bracket Mounting Assembly",
    "material": "Aluminium 6061-T6",
    "quantity": 12,
    "scale": "1:5",
    "revision": "C",
    "tolerance": "ISO 2768-m",
    "surface_finish": "Ra 3.2",
    "weight": "0.86 kg",
    "generated_by": "EngiSummary AI",
    "date": "2026-08-30"
  },
  "bom": [
    {
      "part_no": "1",
      "description": "PIPE 100 NB",
      "material": "STEEL",
      "dimensions": {
        "nominal_bore": 100,
        "length": 4.5,
        "other_relevant_dims": "as shown"
      },
      "quantity": 1,
      "unit": "M"
    }
  ]
}

For dimensions:
- If it says "L 65x65x6" interpret it as an angle with 65x65x6 dimensions.
- If it says "PLATE 20MM" interpret it as a plate with thickness 20mm only.
- Include relevant dimensions only when they are clearly shown.
- Do not invent missing values.

Return only the JSON."""
    
    def extract_bom_from_image(self, image_path: str) -> Optional[BOM]:
        """
        Extract BOM information from an image using Gemini Vision
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Parsed BOM object or None if extraction fails
        """
        try:
            if not self.api_key:
                self.logger.error("Gemini API key not configured")
                return None
            
            # Encode image
            image_base64 = self.encode_image_to_base64(image_path)
            if not image_base64:
                return None
            
            # Get model
            model = genai.GenerativeModel(self.model_name)
            
            # Prepare message
            prompt = self.get_bom_extraction_prompt()
            
            # Send request to Gemini
            self.logger.info(f"Sending image to Gemini for BOM extraction: {image_path}")
            response = model.generate_content([
                prompt,
                {
                    "mime_type": "image/png",
                    "data": image_base64
                }
            ])
            
            # Extract response text
            response_text = response.text
            self.logger.info(f"Received response from Gemini")
            
            # Parse JSON from response
            bom_data = self._parse_json_response(response_text)
            if not bom_data:
                self.logger.error("Failed to parse Gemini response as JSON")
                return None
            
            # Validate and create BOM object
            bom = self._create_bom_object(bom_data)
            self.logger.info(f"Extracted BOM with {len(bom.bom)} items")
            
            return bom
        except Exception as e:
            self.logger.error(f"Error extracting BOM from image: {str(e)}")
            return None
    
    def _parse_json_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """
        Parse JSON from Gemini response
        Handles cases where response contains JSON within text
        """
        try:
            # Try direct JSON parsing
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Try to extract JSON from response text
            try:
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}')
                
                if start_idx != -1 and end_idx != -1:
                    json_str = response_text[start_idx:end_idx + 1]
                    return json.loads(json_str)
            except Exception:
                pass
            
            self.logger.error(f"Could not parse JSON from response: {response_text[:200]}")
            return None
    
    def _create_bom_object(self, bom_data: Dict[str, Any]) -> BOM:
        """Create BOM object from parsed data"""
        try:
            bom_items = []
            
            for item_data in bom_data.get("bom", []):
                dims_data = item_data.get("dimensions", {})
                dimensions = Dimensions(**dims_data) if isinstance(dims_data, dict) and dims_data else None

                bom_item = BOMItem(
                    part_no=str(item_data.get("part_no", "")),
                    description=str(item_data.get("description", "")),
                    material=item_data.get("material"),
                    dimensions=dimensions,
                    quantity=item_data.get("quantity"),
                    unit=item_data.get("unit"),
                    confidence=item_data.get("confidence", 0.9)
                )
                bom_items.append(bom_item)

            title_block = bom_data.get("title_block")
            if isinstance(title_block, dict) and title_block:
                part_no = title_block.get("part_no") or title_block.get("partNumber")
                description = title_block.get("drawing_title") or title_block.get("drawingTitle")
                material = title_block.get("material")
                quantity = title_block.get("quantity")
                unit = title_block.get("unit") or "NOS"

                if not bom_items and (part_no or description):
                    bom_items.append(BOMItem(
                        part_no=str(part_no or ""),
                        description=str(description or "Generated Summary"),
                        material=str(material) if material else None,
                        quantity=quantity,
                        unit=unit,
                        confidence=0.9,
                    ))

            return BOM(bom=bom_items, title_block=title_block)
        except Exception as e:
            self.logger.error(f"Error creating BOM object: {str(e)}")
            return BOM(bom=[])


# Create service instance
gemini_service = GeminiService()
