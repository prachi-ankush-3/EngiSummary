"""
Status Route Module
Handles job status queries
"""

from fastapi import APIRouter, Path, HTTPException, status
from app.core import logger
from app.models.response import ProcessingStatus
from app.services.job_manager import job_manager

router = APIRouter()


@router.get("/status/{job_id}", response_model=ProcessingStatus)
async def get_status(job_id: str = Path(..., description="Job ID")) -> ProcessingStatus:
    """
    Get the processing status of a job
    
    Args:
        job_id: Job ID
        
    Returns:
        ProcessingStatus with current status and progress
    """
    try:
        # Get job details
        job = job_manager.get_job(job_id)
        if not job:
            logger.error(f"Job not found: {job_id}")
            return ProcessingStatus(
                job_id=job_id,
                status="not_found",
                progress=0,
                stage="Job not found",
                error="Job not found"
            )
        
        logger.info(f"Retrieved status for job {job_id}: {job['status']}")
        
        return ProcessingStatus(
            job_id=job_id,
            status=job["status"],
            progress=job.get("progress", 0),
            stage=job.get("stage", ""),
            error=job.get("error")
        )
    except Exception as e:
        logger.error(f"Error getting status for job {job_id}: {str(e)}")
        return ProcessingStatus(
            job_id=job_id,
            status="error",
            progress=0,
            stage="Error",
            error=str(e)
        )
