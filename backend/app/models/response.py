"""
API Response Models
Defines the structure of API responses
"""

from typing import Optional, Any
from pydantic import BaseModel
from app.models.bom import Summary


class UploadResponse(BaseModel):
    """Response for PDF upload endpoint"""
    success: bool
    job_id: Optional[str] = None
    filename: Optional[str] = None
    message: str
    error: Optional[str] = None


class ProcessingStatus(BaseModel):
    """Response for processing status endpoint"""
    job_id: str
    status: str
    progress: int
    stage: str
    error: Optional[str] = None


class DownloadResponse(BaseModel):
    """Response for download endpoint"""
    filename: str
    content_type: str


class ResultResponse(BaseModel):
    """Response for result endpoint"""
    success: bool
    data: Optional[Summary] = None
    error: Optional[str] = None


class SendPdfEmailRequest(BaseModel):
    """Request body for sending the generated PDF by email"""
    email: str


class SendPdfEmailResponse(BaseModel):
    """Response for send-PDF-via-email endpoint"""
    success: bool
    message: Optional[str] = None
    error: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response"""
    success: bool = False
    error: str
    details: Optional[Any] = None
