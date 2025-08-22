# 🎥 Facebook Video Downloader API

A production-ready REST API for downloading Facebook videos built with FastAPI and yt-dlp.

## ✨ Features

- **Fast & Reliable**: Built with FastAPI for high performance
- **Multiple Quality Options**: Support for 360p, 720p, 1080p, best, and worst quality
- **Rate Limiting**: Built-in protection against abuse
- **Error Handling**: Comprehensive error handling and validation
- **Docker Support**: Easy deployment with Docker
- **Production Ready**: Logging, health checks, and monitoring
- **Wide URL Support**: Works with all Facebook video URL formats, including the new share/v/ format

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- ffmpeg (for video processing)
- yt-dlp 2025.8.20 or later (for supporting all URL formats)

### Local Development

1. **Clone and setup**:
```bash
git clone <your-repo>
cd facebook-video-downloader
pip install -r requirements.txt
```

2. **Install ffmpeg**:
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

3. **Run the API**:
```bash
# Development mode
python -m app.main

# Or with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. **Test the API**:
```bash
curl -X POST "http://localhost:8000/download" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.facebook.com/share/v/1C6EwSc49J/", "quality": "best"}'
```

### Docker Deployment

1. **Build and run with Docker**:
```bash
# Build image
docker build -t facebook-video-api .

# Run container
docker run -p 8000:8000 facebook-video-api
```

2. **Or use Docker Compose**:
```bash
docker-compose up -d
```

## 📖 API Documentation

### Online Documentation
A detailed API documentation is available as a GitHub Pages site at:
```
https://your-github-username.github.io/facebook-video-downloader-api/
```

### Browser Interface
A browser-based interface is available for easy access to the API:
```
https://your-github-username.github.io/facebook-video-downloader-api/browser.html
```

### Direct URI Access
You can create shareable links with URL parameters that can be used directly in a browser:
```
https://your-github-username.github.io/facebook-video-downloader-api/direct.html?url=https://www.facebook.com/share/v/1C6EwSc49J/&quality=best&api=http://localhost:8000
```

You can also use direct browser URI access for the following GET endpoints:
- Health check: `http://localhost:8000/health`
- Quality options: `http://localhost:8000/qualities`

### Base URL
```
http://localhost:8000
```

### Supported URL Formats

The API supports the following Facebook video URL formats:

- `https://www.facebook.com/watch/?v=1234567890`
- `https://www.facebook.com/username/videos/1234567890`
- `https://www.facebook.com/video.php?v=1234567890`
- `https://fb.watch/abcdef123`
- `https://www.facebook.com/reel/1234567890`
- `https://www.facebook.com/username/posts/1234567890`
- `https://www.facebook.com/share/v/1C6EwSc49J/` (New format)

### Endpoints

#### `POST /download`
Download Facebook video and get direct download link.

**Request Body**:
```json
{
  "url": "https://www.facebook.com/watch/?v=1234567890",
  "quality": "720p"
}
```

**Response**:
```json
{
  "status": "success",
  "video_info": {
    "title": "Amazing Facebook Video",
    "duration": 25.533,
    "thumbnail": "https://example.com/thumb.jpg",
    "uploader": "John Doe",
    "view_count": 1000,
    "upload_date": "20250816"
  },
  "download_url": "https://video-cdn.facebook.com/video.mp4",
  "available_formats": [
    {
      "quality": "720p",
      "format_id": "720p",
      "ext": "mp4",
      "filesize": 52428800,
      "url": "https://video-cdn.facebook.com/720p.mp4"
    }
  ]
}
```

#### `POST /info`
Get video information without download URL.

#### `GET /qualities`
Get supported video quality options.

#### `GET /health`
Health check endpoint.

### Quality Options

- `best` - Best available quality (default)
- `worst` - Worst available quality
- `360p` - 360p resolution
- `720p` - 720p resolution  
- `1080p` - 1080p resolution

### Error Responses

```json
{
  "status": "error",
  "message": "Invalid Facebook URL provided",
  "error_code": "INVALID_REQUEST"
}
```

## 🌐 Free Hosting Deployment

### Railway

1. **Connect GitHub repo to Railway**
2. **Set environment variables**:
   ```
   PORT=8000
   DEBUG=false
   RATE_LIMIT_REQUESTS=10
   ```
3. **Deploy automatically**

### Render

1. **Create new Web Service**
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**:
   ```
   DEBUG=false
   RATE_LIMIT_REQUESTS=10
   ```

### Heroku

1. **Create Procfile**:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. **Deploy**:
```bash
heroku create your-app-name
git push heroku main
```

## ⚙️ Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `False` | Enable debug mode |
| `HOST` | `0.0.0.0` | Host to bind to |
| `PORT` | `8000` | Port to listen on |
| `RATE_LIMIT_REQUESTS` | `10` | Max requests per window |
| `RATE_LIMIT_WINDOW` | `60` | Rate limit window (seconds) |
| `MAX_VIDEO_SIZE_MB` | `500` | Max video size limit |
| `DOWNLOAD_TIMEOUT` | `30` | Download timeout (seconds) |

## 🔒 Rate Limiting

- Default: 10 requests per 60 seconds per IP
- Configurable via environment variables
- Returns 429 status code when exceeded

## 🛠️ Development

### Project Structure
```
app/
├── main.py              # FastAPI application
├── models.py            # Pydantic models (with float duration support)
├── config.py            # Configuration settings
├── services/
│   └── video_service.py # Video download logic
└── utils/
    ├── rate_limiter.py  # Rate limiting
    └── validators.py    # URL validation (including new share/v/ format)
```

### Adding New Features

1. **Add models** in `models.py`
2. **Implement services** in `services/`
3. **Add endpoints** in `main.py`
4. **Update tests** and documentation

## ⚠️ Important Notes

- **Facebook's Terms**: Ensure compliance with Facebook's terms of service
- **Rate Limits**: Respect Facebook's rate limits to avoid blocking
- **Privacy**: Only download public videos you have permission to download
- **Legal**: Use responsibly and respect copyright laws

## 🐛 Troubleshooting

### Common Issues

1. **"No video found"**: Video may be private or URL invalid
2. **Rate limited**: Wait for rate limit window to reset
3. **Download fails**: Video may be too large or connection timeout
4. **"Requested format is not available"**: The requested quality is not available for this video. Try using "best" instead of a specific resolution.
5. **Fractional duration error**: Ensure your VideoInfo model allows float values for duration (fixed in current version)

### Logs

Check logs for detailed error information:
```bash
# Docker logs
docker logs <container-id>

# Local development
# Logs print to console
```

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Submit pull request

---

**⚠️ Disclaimer**: This tool is for educational purposes. Ensure you comply with Facebook's terms of service and respect copyright laws when downloading videos.