# Facebook Video Downloader API

[![License](https://img.shields.io/badge/License-WTFPL-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://docker.com)
[![Live Demo](https://img.shields.io/badge/Demo-Live-success.svg)](https://fdown.isuru.eu.org)

A production-ready REST API and web interface for downloading Facebook videos with audio support. Built with FastAPI, yt-dlp, and modern web technologies for reliable video extraction and processing.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Live Demo](#live-demo)
- [Technical Architecture](#technical-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Project Evolution](#project-evolution)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project provides a robust solution for downloading Facebook videos programmatically. The system handles Facebook's complex video streaming formats, including DASH streams that require audio and video merging, making it suitable for both developers and end-users.

### Key Problem Solved

Facebook videos often use separate audio and video streams (DASH format), making direct downloads challenging. This API automatically detects and merges these streams using FFmpeg, ensuring downloaded videos include both audio and video components.

## Features

### Core Functionality
- **Video Download**: Extract and download Facebook videos in multiple quality options
- **Audio Merging**: Automatic handling of DASH streams with audio/video synchronization
- **Format Support**: MP4 output with quality selection (360p, 720p, 1080p, best, worst)
- **URL Flexibility**: Support for various Facebook URL formats including fb.watch short links

### Technical Features
- **RESTful API**: Clean HTTP API with comprehensive endpoint documentation
- **Rate Limiting**: Built-in protection against abuse (10 requests per 60 seconds per IP)
- **Error Handling**: Detailed error responses with actionable user guidance
- **Web Interface**: Responsive frontend for non-technical users
- **Docker Support**: Containerized deployment with all dependencies included

### Quality Options
- `best`: Highest available quality with audio
- `worst`: Lowest quality for faster downloads
- `360p`, `720p`, `1080p`: Specific resolution targets
- Automatic fallback to best available quality if requested resolution unavailable

## Live Demo

**Web Interface**: [https://fdown.isuru.eu.org](https://fdown.isuru.eu.org)

**API Documentation**: [https://fdown.isuru.eu.org/docs](https://fdown.isuru.eu.org/docs)

**GitHub Pages**: [https://sh13y.github.io/Facebook-Video-Download-API](https://sh13y.github.io/Facebook-Video-Download-API)

### Quick Test
```bash
curl -X POST "https://fdown.isuru.eu.org/info" \
     -H "Content-Type: application/json" \
     -d '{"url": "YOUR_FACEBOOK_VIDEO_URL"}'
```

### Mobile Demo

<div align="center">

![Mobile Demo](assets/mobile-demo.gif)

*Mobile interface demonstration: Paste Facebook video URL → Select quality → Download*

</div>

## Technical Architecture

### Backend Stack
- **FastAPI**: Modern Python web framework for API development
- **yt-dlp**: Robust video extraction library with Facebook support
- **FFmpeg**: Video processing for stream merging and format conversion
- **Pydantic**: Data validation and serialization
- **aiohttp**: Asynchronous HTTP client for URL resolution

### Frontend Stack
- **Vanilla JavaScript**: Lightweight, dependency-free frontend
- **Tailwind CSS**: Utility-first CSS framework for responsive design
- **Responsive Design**: Mobile-first approach supporting all screen sizes

### Infrastructure
- **Docker**: Containerization with multi-stage builds
- **Render**: Production hosting with automatic deployments
- **GitHub Actions**: CI/CD pipeline for documentation and testing

## Installation

### Prerequisites
- Python 3.11 or higher
- FFmpeg installed on system
- Git for cloning the repository

### Method 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/sh13y/Facebook-Video-Download-API.git
cd Facebook-Video-Download-API

# Build and run with Docker Compose
docker-compose up -d

# Access the application
# Web Interface: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

### Method 2: Local Development

```bash
# Clone the repository
git clone https://github.com/sh13y/Facebook-Video-Download-API.git
cd Facebook-Video-Download-API

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### FFmpeg Installation

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [FFmpeg official website](https://ffmpeg.org/download.html) or use package managers like Chocolatey.

## Usage

### Web Interface

1. Navigate to the web interface at `http://localhost:8000`
2. Paste a Facebook video URL in the input field
3. Select desired video quality
4. Click "Download Video" to process and download

### API Usage

#### Get Video Information
```bash
curl -X POST "http://localhost:8000/info" \
     -H "Content-Type: application/json" \
     -d '{
       "url": "https://www.facebook.com/watch/?v=1234567890",
       "quality": "best"
     }'
```

#### Download Video
```bash
curl -X POST "http://localhost:8000/download" \
     -H "Content-Type: application/json" \
     -d '{
       "url": "https://www.facebook.com/watch/?v=1234567890",
       "quality": "720p"
     }'
```

### Supported URL Formats

The API accepts various Facebook URL formats:

```
https://www.facebook.com/watch/?v=1234567890
https://facebook.com/username/videos/1234567890
https://m.facebook.com/watch/?v=1234567890
https://fb.watch/ABC123/
https://www.facebook.com/reel/1234567890
```

**Note**: For fb.watch URLs, if processing fails, copy the full Facebook URL after the redirect for better reliability.

## API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web interface |
| GET | `/health` | Health check |
| POST | `/info` | Get video information |
| POST | `/download` | Download video |
| GET | `/qualities` | List supported qualities |
| GET | `/stream/{video_id}` | Stream video file |

### Response Format

**Success Response:**
```json
{
  "status": "success",
  "video_info": {
    "title": "Video Title",
    "duration": 120,
    "thumbnail": "https://example.com/thumb.jpg",
    "uploader": "Page Name",
    "view_count": 1000,
    "upload_date": "20240101"
  },
  "download_url": "https://example.com/video.mp4",
  "available_formats": [...]
}
```

**Error Response:**
```json
{
  "status": "error",
  "message": "Invalid Facebook URL provided",
  "error_code": "INVALID_REQUEST"
}
```

### Rate Limiting

- **Limit**: 10 requests per 60 seconds per IP address
- **Headers**: Rate limit information included in response headers
- **Behavior**: Returns 429 status code when limit exceeded

## Deployment

### Production Deployment on Render

1. Fork this repository
2. Connect your GitHub account to Render
3. Create a new Web Service
4. Connect your forked repository
5. Render will automatically deploy using the included `render.yaml`

### Environment Variables

```bash
# Optional: Set debug mode
DEBUG=false

# Optional: Custom port
PORT=8000
```

### Docker Deployment

```bash
# Build the image
docker build -t facebook-video-downloader .

# Run the container
docker run -p 8000:8000 facebook-video-downloader
```

## Project Evolution

This project evolved through several phases, each addressing specific technical challenges and user needs:

### Phase 1: Core Functionality
**Challenge**: Basic video extraction without audio
- Implemented yt-dlp integration for Facebook video extraction
- Discovered Facebook's DASH stream architecture separating audio/video
- **Solution**: Integrated FFmpeg for automatic stream merging

### Phase 2: Web Interface Development
**Challenge**: Making the API accessible to non-technical users
- Developed responsive web interface using Tailwind CSS
- Implemented real-time feedback and error handling
- **Solution**: Progressive enhancement with mobile-first design

### Phase 3: URL Compatibility
**Challenge**: Supporting Facebook's diverse URL formats
- Researched Facebook's URL structure variations
- Implemented comprehensive regex patterns for URL validation
- **Solution**: Built URL normalization system handling redirects

### Phase 4: Production Readiness
**Challenge**: Deploying a reliable service for public use
- Implemented rate limiting and error handling
- Added comprehensive logging and monitoring
- **Solution**: Containerized deployment with auto-scaling capabilities

### Phase 5: Developer Experience
**Challenge**: Providing clear documentation and testing capabilities
- Created comprehensive API documentation
- Built interactive testing interface
- **Solution**: Multi-format documentation with live examples

### Current Status

| Component | Status | Description |
|-----------|--------|-------------|
| **Core API** | Production Ready | Stable video extraction with error handling |
| **Web Interface** | Production Ready | Responsive design supporting all devices |
| **Documentation** | Complete | API docs, deployment guides, troubleshooting |
| **Deployment** | Automated | Docker containers with CI/CD pipeline |
| **Testing** | Interactive | Live API testing through documentation |

## Contributing

Contributions are welcome! Please read our contributing guidelines:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python -m pytest

# Run with auto-reload for development
uvicorn app.main:app --reload
```

### Code Style

- Follow PEP 8 for Python code
- Use type hints for all function parameters and return values
- Write descriptive commit messages
- Include tests for new features

## License

This project is licensed under the WTFPL (Do What The F*** You Want To Public License) - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)**: Robust video extraction library
- **[FastAPI](https://fastapi.tiangolo.com/)**: Modern Python web framework
- **[FFmpeg](https://ffmpeg.org/)**: Video processing capabilities
- **[Tailwind CSS](https://tailwindcss.com/)**: Utility-first CSS framework

---

**Built by [sh13y](https://github.com/sh13y)**

For questions, issues, or contributions, please visit the [GitHub repository](https://github.com/sh13y/Facebook-Video-Download-API).
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
## 📖 How To Use This Magic

### 🖥️ Web Interface (For Humans)

*"So simple, your grandma could use it!"*

1. **Visit** `http://localhost:8000` *(or your live demo)*
2. **Paste** that Facebook video URL you've been hoarding
3. **Pick** your quality *(360p for data-savers, 1080p for perfectionists)*
4. **Click** "Download Video" 
5. **Profit!** 💰 *(Well, more like... enjoy your video)*

### 🤖 API Usage (For Developers)

*"Because sometimes you need to download 1000 cat videos programmatically"*

#### Download a Video

```bash
curl -X POST "http://localhost:8000/download" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.facebook.com/share/v/17GS54EKBN/",
    "quality": "best"
  }'
```

#### What You Get Back

```json
{
  "status": "success",
  "video_info": {
    "title": "Cats Being Cats for 5 Minutes Straight",
    "duration": 300,
    "thumbnail": "https://beautiful-cat-thumbnail.jpg",
    "uploader": "CatLoversPro", 
    "view_count": 5000000
  },
  "download_url": "https://your-video-is-here.mp4",
  "available_formats": ["360p", "720p", "1080p"]
}
```

### 🎯 API Endpoints Reference

| 🌐 Method | 🛤️ Endpoint | 🎭 What It Does | 😎 Cool Factor |
|-----------|-------------|----------------|----------------|
| **GET** | `/` | Web interface | ⭐⭐⭐⭐⭐ |
| **POST** | `/download` | Download video | ⭐⭐⭐⭐⭐ |
| **POST** | `/info` | Just the facts, ma'am | ⭐⭐⭐⭐ |
| **GET** | `/qualities` | Available quality options | ⭐⭐⭐ |
| **GET** | `/health` | "Are you alive?" | ⭐⭐ |
| **GET** | `/docs` | Interactive API playground | ⭐⭐⭐⭐⭐ |

*Pro tip: The `/docs` endpoint is where the real fun happens - interactive API testing!* 🎮

## ⚙️ Configuration Wizardry

*"Tweak it 'til it's perfect!"*

Environment variables you can play with:

```env
# Server Settings (The Basics)
HOST=0.0.0.0              # Listen everywhere
PORT=8000                 # Your favorite port
DEBUG=false               # Keep it cool in production

# Rate Limiting (Anti-Spam Shield)
RATE_LIMIT_REQUESTS=10    # 10 requests...
RATE_LIMIT_WINDOW=60      # ...per minute (be nice!)

# Download Settings (The Good Stuff)
DOWNLOAD_TIMEOUT=30       # 30 seconds to download or bust
```

## 🛠️ Supported Facebook URLs

*"We speak all dialects of Facebook!"*

✅ **What Works:**
- `https://www.facebook.com/user/videos/123456789/`
- `https://www.facebook.com/share/v/abc123/`
- `https://www.facebook.com/watch/?v=123456789`
- `https://fb.watch/abc123/` *(The short and sweet ones)*

❌ **What Doesn't Work:**
- Private videos *(Sorry, no hacking here!)*
- Live streams *(They're... still live)*
- Videos from pages you can't access *(Facebook's rules, not ours)*

## 🐛 When Things Go Wrong (Troubleshooting)

*"Every developer's favorite section!"* 😅

### 🔇 **Problem**: "My video has no sound!"

**🎯 Solution**: We already fixed this! Facebook's sneaky DASH streaming separates video and audio.

**What We Did**:
- **Before**: Videos came out mute (like a sad mime)
- **After**: Perfect video+audio harmony (like a beautiful symphony)
- **Magic**: Our format selector automatically merges both streams

```python
# The hero code that saved the day:
'format': 'best[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
```

### 📵 **Problem**: "No video formats found"

**🎯 Solution**: Your yt-dlp needs a coffee break (aka update)

```bash
pip install --upgrade yt-dlp
# Sometimes YouTube changes their API, we adapt
```

### 🚫 **Problem**: "ffmpeg not found"

**🎯 Solution**: Install the video processing Swiss Army knife

```bash
# Ubuntu/Debian (The Penguins)
sudo apt install ffmpeg

# macOS (The Apple Way)
brew install ffmpeg

# Windows (The Scenic Route)
# Download from https://ffmpeg.org/download.html
```

### 🐌 **Problem**: "Downloads are slower than my internet in 2005"

**🎯 Possible Causes**:
- Facebook's servers are having a bad day
- Your internet is actually from 2005
- The video is 4K and massive
- Planetary alignment is off

**🎯 Solutions**:
- Try a lower quality setting
- Check your internet connection
- Wait for Mercury to stop being in retrograde
- Consider downloading smaller videos first

# Windows - Download from https://ffmpeg.org/
```

### 🚨 **Problem**: Rate limit exceeded

**🎯 Solution**: Patience, young grasshopper! Wait 60 seconds and try again.
*Our rate limiter protects the server from overzealous downloading sprees*

### 🔗 **Problem**: "Invalid Facebook URL"

**🎯 Solution**: Make sure you're using a direct video URL, not a post link
- ✅ Good: `https://www.facebook.com/watch/?v=123456789`
- ❌ Bad: `https://www.facebook.com/user/posts/123456789`

### 🔍 Debug Mode (For the Curious)

Want to see what's happening under the hood?

```bash
export DEBUG=true
python -m app.main
# Now you'll see ALL the things!
```

---

## 🏗️ Project Architecture

*"How the sausage is made"*

```
📁 Facebook-Video-Download-API/
├── 🐍 app/
│   ├── main.py              # The FastAPI magic happens here
│   ├── config.py            # All the boring settings
│   ├── models.py            # Data structures (Pydantic models)
│   ├── services/
│   │   └── video_service.py # The video downloading wizard
│   └── utils/
│       ├── rate_limiter.py  # The "calm down" enforcer
│       └── validators.py    # The URL quality checker
├── 🌐 static/
│   ├── index.html          # Pretty web interface
│   └── script.js           # Frontend JavaScript magic
├── 🐳 docker-compose.yml   # One-click deployment
├── 📦 Dockerfile          # Container recipe
└── 📋 requirements.txt     # Python shopping list
```

---

## 🚀 Deploy Your Own Instance

*"Because sharing is caring, but having your own is cooler!"*

### **🌟 Render (The Easy Button)**

1. **🍴 Fork** this repository to your GitHub
2. **🔗 Sign up** at [Render](https://render.com) with GitHub  
3. **➕ Create** a new Web Service → Connect your forked repo
4. **⚙️ Configure** these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     - `DEBUG=false` *(Keep it professional)*
     - `PYTHON_VERSION=3.11.9` *(The good stuff)*
5. **🚀 Deploy** and be live in ~5 minutes!

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

*Pro tip: Render's free tier is perfect for personal use and small projects!*

---

## 🤝 Contributing

*"All contributions welcome - from typo fixes to feature additions!"*

1. **🍴 Fork** the repo
2. **🌿 Branch** it (`git checkout -b feature/MyAwesomeFeature`)
3. **✨ Code** your magic
4. **💾 Commit** with style (`git commit -m 'Add some MyAwesomeFeature'`)
5. **🚀 Push** it (`git push origin feature/MyAwesomeFeature`)
6. **🎯 PR** it (Open a Pull Request)

*Don't forget to add tests if you're feeling fancy!* 🧪

---

## 📜 License

This project is licensed under **WPFTL (WTFPL)** - see the [LICENSE](LICENSE) file for details.

**🎉 TL;DR**: Do whatever you want with this code! Build it, break it, sell it, frame it - we don't mind!

## 🙏 Acknowledgments

*"Standing on the shoulders of giants (and caffeinated developers)"*

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - The Swiss Army knife of video downloading ⚔️
- **[FastAPI](https://fastapi.tiangolo.com/)** - The web framework that makes APIs fun again 🚀
- **[Tailwind CSS](https://tailwindcss.com/)** - Making things pretty without the CSS nightmares 🎨
- **[ffmpeg](https://ffmpeg.org/)** - The video processing wizard behind the curtain 🧙‍♂️
- **Coffee** ☕ - The real MVP

## 📞 Support & Community

*"Need help? We've got your back!"*

- 🐛 **Found a Bug?** → [GitHub Issues](https://github.com/sh13y/Facebook-Video-Download-API/issues)
- 💬 **Want to Chat?** → [GitHub Discussions](https://github.com/sh13y/Facebook-Video-Download-API/discussions)
- 📧 **Direct Contact** → [GitHub Profile](https://github.com/sh13y)
- 📖 **Read the Docs** → Check out our [documentation files](#-complete-documentation-suite) above!

*Response time: Usually faster than your pizza delivery! 🍕*

## 🏆 Star History

*"Our journey to GitHub stardom (one ⭐ at a time)"*

[![Star History Chart](https://api.star-history.com/svg?repos=sh13y/Facebook-Video-Download-API&type=Date)](https://star-history.com/#sh13y/Facebook-Video-Download-API&Date)

---

<div align="center">

### 🇱🇰 **Made in Ceylon with ❤️ and Lots of Tea** 

**Created by [sh13y](https://github.com/sh13y)**

*If this project saved you from manually downloading videos one by one,*  
*show some love with a ⭐ and maybe buy me a virtual tea!* 🍵

---

**Fun Fact**: This entire project was built because downloading Facebook videos  
shouldn't require a PhD in Computer Science! 🎓

---

[![Visitors](https://api.visitorbadge.io/api/visitors?path=sh13y%2FFacebook-Video-Download-API&labelColor=%23697689&countColor=%23555555)](https://visitorbadge.io/status?path=sh13y%2FFacebook-Video-Download-API)
[![GitHub forks](https://img.shields.io/github/forks/sh13y/Facebook-Video-Download-API?style=social)](https://github.com/sh13y/Facebook-Video-Download-API/fork)
[![GitHub stars](https://img.shields.io/github/stars/sh13y/Facebook-Video-Download-API?style=social)](https://github.com/sh13y/Facebook-Video-Download-API)

</div>README update to trigger workflow
