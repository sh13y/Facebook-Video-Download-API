import yt_dlp
import asyncio
import logging
from typing import Dict, List, Optional, Any
from app.models import VideoInfo, VideoFormat, VideoQuality
from app.utils.validators import URLValidator
from app.config import settings

logger = logging.getLogger(__name__)

class VideoDownloadService:
    """Service for downloading Facebook videos using yt-dlp"""
    
    def __init__(self):
        self.ydl_opts = {
            'quiet': not settings.DEBUG,
            'no_warnings': not settings.DEBUG,
            'extract_flat': False,
            'socket_timeout': settings.DOWNLOAD_TIMEOUT,
            'retries': 3,
            'fragment_retries': 3,
            'ignoreerrors': False,
            'no_check_certificate': True,
            # Ensure proper audio merging for Facebook videos
            'format': 'best[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }
    
    async def get_video_info(self, url: str, quality: VideoQuality = VideoQuality.BEST) -> Dict[str, Any]:
        """Extract video information and download URLs"""
        
        # Validate URL
        if not URLValidator.is_valid_facebook_url(url):
            raise ValueError("Invalid Facebook URL provided")
        
        # Normalize URL
        normalized_url = URLValidator.normalize_url(url)
        
        try:
            # Run yt-dlp in a thread to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                self._extract_info, 
                normalized_url, 
                quality
            )
            return result
            
        except Exception as e:
            logger.error(f"Error extracting video info: {str(e)}")
            raise ValueError(f"Failed to extract video information: {str(e)}")
    
    def _extract_info(self, url: str, quality: VideoQuality) -> Dict[str, Any]:
        """Extract video information using yt-dlp (runs in thread)"""
        
        # Configure yt-dlp options based on quality
        opts = self.ydl_opts.copy()
        
        # Set format selector based on quality - with proper audio merging
        if quality == VideoQuality.BEST:
            opts['format'] = 'best[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        elif quality == VideoQuality.WORST:
            opts['format'] = 'worst[ext=mp4]+bestaudio[ext=m4a]/worst[ext=mp4]/worst'
        elif quality == VideoQuality.P360:
            opts['format'] = 'best[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360][ext=mp4]/best[height<=360]'
        elif quality == VideoQuality.P720:
            opts['format'] = 'best[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best[height<=720]'
        elif quality == VideoQuality.P1080:
            opts['format'] = 'best[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best[height<=1080]'
        
        with yt_dlp.YoutubeDL(opts) as ydl:
            # Extract video information
            info = ydl.extract_info(url, download=False)
            
            if not info:
                raise ValueError("No video information found")
            
            return self._process_video_info(info)
    
    def _process_video_info(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """Process and structure video information"""
        
        # Extract basic video info
        video_info = VideoInfo(
            title=info.get('title', 'Unknown Title'),
            duration=info.get('duration'),
            thumbnail=info.get('thumbnail'),
            uploader=info.get('uploader'),
            view_count=info.get('view_count'),
            upload_date=info.get('upload_date')
        )
        
        # Get the selected format URL
        download_url = info.get('url')
        
        # Extract available formats
        available_formats = []
        formats = info.get('formats', [])
        
        for fmt in formats:
            if fmt.get('url') and fmt.get('height'):
                video_format = VideoFormat(
                    quality=f"{fmt.get('height')}p" if fmt.get('height') else "unknown",
                    format_id=fmt.get('format_id', ''),
                    ext=fmt.get('ext', 'mp4'),
                    filesize=fmt.get('filesize'),
                    url=fmt.get('url')
                )
                available_formats.append(video_format)
        
        # Sort formats by quality (highest first)
        available_formats.sort(
            key=lambda x: int(x.quality.replace('p', '')) if x.quality.replace('p', '').isdigit() else 0,
            reverse=True
        )
        
        return {
            'video_info': video_info,
            'download_url': download_url,
            'available_formats': available_formats[:10]  # Limit to top 10 formats
        }

# Global service instance
video_service = VideoDownloadService()