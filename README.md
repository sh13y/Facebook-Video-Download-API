# 🎥 Facebook Video Downloader API

[![Made in Ceylon](https://img.shields.io/badge/Made%20in-Ceylon%20🇱🇰-ff6b35?style=for-the-badge)](https://github.com/sh13y)
[![License](https://img.shields.io/badge/License-WPFTL-blue.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ed?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

> *"Because sometimes you just need that perfect Facebook video for your meme collection... or your business presentation. We don't judge!"* 😏

A **production-ready** REST API and sleek web interface for downloading Facebook videos with crystal-clear audio support. Built with modern tech stack: **FastAPI** + **yt-dlp** + a dash of engineering magic ✨.

*Fun fact: This started because Facebook's "Save Video" feature was as reliable as weather predictions. So we built something that actually works!* 🌩️

---

## ✨ Features That'll Make You Go "Wow!"

- **🚀 Lightning Fast**: FastAPI under the hood - because nobody has time to wait
- **🎵 Audio Magic**: Automatically merges video+audio streams (Facebook's DASH format tried to trick us, but we're smarter!)
- **📱 Gorgeous UI**: Responsive web interface that works on everything from phones to 4K monitors
- **🎯 Quality Options**: 360p to 1080p - from "good enough for WhatsApp" to "cinematic masterpiece"
- **🛡️ Bulletproof**: Rate limiting, error handling, and logging - because crashes are for cars, not APIs
- **🐳 Docker Ready**: One command deployment - easier than making instant noodles
- **🌐 URL Flexibility**: Handles all Facebook URL formats - we speak fluent Facebook

---

## 🌟 Live Demo

**✨ Try it now:** [https://facebook-video-download-api.onrender.com/](https://facebook-video-download-api.onrender.com/)
> *Go ahead, paste that video URL you've been saving "for later" since 2019* 

**📖 API Documentation:** [https://facebook-video-download-api.onrender.com/docs](https://facebook-video-download-api.onrender.com/docs)
> *Interactive docs that are more fun than reading terms & conditions*

---

## 📚 Complete Documentation Suite

We believe in documentation more than we believe in coffee ☕ (and that's saying something!):

| 📄 Document | 🎯 Purpose | 😄 TL;DR |
|-------------|------------|-----------|
| **[API_DOCS.md](API_DOCS.md)** | Complete API reference | "How to make this thing do the thing" |
| **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** | Multi-platform deployment | "Deploy anywhere, anytime, any cloud" |
| **[RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)** | Render-specific guide | "The easiest way to go live" |
| **[NETLIFY_DEPLOYMENT.md](NETLIFY_DEPLOYMENT.md)** | Netlify deployment | "For the static site lovers" |
| **[PROBLEMS_AND_SOLUTIONS.md](PROBLEMS_AND_SOLUTIONS.md)** | Troubleshooting guide | "When things go wrong (and they will)" |

*Pro tip: Start with PROBLEMS_AND_SOLUTIONS.md - it's like a FAQ but for developers who've seen things.* 👀

## 🚀 Quick Start Guide

*"From zero to hero in 3 minutes or your money back!"* 💸

### 🔧 Prerequisites

Before we dive into the fun stuff, make sure you have:

- **Python 3.11+** *(Because we're modern like that)*
- **ffmpeg** *(The Swiss Army knife of video processing)*
- **A sense of adventure** *(Optional but recommended)*

```bash
# Check if you're ready to rock
python --version  # Should say 3.11 or higher
ffmpeg -version   # Should not say "command not found"
```

### 🐳 Docker Deployment (Recommended)

*"Why make it complicated when you can make it simple?"*

```bash
# Clone this masterpiece
git clone https://github.com/sh13y/Facebook-Video-Download-API.git
cd Facebook-Video-Download-API

# One command to rule them all
docker-compose up -d

# Visit the magic:
# 🌐 Web Interface: http://localhost:8000
# 📖 API Docs: http://localhost:8000/docs
```

### 🏃‍♂️ Local Development Setup

*"For those who like to tinker under the hood"*

```bash
# Clone and enter the matrix
git clone https://github.com/sh13y/Facebook-Video-Download-API.git
cd Facebook-Video-Download-API

# Create your Python playground
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install the good stuff
pip install -r requirements.txt

# Install ffmpeg (the video wizard)
# Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg
# macOS: brew install ffmpeg  
# Windows: Download from https://ffmpeg.org/download.html

# Launch the rocket 🚀
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Boom!** Visit `http://localhost:8000` and start downloading those cat videos! 🐱
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

</div>