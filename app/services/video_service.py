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
            'quiet': True,
            'no_warnings': False,
            'extractaudio': False,
            'audioformat': 'mp3',
            'outtmpl': '/tmp/%(title)s.%(ext)s',
            'retries': 5,  # Increased retries for redirect issues
            'fragment_retries': 5,
            'ignoreerrors': False,
            'no_check_certificate': True,
            # Handle redirects and cookies better
            'cookiefile': None,
            'extract_flat': False,
            # Add user agent to avoid blocking
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
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
        
        # Special handling for fb.watch URLs - try to resolve redirects
        if 'fb.watch' in normalized_url:
            normalized_url = await self._resolve_fb_watch_url(normalized_url)
        
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
    
    async def _resolve_fb_watch_url(self, url: str) -> str:
        """Resolve fb.watch URLs to full Facebook URLs with multiple redirect handling"""
        import aiohttp
        
        try:
            timeout = aiohttp.ClientTimeout(total=15)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                current_url = url
                max_redirects = 5
                redirect_count = 0
                
                while redirect_count < max_redirects:
                    try:
                        async with session.get(
                            current_url, 
                            allow_redirects=False,
                            headers=headers
                        ) as response:
                            # If it's a redirect response
                            if response.status in [301, 302, 303, 307, 308]:
                                redirect_url = response.headers.get('Location')
                                if redirect_url:
                                    # Handle relative redirects
                                    if redirect_url.startswith('/'):
                                        from urllib.parse import urljoin
                                        redirect_url = urljoin(current_url, redirect_url)
                                    
                                    # Check if we got a Facebook URL
                                    if 'facebook.com' in redirect_url:
                                        logger.info(f"Resolved fb.watch URL: {url} -> {redirect_url}")
                                        return redirect_url
                                    
                                    current_url = redirect_url
                                    redirect_count += 1
                                else:
                                    break
                            else:
                                # No more redirects, check if current URL is Facebook
                                if 'facebook.com' in current_url:
                                    return current_url
                                break
                    except Exception as e:
                        logger.warning(f"Error during redirect {redirect_count}: {str(e)}")
                        break
                
                # If we couldn't resolve to a facebook.com URL, return original
                logger.warning(f"Could not resolve fb.watch URL to facebook.com: {url}")
                return url
                
        except Exception as e:
            logger.warning(f"Could not resolve fb.watch URL: {str(e)}, using original")
            return url
    
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
        
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                # Extract video information
                info = ydl.extract_info(url, download=False)
                
                if not info:
                    raise ValueError("No video information found")
                
                return self._process_video_info(info)
                
        except yt_dlp.DownloadError as e:
            error_msg = str(e)
            if "redirect loop" in error_msg.lower() or "redirect" in error_msg.lower():
                if 'fb.watch' in url:
                    raise ValueError("fb.watch URL couldn't be processed. Please try: 1) Open the video on Facebook, 2) Copy the full facebook.com URL from the address bar, 3) Use that URL instead.")
                else:
                    raise ValueError("Video URL has redirect issues. Try copying the direct Facebook video URL.")
            elif "private" in error_msg.lower() or "not available" in error_msg.lower():
                raise ValueError("This video is private or not available for download.")
            elif "age" in error_msg.lower():
                raise ValueError("This video has age restrictions and cannot be downloaded.")
            else:
                raise ValueError(f"Could not extract video: {error_msg}")
        except Exception as e:
            error_msg = str(e)
            if "302" in error_msg or "redirect" in error_msg.lower():
                if 'fb.watch' in url:
                    raise ValueError("fb.watch URL needs the full Facebook URL. Please: 1) Open the video on Facebook, 2) Copy the complete facebook.com URL, 3) Try again.")
                else:
                    raise ValueError("URL redirect issue. Please try using the direct Facebook video URL.")
            else:
                raise ValueError(f"Unexpected error: {error_msg}")
    
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