"""
BOM Extractor Module
Handles BOM detection and extraction from PDF
"""

from typing import Optional, List
from app.core import logger
from app.services.pdf_service import pdf_service
from app.services.image_service import image_service
from app.services.gemini_service import gemini_service
from app.models.bom import BOM


class BOMExtractor:
    """Service for extracting BOM from engineering drawings"""
    
    def __init__(self):
        """Initialize BOM extractor"""
        self.logger = logger
        self.pdf_service = pdf_service
        self.image_service = image_service
        self.gemini_service = gemini_service
    
    def extract_bom_from_pdf(self, pdf_path: str, job_id: str) -> Optional[BOM]:
        """
        Extract BOM from PDF by rendering pages and using Gemini Vision
        
        Args:
            pdf_path: Path to the PDF file
            job_id: Job ID for temporary file storage
            
        Returns:
            Extracted BOM object or None if extraction fails
        """
        try:
            self.logger.info(f"Starting BOM extraction from PDF: {pdf_path}")
            
            # Get page count
            page_count = self.pdf_service.get_page_count(pdf_path)
            if page_count == 0:
                self.logger.error("PDF has no pages")
                return None
            
            self.logger.info(f"PDF has {page_count} pages")
            
            # Extract text to find BOM pages
            bom_pages = self._find_bom_pages(pdf_path)
            self.logger.info(f"Found potential BOM on pages: {bom_pages}")
            
            # If no BOM pages found from text, try visual detection
            if not bom_pages:
                bom_pages = [p for p in range(min(page_count, 5))]
                self.logger.info(f"Using visual detection on pages: {bom_pages}")
            
            # Try to extract BOM from each potential page
            for page_num in bom_pages:
                bom = self._extract_bom_from_page(pdf_path, page_num, job_id)
                if bom and len(bom.bom) > 0:
                    self.logger.info(f"Successfully extracted BOM from page {page_num}")
                    return bom
            
            self.logger.error("Could not extract BOM from any page")
            return None
        except Exception as e:
            self.logger.error(f"Error extracting BOM from PDF: {str(e)}")
            return None
    
    def _find_bom_pages(self, pdf_path: str) -> List[int]:
        """
        Find pages containing BOM information by analyzing text
        
        Returns:
            List of page indices (0-based) that likely contain BOM
        """
        try:
            bom_pages = []
            page_count = self.pdf_service.get_page_count(pdf_path)
            
            bom_keywords = ["BOM", "BILL OF MATERIALS", "PARTS LIST", "COMPONENT", 
                           "PART NO", "DESCRIPTION", "QUANTITY", "MATERIAL"]
            
            for page_num in range(page_count):
                text = self.pdf_service.extract_text(pdf_path, page_num).upper()
                
                # Count BOM keywords
                keyword_count = sum(1 for keyword in bom_keywords if keyword in text)
                
                if keyword_count >= 2:
                    bom_pages.append(page_num)
            
            return bom_pages
        except Exception as e:
            self.logger.error(f"Error finding BOM pages: {str(e)}")
            return []
    
    def _extract_bom_from_page(self, pdf_path: str, page_num: int, job_id: str) -> Optional[BOM]:
        """
        Extract BOM from a specific PDF page
        
        Args:
            pdf_path: Path to the PDF file
            page_num: Page number (0-based)
            job_id: Job ID for temporary file storage
            
        Returns:
            Extracted BOM or None
        """
        try:
            self.logger.info(f"Extracting BOM from page {page_num}")
            
            # Render page to image
            image_path = self.pdf_service.render_page_to_image(pdf_path, page_num, job_id)
            if not image_path:
                self.logger.error(f"Failed to render page {page_num} to image")
                return None
            
            # Load image
            image = self.image_service.load_image(image_path)
            if image is None:
                return None
            
            # Resize image for Gemini (keep reasonable size)
            image = self.image_service.resize_image(image, max_width=2000, max_height=2000)
            
            # Save resized image
            self.image_service.save_image(image, image_path)
            
            # Extract BOM using Gemini Vision
            bom = self.gemini_service.extract_bom_from_image(image_path)
            
            return bom
        except Exception as e:
            self.logger.error(f"Error extracting BOM from page {page_num}: {str(e)}")
            return None


# Create service instance
bom_extractor = BOMExtractor()
