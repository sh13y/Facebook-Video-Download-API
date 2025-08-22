import re
from urllib.parse import urlparse

class URLValidator:
    """Validator for Facebook URLs"""
    
    FACEBOOK_URL_PATTERNS = [
        r'https?://(?:www\.)?facebook\.com/watch/?\?v=\d+',
        r'https?://(?:www\.)?facebook\.com/.*?/videos/\d+',
        r'https?://(?:www\.)?facebook\.com/video\.php\?v=\d+',
        r'https?://fb\.watch/[a-zA-Z0-9_-]+',
        r'https?://(?:www\.)?facebook\.com/reel/\d+',
        r'https?://(?:www\.)?facebook\.com/.+/posts/\d+',
        r'https?://(?:www\.)?facebook\.com/share/v/[a-zA-Z0-9_-]+/?',
        r'https?://(?:www\.)?facebook\.com/share/r/[a-zA-Z0-9_-]+/?'
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
        if 'facebook.com' in url:
            # Remove common tracking parameters
            url = re.sub(r'[&?](fbclid|ref|source)=[^&]*', '', url)
            # Clean up any trailing & or ?
            url = re.sub(r'[&?]$', '', url)
            
        return url