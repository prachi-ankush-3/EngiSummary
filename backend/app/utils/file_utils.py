"""
File Utilities Module
Contains file handling utilities
"""

import os
import shutil
import uuid
from pathlib import Path
from typing import Tuple
from app.core.config import settings
from app.utils.validators import safe_filename
from app.core import logger


def generate_job_id() -> str:
    """Generate a unique job ID"""
    return str(uuid.uuid4())


def get_upload_path(job_id: str, filename: str) -> str:
    """Get the path for an uploaded file"""
    safe_name = safe_filename(filename)
    return os.path.join(settings.UPLOAD_DIR, job_id, safe_name)


def get_output_path(job_id: str) -> str:
    """Get the output PDF path for a job"""
    return os.path.join(settings.OUTPUT_DIR, f"drawing_summary_{job_id}.pdf")


def get_temp_path(job_id: str, filename: str = "") -> str:
    """Get temporary file path for a job"""
    temp_dir = os.path.join(settings.TEMP_DIR, job_id)
    Path(temp_dir).mkdir(parents=True, exist_ok=True)
    
    if filename:
        return os.path.join(temp_dir, safe_filename(filename))
    return temp_dir


def save_uploaded_file(job_id: str, filename: str, content: bytes) -> Tuple[bool, str]:
    """
    Save uploaded file to disk
    Returns: (success, file_path_or_error)
    """
    try:
        upload_path = get_upload_path(job_id, filename)
        
        # Create directory if needed
        Path(upload_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(upload_path, 'wb') as f:
            f.write(content)
        
        logger.info(f"File saved: {upload_path}")
        return True, upload_path
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        return False, str(e)


def cleanup_job_files(job_id: str) -> bool:
    """Clean up all files for a job"""
    try:
        # Clean upload directory
        upload_dir = os.path.join(settings.UPLOAD_DIR, job_id)
        if os.path.exists(upload_dir):
            shutil.rmtree(upload_dir)
        
        # Clean temp directory
        temp_dir = os.path.join(settings.TEMP_DIR, job_id)
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        
        logger.info(f"Cleaned up files for job: {job_id}")
        return True
    except Exception as e:
        logger.error(f"Error cleaning up files for job {job_id}: {str(e)}")
        return False


def file_exists(file_path: str) -> bool:
    """Check if a file exists"""
    return os.path.exists(file_path) and os.path.isfile(file_path)


def read_file(file_path: str) -> bytes:
    """Read file content"""
    with open(file_path, 'rb') as f:
        return f.read()
