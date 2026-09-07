"""
Routes Module
Contains all API route definitions
"""

from app.api.routes import upload, processing, status, download, email_pdf

__all__ = ["upload", "processing", "status", "download", "email_pdf"]
