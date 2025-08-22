from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
from contextlib import asynccontextmanager

from app.config import settings
from app.models import (
    VideoDownloadRequest, 
    VideoDownloadResponse, 
    ErrorResponse,
    VideoQuality
)
from app.services.video_service import video_service
from app.utils.rate_limiter import check_rate_limit

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Facebook Video Downloader API starting up...")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Rate limiting: {settings.RATE_LIMIT_REQUESTS} requests per {settings.RATE_LIMIT_WINDOW}s")
    yield
    # Shutdown
    logger.info("📱 Facebook Video Downloader API shutting down...")

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error occurred",
            "error_code": "INTERNAL_ERROR"
        }
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.API_VERSION,
        "service": "Facebook Video Downloader API"
    }

# Main video download endpoint
@app.post("/download", response_model=VideoDownloadResponse)
async def download_video(
    request: VideoDownloadRequest,
    _: None = Depends(check_rate_limit)
):
    """
    Download Facebook video and get direct download link
    
    - **url**: Facebook video URL (required)
    - **quality**: Preferred video quality (optional, default: best)
    
    Returns video information and direct download URL.
    """
    
    try:
        logger.info(f"Processing video download request: {request.url}")
        
        # Extract video information
        result = await video_service.get_video_info(
            str(request.url), 
            request.quality
        )
        
        response = VideoDownloadResponse(
            status="success",
            video_info=result['video_info'],
            download_url=result['download_url'],
            available_formats=result['available_formats']
        )
        
        logger.info(f"Successfully processed video: {result['video_info'].title}")
        return response
        
    except ValueError as e:
        logger.warning(f"Invalid request: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": str(e),
                "error_code": "INVALID_REQUEST"
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": "Failed to process video",
                "error_code": "PROCESSING_ERROR"
            }
        )

# Get video info without download
@app.post("/info", response_model=VideoDownloadResponse)
async def get_video_info(
    request: VideoDownloadRequest,
    _: None = Depends(check_rate_limit)
):
    """
    Get Facebook video information without download URL
    
    - **url**: Facebook video URL (required)
    
    Returns video metadata only.
    """
    
    try:
        logger.info(f"Processing video info request: {request.url}")
        
        result = await video_service.get_video_info(
            str(request.url), 
            request.quality
        )
        
        response = VideoDownloadResponse(
            status="success",
            video_info=result['video_info'],
            available_formats=result['available_formats']
        )
        
        logger.info(f"Successfully retrieved info: {result['video_info'].title}")
        return response
        
    except ValueError as e:
        logger.warning(f"Invalid request: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": str(e),
                "error_code": "INVALID_REQUEST"
            }
        )

# Get supported quality options
@app.get("/qualities")
async def get_supported_qualities():
    """Get list of supported video qualities"""
    return {
        "status": "success",
        "qualities": [quality.value for quality in VideoQuality],
        "descriptions": {
            "best": "Best available quality",
            "worst": "Worst available quality", 
            "360p": "360p resolution",
            "720p": "720p resolution",
            "1080p": "1080p resolution"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.DEBUG
    )