"""
Job Manager Module
Manages processing jobs and their status
"""

from typing import Optional, Dict, Any
from datetime import datetime
from app.core import logger


class JobManager:
    """In-memory job manager for tracking processing jobs"""
    
    def __init__(self):
        """Initialize job manager"""
        self.logger = logger
        self.jobs: Dict[str, Dict[str, Any]] = {}
    
    def create_job(self, job_id: str, filename: str, input_file: str) -> Dict[str, Any]:
        """Create a new job"""
        job = {
            "job_id": job_id,
            "status": "uploaded",
            "progress": 0,
            "stage": "File uploaded",
            "filename": filename,
            "input_file": input_file,
            "output_file": None,
            "result": None,
            "error": None,
            "created_at": datetime.now().isoformat(),
            "started_at": None,
            "completed_at": None
        }
        
        self.jobs[job_id] = job
        self.logger.info(f"Created job: {job_id}")
        
        return job
    
    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job details"""
        return self.jobs.get(job_id)
    
    def update_job(self, job_id: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Update job details"""
        job = self.get_job(job_id)
        if job:
            job.update(kwargs)
            return job
        return None
    
    def set_processing(self, job_id: str, stage: str, progress: int = 10) -> Optional[Dict[str, Any]]:
        """Mark job as processing"""
        return self.update_job(
            job_id,
            status="processing",
            stage=stage,
            progress=progress,
            started_at=datetime.now().isoformat()
        )
    
    def set_completed(self, job_id: str, output_file: str, result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Mark job as completed"""
        return self.update_job(
            job_id,
            status="completed",
            progress=100,
            stage="Processing complete",
            output_file=output_file,
            result=result,
            completed_at=datetime.now().isoformat()
        )
    
    def set_failed(self, job_id: str, error: str) -> Optional[Dict[str, Any]]:
        """Mark job as failed"""
        return self.update_job(
            job_id,
            status="failed",
            progress=0,
            error=error,
            completed_at=datetime.now().isoformat()
        )
    
    def delete_job(self, job_id: str) -> bool:
        """Delete job from manager"""
        if job_id in self.jobs:
            del self.jobs[job_id]
            self.logger.info(f"Deleted job: {job_id}")
            return True
        return False
    
    def cleanup_old_jobs(self, max_jobs: int = 100) -> None:
        """Clean up old jobs if exceeding max"""
        if len(self.jobs) > max_jobs:
            # Remove oldest completed jobs
            completed_jobs = [
                (jid, job) for jid, job in self.jobs.items()
                if job["status"] in ["completed", "failed"]
            ]
            
            if completed_jobs:
                # Sort by completion time
                completed_jobs.sort(
                    key=lambda x: x[1].get("completed_at", ""),
                    reverse=True
                )
                
                # Remove oldest half
                for jid, _ in completed_jobs[len(completed_jobs)//2:]:
                    self.delete_job(jid)
                    self.logger.info(f"Cleaned up old job: {jid}")


# Create global job manager instance
job_manager = JobManager()
