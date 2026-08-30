"""
Download and Result Routes
Handles PDF download and result retrieval
"""

from fastapi import APIRouter, Path, HTTPException, status
from fastapi.responses import FileResponse
from app.core import logger
from app.models.response import ResultResponse
from app.services.job_manager import job_manager
from app.utils import file_exists, read_file

router = APIRouter()


@router.get("/download/{job_id}")
async def download_pdf(job_id: str = Path(..., description="Job ID")):
    """
    Download the generated summary PDF
    
    Args:
        job_id: Job ID
        
    Returns:
        PDF file for download
    """
    try:
        # Get job details
        job = job_manager.get_job(job_id)
        if not job:
            logger.error(f"Job not found: {job_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        # Check if processing is complete
        if job["status"] != "completed":
            logger.error(f"Job not completed: {job_id}, status: {job['status']}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Job not completed. Current status: {job['status']}"
            )
        
        output_file = job.get("output_file")
        if not output_file:
            logger.error(f"No output file for job: {job_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Output file not found"
            )
        
        # Check if file exists
        if not file_exists(output_file):
            logger.error(f"Output file not found: {output_file}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Output file not found"
            )
        
        logger.info(f"Downloading PDF for job {job_id}: {output_file}")

        response = FileResponse(
            path=output_file,
            media_type="application/pdf",
            filename=f"drawing_summary_{job_id}.pdf"
        )
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Cross-Origin-Resource-Policy"] = "cross-origin"
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading PDF for job {job_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error downloading PDF"
        )


@router.get("/result/{job_id}", response_model=ResultResponse)
async def get_result(job_id: str = Path(..., description="Job ID")) -> ResultResponse:
    """
    Get the processing result for a job
    
    Args:
        job_id: Job ID
        
    Returns:
        ResultResponse with summary data
    """
    try:
        # Get job details
        job = job_manager.get_job(job_id)
        if not job:
            logger.error(f"Job not found: {job_id}")
            return ResultResponse(
                success=False,
                error="Job not found"
            )
        
        # Check if processing is complete
        if job["status"] != "completed":
            logger.error(f"Job not completed: {job_id}, status: {job['status']}")
            return ResultResponse(
                success=False,
                error=f"Job not completed. Current status: {job['status']}"
            )
        
        result = job.get("result")
        if not result:
            logger.error(f"No result data for job: {job_id}")
            return ResultResponse(
                success=False,
                error="Result data not available"
            )
        
        logger.info(f"Retrieved result for job {job_id}")
        
        # Convert result dict to Summary object if needed
        from app.models.bom import Summary
        if isinstance(result, dict):
            summary = Summary(**result)
        else:
            summary = result
        
        return ResultResponse(
            success=True,
            data=summary
        )
    except Exception as e:
        logger.error(f"Error getting result for job {job_id}: {str(e)}")
        return ResultResponse(
            success=False,
            error=str(e)
        )
