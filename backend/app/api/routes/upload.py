"""
Upload Route Module
Handles PDF file uploads
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.core import logger, settings
from app.models.response import UploadResponse
from app.utils import validate_uploaded_pdf, generate_job_id, save_uploaded_file
from app.services.job_manager import job_manager

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)) -> UploadResponse:
    """
    Upload an engineering drawing PDF
    
    Args:
        file: PDF file to upload
        
    Returns:
        UploadResponse with job_id and filename
    """
    try:
        # Validate file type
        if file.content_type != "application/pdf":
            logger.error(f"Invalid file type: {file.content_type}")
            return UploadResponse(
                success=False,
                message="File must be a PDF",
                error="Invalid file type"
            )
        
        # Generate job ID
        job_id = generate_job_id()
        
        # Read file content
        content = await file.read()
        
        # Save file temporarily
        success, result = save_uploaded_file(job_id, file.filename or "drawing.pdf", content)
        
        if not success:
            logger.error(f"Failed to save file for job {job_id}: {result}")
            return UploadResponse(
                success=False,
                message="Failed to save file",
                error=result
            )
        
        file_path = result
        
        # Validate PDF
        is_valid, error_msg = validate_uploaded_pdf(file_path)
        if not is_valid:
            logger.error(f"Invalid PDF: {error_msg}")
            return UploadResponse(
                success=False,
                message="File is not a valid PDF",
                error=error_msg
            )
        
        # Create job in job manager
        job_manager.create_job(job_id, file.filename or "drawing.pdf", file_path)
        
        logger.info(f"Successfully uploaded PDF for job {job_id}: {file.filename}")
        
        return UploadResponse(
            success=True,
            job_id=job_id,
            filename=file.filename,
            message="File uploaded successfully"
        )
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        return UploadResponse(
            success=False,
            message="Error uploading file",
            error=str(e)
        )
