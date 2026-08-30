"""
PDF Service Module
Handles PDF loading, rendering, and text extraction
"""

import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Tuple, Optional
from app.core import logger
from app.utils.file_utils import get_temp_path


class PDFService:
    """Service for PDF processing"""
    
    def __init__(self):
        """Initialize PDF service"""
        self.logger = logger
    
    def load_pdf(self, pdf_path: str) -> Optional[fitz.Document]:
        """Load PDF document"""
        try:
            if not Path(pdf_path).exists():
                self.logger.error(f"PDF file not found: {pdf_path}")
                return None
            
            doc = fitz.open(pdf_path)
            self.logger.info(f"Loaded PDF with {len(doc)} pages: {pdf_path}")
            return doc
        except Exception as e:
            self.logger.error(f"Error loading PDF: {str(e)}")
            return None
    
    def get_page_count(self, pdf_path: str) -> int:
        """Get number of pages in PDF"""
        doc = self.load_pdf(pdf_path)
        if doc is None:
            return 0
        page_count = len(doc)
        doc.close()
        return page_count
    
    def extract_text(self, pdf_path: str, page_num: int = -1) -> str:
        """
        Extract text from PDF
        page_num: -1 for all pages, 0-based index for specific page
        """
        try:
            doc = self.load_pdf(pdf_path)
            if doc is None:
                return ""
            
            text = ""
            
            if page_num == -1:
                # Extract from all pages
                for page in doc:
                    text += page.get_text()
            else:
                # Extract from specific page
                if 0 <= page_num < len(doc):
                    page = doc[page_num]
                    text = page.get_text()
            
            doc.close()
            return text
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    def render_page_to_image(self, pdf_path: str, page_num: int, job_id: str, 
                            zoom: float = 2.0) -> Optional[str]:
        """
        Render PDF page to image
        zoom: Zoom factor (1.0 = 72 DPI, 2.0 = 144 DPI, 3.0 = 216 DPI)
        Returns: Path to saved image
        """
        try:
            doc = self.load_pdf(pdf_path)
            if doc is None or page_num < 0 or page_num >= len(doc):
                return None
            
            page = doc[page_num]
            
            # Render page to image
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # Save image
            temp_dir = get_temp_path(job_id)
            image_path = Path(temp_dir) / f"page_{page_num}.png"
            pix.save(str(image_path))
            
            doc.close()
            self.logger.info(f"Rendered page {page_num} to image: {image_path}")
            return str(image_path)
        except Exception as e:
            self.logger.error(f"Error rendering page to image: {str(e)}")
            return None
    
    def render_pages_to_images(self, pdf_path: str, job_id: str, 
                               zoom: float = 2.0) -> List[str]:
        """
        Render all PDF pages to images
        Returns: List of image paths
        """
        try:
            doc = self.load_pdf(pdf_path)
            if doc is None:
                return []
            
            image_paths = []
            for page_num in range(len(doc)):
                image_path = self.render_page_to_image(pdf_path, page_num, job_id, zoom)
                if image_path:
                    image_paths.append(image_path)
            
            return image_paths
        except Exception as e:
            self.logger.error(f"Error rendering pages to images: {str(e)}")
            return []
    
    def get_page_dimensions(self, pdf_path: str, page_num: int = 0) -> Tuple[float, float]:
        """Get page dimensions (width, height) in points"""
        try:
            doc = self.load_pdf(pdf_path)
            if doc is None or page_num < 0 or page_num >= len(doc):
                return (0, 0)
            
            page = doc[page_num]
            rect = page.rect
            dimensions = (rect.width, rect.height)
            
            doc.close()
            return dimensions
        except Exception as e:
            self.logger.error(f"Error getting page dimensions: {str(e)}")
            return (0, 0)


# Create service instance
pdf_service = PDFService()
