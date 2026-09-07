"""
Core Configuration Module
Loads environment variables and provides application settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Backend root directory (.../backend), independent of the process's current
# working directory. Anchoring paths here avoids "file not found" issues when
# the app is started from a different directory (e.g. via a process manager
# or a different deployment working directory).
BACKEND_ROOT = Path(__file__).parent.parent.parent

# Load .env file
env_path = BACKEND_ROOT / ".env"
load_dotenv(env_path)


class Settings:
    """Application settings loaded from environment variables"""

    # API Configuration
    API_TITLE = "EngiSummary Backend API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "Engineering Drawing Data Extraction and Summary Generation System"
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # Gemini Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    # Frontend Configuration
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # File Configuration
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "25"))
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

    # Resolve upload/output/temp dirs as absolute paths anchored to the backend
    # root. If UPLOAD_DIR/OUTPUT_DIR are given as absolute paths in .env, those
    # are respected as-is; otherwise they are resolved relative to BACKEND_ROOT
    # (not the process cwd), so file paths stay correct no matter where the
    # server process is launched from.
    UPLOAD_DIR = str((BACKEND_ROOT / os.getenv("UPLOAD_DIR", "uploads")).resolve()) \
        if not os.path.isabs(os.getenv("UPLOAD_DIR", "uploads")) else os.getenv("UPLOAD_DIR")
    OUTPUT_DIR = str((BACKEND_ROOT / os.getenv("OUTPUT_DIR", "outputs")).resolve()) \
        if not os.path.isabs(os.getenv("OUTPUT_DIR", "outputs")) else os.getenv("OUTPUT_DIR")
    TEMP_DIR = str((BACKEND_ROOT / "app" / "temp").resolve())
    
    # Material Properties
    STEEL_DENSITY = float(os.getenv("STEEL_DENSITY", "7850"))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # SMTP / Email Configuration (used to send generated PDFs)
    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM = os.getenv("SMTP_FROM", os.getenv("SMTP_USER", ""))
    SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
    SMTP_USE_SSL = os.getenv("SMTP_USE_SSL", "false").lower() == "true"
    
    # Ensure directories exist
    @staticmethod
    def ensure_directories():
        """Create required directories if they don't exist"""
        for directory in [Settings.UPLOAD_DIR, Settings.OUTPUT_DIR, Settings.TEMP_DIR]:
            Path(directory).mkdir(parents=True, exist_ok=True)


# Create settings instance
settings = Settings()

# Ensure directories exist on import
settings.ensure_directories()
