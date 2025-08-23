import re
from urllib.parse import urlparse

class URLValidator:
    """Validator for Facebook URLs"""
    
    FACEBOOK_URL_PATTERNS = [
        # Standard video URLs
        r'https?://(?:www\.|web\.)?facebook\.com/watch/?\?v=\d+',
        r'https?://(?:www\.|web\.)?facebook\.com/.*?/videos/\d+',
        r'https?://(?:www\.|web\.)?facebook\.com/video\.php\?v=\d+',
        # Short URLs
        r'https?://fb\.watch/[a-zA-Z0-9_-]+/?',
        # Reels
        r'https?://(?:www\.|web\.)?facebook\.com/reel/\d+',
        # Posts with videos
        r'https?://(?:www\.|web\.)?facebook\.com/.+/posts/\d+',
        # Share URLs
        r'https?://(?:www\.|web\.)?facebook\.com/share/v/[a-zA-Z0-9_-]+/?',
        r'https?://(?:www\.|web\.)?facebook\.com/share/r/[a-zA-Z0-9_-]+/?',
        # Mobile URLs
        r'https?://m\.facebook\.com/.*',
        # General Facebook video patterns (more flexible)
        r'https?://(?:www\.|web\.|m\.)?facebook\.com/.*/.*',
    ]
    
    @classmethod
    def is_valid_facebook_url(cls, url: str) -> bool:
        """Check if URL is a valid Facebook video URL"""
        if not url:
            return False
            
        # Parse URL to ensure it's properly formatted
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False
        except Exception:
            return False
        
        # Check against Facebook URL patterns
        for pattern in cls.FACEBOOK_URL_PATTERNS:
            if re.match(pattern, url, re.IGNORECASE):
                return True
                
        return False
    
    @classmethod
    def normalize_url(cls, url: str) -> str:
        """Normalize Facebook URL for consistent processing"""
        # Remove tracking parameters and normalize
        if 'facebook.com' in url or 'fb.watch' in url:
            # Remove common tracking parameters
            url = re.sub(r'[&?](fbclid|ref|source|__tn__|__cft__|hash)=[^&]*', '', url)
            # Clean up any trailing & or ?
            url = re.sub(r'[&?]$', '', url)
            
            # Normalize web.facebook.com to www.facebook.com for yt-dlp compatibility
            url = url.replace('web.facebook.com', 'www.facebook.com')
            url = url.replace('m.facebook.com', 'www.facebook.com')
            
        return url