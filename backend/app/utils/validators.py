"""
Validators Module
Contains validation functions for files and data
"""

import os
from pathlib import Path
from app.core.config import settings


def is_valid_pdf(file_path: str) -> bool:
    """Check if file is a valid PDF"""
    if not os.path.exists(file_path):
        return False
    
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4)
            return header == b'%PDF'
    except Exception:
        return False


def validate_file_size(file_path: str) -> bool:
    """Validate file size is within limits"""
    try:
        file_size = os.path.getsize(file_path)
        return file_size <= settings.MAX_FILE_SIZE_BYTES
    except Exception:
        return False


def validate_uploaded_pdf(file_path: str) -> tuple[bool, str]:
    """
    Comprehensive validation for uploaded PDF
    Returns: (is_valid, error_message)
    """
    if not os.path.exists(file_path):
        return False, "File not found"
    
    if not is_valid_pdf(file_path):
        return False, "Invalid PDF file"
    
    if not validate_file_size(file_path):
        return False, f"File size exceeds {settings.MAX_FILE_SIZE_MB} MB limit"
    
    return True, ""


def safe_filename(filename: str) -> str:
    """Create a safe filename from user input"""
    # Remove path separators and dangerous characters
    dangerous_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '\x00']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    return filename
