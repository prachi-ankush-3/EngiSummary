"""
Tests for PDF Upload
"""

import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.job_manager import job_manager
from app.utils.file_utils import get_output_path


client = TestClient(app)


def test_upload_valid_pdf(tmp_path):
    """Test uploading a valid PDF file"""
    # Create a minimal PDF
    pdf_content = b"%PDF-1.4\n%EOF"
    pdf_file = tmp_path / "test.pdf"
    pdf_file.write_bytes(pdf_content)
    
    # Upload file
    with open(pdf_file, "rb") as f:
        response = client.post(
            "/api/upload",
            files={"file": (f.name, f, "application/pdf")}
        )
    
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "job_id" in response.json()
    assert response.json()["filename"] == "test.pdf"


def test_upload_invalid_file_type(tmp_path):
    """Test uploading a non-PDF file"""
    # Create a text file
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("Hello World")
    
    # Try to upload as PDF
    with open(txt_file, "rb") as f:
        response = client.post(
            "/api/upload",
            files={"file": (f.name, f, "application/pdf")}
        )
    
    # Should fail PDF validation
    assert response.status_code == 200
    assert response.json()["success"] is False


def test_upload_missing_file():
    """Test upload with no file"""
    response = client.post("/api/upload")
    
    assert response.status_code == 422  # Unprocessable Entity


def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    
    assert response.status_code == 200
    assert "title" in response.json()
    assert response.json()["status"] == "running"


def test_download_response_avoids_cache_staleness():
    """Test that generated downloads are marked as non-cacheable."""
    job_id = f"cache-test-{uuid.uuid4()}"
    output_path = Path(get_output_path(job_id))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(b"%PDF-1.4\n%EOF")

    job_manager.create_job(job_id, "sample.pdf", str(output_path))
    job_manager.set_completed(job_id, str(output_path), {"job_id": job_id, "summary": []})

    response = client.get(f"/api/download/{job_id}")

    assert response.status_code == 200
    assert "no-store" in response.headers.get("cache-control", "").lower()
    assert response.headers.get("pragma", "").lower() == "no-cache"
    assert response.headers.get("expires", "") == "0"

    job_manager.delete_job(job_id)
