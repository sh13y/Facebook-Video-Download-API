import os
from typing import List

class Settings:
    # API Configuration
    API_TITLE = "Facebook Video Downloader API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "A production-ready API for downloading Facebook videos"
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "10"))
    RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:5500",  # VS Code Live Server
        "https://yourdomain.com",
        "*"  # Allow all origins for demonstration purposes (not recommended for production)
    ]
    
    # Video Download Settings
    MAX_VIDEO_SIZE_MB = int(os.getenv("MAX_VIDEO_SIZE_MB", "500"))
    DOWNLOAD_TIMEOUT = int(os.getenv("DOWNLOAD_TIMEOUT", "30"))
    
    # Environment
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))

settings = Settings()