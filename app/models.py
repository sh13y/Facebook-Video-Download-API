from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any
from enum import Enum

class VideoQuality(str, Enum):
    BEST = "best"
    WORST = "worst"
    P360 = "360p"
    P720 = "720p"
    P1080 = "1080p"

class VideoDownloadRequest(BaseModel):
    url: HttpUrl
    quality: Optional[VideoQuality] = VideoQuality.BEST
    
    class Config:
        schema_extra = {
            "example": {
                "url": "https://www.facebook.com/watch/?v=1234567890",
                "quality": "720p"
            }
        }

class VideoInfo(BaseModel):
    title: str
    duration: Optional[float] = None  # Changed from int to float to handle fractional durations
    thumbnail: Optional[str] = None
    uploader: Optional[str] = None
    view_count: Optional[int] = None
    upload_date: Optional[str] = None

class VideoFormat(BaseModel):
    quality: str
    format_id: str
    ext: str
    filesize: Optional[int] = None
    url: str

class VideoDownloadResponse(BaseModel):
    status: str
    message: Optional[str] = None
    video_info: Optional[VideoInfo] = None
    download_url: Optional[str] = None
    available_formats: Optional[List[VideoFormat]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "video_info": {
                    "title": "Amazing Facebook Video",
                    "duration": 120,
                    "thumbnail": "https://example.com/thumb.jpg",
                    "uploader": "John Doe"
                },
                "download_url": "https://video-cdn.facebook.com/video.mp4",
                "available_formats": [
                    {
                        "quality": "720p",
                        "format_id": "720p",
                        "ext": "mp4",
                        "url": "https://video-cdn.facebook.com/720p.mp4"
                    }
                ]
            }
        }

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    error_code: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "status": "error",
                "message": "Invalid Facebook URL provided",
                "error_code": "INVALID_URL"
            }
        }