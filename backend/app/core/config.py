"""
Core Configuration Module
Loads environment variables and provides application settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent.parent.parent / ".env"
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
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "outputs")
    TEMP_DIR = "app/temp"
    
    # Material Properties
    STEEL_DENSITY = float(os.getenv("STEEL_DENSITY", "7850"))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
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
