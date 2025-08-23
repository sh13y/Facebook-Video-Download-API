# 🎥 Facebook Video Downloader API

[![Made in Ceylon](https://img.shields.io/badge/Made%20in-Ceylon%20🇱🇰-ff6b35?style=for-the-badge)](https://github.com/sh13y)
[![License](https://img.shields.io/badge/License-WPFTL-blue.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ed?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

A production-ready REST API and web interface for downloading Facebook videos with high-quality audio support. Built with FastAPI and yt-dlp, featuring a modern responsive web GUI.

## ✨ Features

- **🚀 Fast & Reliable**: Built with FastAPI for high performance
- **🎵 Audio Support**: Automatic video+audio merging for Facebook's DASH streams  
- **📱 Responsive GUI**: Modern web interface with Tailwind CSS
- **🔧 Multiple Quality Options**: Support for 360p, 720p, 1080p, best, and worst quality
- **🛡️ Rate Limiting**: Built-in protection against abuse
- **📊 Comprehensive Logging**: Error handling and monitoring
- **🐳 Docker Support**: Easy deployment with Docker
- **🌐 Wide URL Support**: Works with all Facebook video URL formats

## 🌟 Live Demo

**Deploy your own instance on:**
- [Railway](https://railway.app) - `https://your-app.railway.app`
- [Render](https://render.com) - `https://your-app.onrender.com`
- [Fly.io](https://fly.io) - `https://your-app.fly.dev`

**Quick Deploy Links:**
- [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template)
- [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ 
- ffmpeg (for video processing)
- yt-dlp 2025.8.20+ (automatically installed)

### 🐳 Docker Deployment (Recommended)

```bash
# Clone the repository
git clone https://github.com/sh13y/Facebook-Video-Download-API.git
cd Facebook-Video-Download-API

# Run with Docker Compose
docker-compose up -d

# Access the application
# Web Interface: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

### 🔧 Local Development

```bash
# Clone and setup
git clone https://github.com/sh13y/Facebook-Video-Download-API.git
cd Facebook-Video-Download-API
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install ffmpeg
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows - Download from https://ffmpeg.org/download.html

# Run the application
python -m app.main
# or
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 🌐 Free Hosting Deployment

#### **Render** ⭐ (Recommended for FastAPI)
1. Go to [Render.com](https://render.com) → New Web Service
2. Connect GitHub repo
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Set environment variables: `DEBUG=false`
6. Deploy → Live at: `https://your-app.onrender.com`

#### **Railway**
1. Push code to GitHub
2. Go to [Railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select your repo and deploy
4. Set environment variables: `DEBUG=false`, `RATE_LIMIT_REQUESTS=10`
5. Your app will be live at: `https://your-app.railway.app`

#### **Fly.io** (Docker)
```bash
# Install flyctl CLI
curl -L https://fly.io/install.sh | sh

# Deploy
flyctl launch
flyctl deploy
```

#### **Netlify** (Serverless Functions)
```bash
# Using Netlify CLI
npm install -g netlify-cli
netlify login
netlify deploy --prod --dir=static --functions=netlify/functions
```
**Note**: Limited to 10-second execution time, may not work for large videos.

**🎯 Recommendation**: Use Railway or Render for full functionality, Netlify for frontend-only deployments.

## 📖 Usage

### Web Interface

1. Open `http://localhost:8000` in your browser
2. Paste a Facebook video URL
3. Select your preferred quality
4. Click "Download Video"
5. Download starts automatically

### API Usage

#### Download Video

```bash
curl -X POST "http://localhost:8000/download" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.facebook.com/share/v/17GS54EKBN/",
    "quality": "best"
  }'
```

#### Response

```json
{
  "status": "success",
  "video_info": {
    "title": "Video Title",
    "duration": 828,
    "thumbnail": "https://...",
    "uploader": "Channel Name", 
    "view_count": 1000000
  },
  "download_url": "https://direct-download-link.mp4",
  "available_formats": [...]
}
```

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web interface |
| POST | `/download` | Download video with URL |
| POST | `/info` | Get video info only |
| GET | `/qualities` | List supported qualities |
| GET | `/health` | Health check |
| GET | `/docs` | API documentation |

## ⚙️ Configuration

Environment variables:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Rate Limiting
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60

# Download Settings
DOWNLOAD_TIMEOUT=30
```

## 🛠️ Supported Video URLs

- `https://www.facebook.com/user/videos/123456789/`
- `https://www.facebook.com/share/v/abc123/`
- `https://www.facebook.com/watch/?v=123456789`
- `https://fb.watch/abc123/`

## 🐛 Troubleshooting

### Common Issues & Solutions

#### ❌ **Problem**: Video downloads without audio

**💡 Solution**: This was a major issue we solved! Facebook uses DASH streaming which separates video and audio streams.

**Technical Details**:
- Facebook serves video and audio as separate streams
- Our solution automatically detects and merges both streams using ffmpeg
- Updated format selector: `best[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best`

**Fix Applied**:
```python
# Before (video only)
'format': 'best[ext=mp4]/best'

# After (video + audio merged)  
'format': 'best[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
```

#### ❌ **Problem**: "No video formats found" error

**💡 Solution**: Update yt-dlp to the latest version

```bash
pip install --upgrade yt-dlp
```

#### ❌ **Problem**: ffmpeg not found

**💡 Solution**: Install ffmpeg on your system

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS  
brew install ffmpeg

# Windows - Download from https://ffmpeg.org/
```

#### ❌ **Problem**: Rate limit exceeded

**💡 Solution**: Wait for the rate limit window to reset (default: 60 seconds)

#### ❌ **Problem**: Invalid Facebook URL

**💡 Solution**: Ensure the URL is a direct Facebook video link, not a post link

### Debug Mode

Enable debug mode for detailed logging:

```bash
export DEBUG=true
python -m app.main
```

## 🏗️ Architecture

```
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── models.py            # Pydantic models
│   ├── services/
│   │   └── video_service.py # Video download logic
│   └── utils/
│       ├── rate_limiter.py  # Rate limiting
│       └── validators.py    # URL validation
├── static/
│   ├── index.html          # Web interface
│   └── script.js           # Frontend JavaScript
├── docker-compose.yml      # Docker deployment
├── Dockerfile             # Container configuration
└── requirements.txt       # Python dependencies
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under **WPFTL (WTFPL)** - see the [LICENSE](LICENSE) file for details.

**TL;DR**: Do whatever you want with this code! 🎉

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The amazing tool that powers video extraction
- [FastAPI](https://fastapi.tiangolo.com/) - For the incredible web framework
- [Tailwind CSS](https://tailwindcss.com/) - For the beautiful UI components

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/sh13y/Facebook-Video-Download-API/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/sh13y/Facebook-Video-Download-API/discussions)
- 📧 **Contact**: [GitHub Profile](https://github.com/sh13y)

## 🏆 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=sh13y/Facebook-Video-Download-API&type=Date)](https://star-history.com/#sh13y/Facebook-Video-Download-API&Date)

---

<div align="center">

**Made in Ceylon 🇱🇰 with ❤️ by [sh13y](https://github.com/sh13y)**

*If you found this project helpful, please give it a ⭐!*

</div>