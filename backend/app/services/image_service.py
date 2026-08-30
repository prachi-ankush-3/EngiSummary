"""
Image Service Module
Handles image processing and preprocessing
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Optional
from app.core import logger


class ImageService:
    """Service for image processing"""
    
    def __init__(self):
        """Initialize image service"""
        self.logger = logger
    
    def load_image(self, image_path: str) -> Optional[np.ndarray]:
        """Load image from file"""
        try:
            if not Path(image_path).exists():
                self.logger.error(f"Image file not found: {image_path}")
                return None
            
            image = cv2.imread(image_path)
            if image is None:
                self.logger.error(f"Failed to load image: {image_path}")
                return None
            
            return image
        except Exception as e:
            self.logger.error(f"Error loading image: {str(e)}")
            return None
    
    def save_image(self, image: np.ndarray, output_path: str) -> bool:
        """Save image to file"""
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(output_path, image)
            self.logger.info(f"Image saved: {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving image: {str(e)}")
            return False
    
    def resize_image(self, image: np.ndarray, max_width: int = 2000, 
                     max_height: int = 2000) -> np.ndarray:
        """Resize image to fit within max dimensions while maintaining aspect ratio"""
        try:
            height, width = image.shape[:2]
            
            scale = min(max_width / width, max_height / height, 1.0)
            
            if scale < 1.0:
                new_width = int(width * scale)
                new_height = int(height * scale)
                image = cv2.resize(image, (new_width, new_height), 
                                   interpolation=cv2.INTER_AREA)
            
            return image
        except Exception as e:
            self.logger.error(f"Error resizing image: {str(e)}")
            return image
    
    def convert_to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """Convert image to grayscale"""
        try:
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                return gray
            return image
        except Exception as e:
            self.logger.error(f"Error converting to grayscale: {str(e)}")
            return image
    
    def increase_contrast(self, image: np.ndarray, alpha: float = 1.5, 
                         beta: float = 0) -> np.ndarray:
        """Increase contrast of image"""
        try:
            adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
            return np.clip(adjusted, 0, 255).astype(np.uint8)
        except Exception as e:
            self.logger.error(f"Error increasing contrast: {str(e)}")
            return image
    
    def denoise_image(self, image: np.ndarray) -> np.ndarray:
        """Denoise image using bilateral filtering"""
        try:
            if len(image.shape) == 2:
                # Grayscale
                denoised = cv2.bilateralFilter(image, 9, 75, 75)
            else:
                # Color
                denoised = cv2.bilateralFilter(image, 9, 75, 75)
            return denoised
        except Exception as e:
            self.logger.error(f"Error denoising image: {str(e)}")
            return image
    
    def apply_adaptive_threshold(self, image: np.ndarray) -> np.ndarray:
        """Apply adaptive threshold to image"""
        try:
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY, 11, 2)
            return thresh
        except Exception as e:
            self.logger.error(f"Error applying adaptive threshold: {str(e)}")
            return image
    
    def preprocess_for_ocr(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for OCR"""
        try:
            # Denoise
            denoised = self.denoise_image(image)
            
            # Increase contrast
            enhanced = self.increase_contrast(denoised, alpha=1.3, beta=10)
            
            # Apply threshold if needed
            if len(enhanced.shape) == 3:
                gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
            else:
                gray = enhanced
            
            return gray
        except Exception as e:
            self.logger.error(f"Error preprocessing for OCR: {str(e)}")
            return image
    
    def get_image_dimensions(self, image: np.ndarray) -> tuple:
        """Get image dimensions (width, height)"""
        try:
            height, width = image.shape[:2]
            return (width, height)
        except Exception as e:
            self.logger.error(f"Error getting image dimensions: {str(e)}")
            return (0, 0)


# Create service instance
image_service = ImageService()
