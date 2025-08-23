# 🌐 Netlify Deployment Guide

## 🚀 Deploy Facebook Video Downloader on Netlify

Netlify is great for static sites and serverless functions. Here's how to deploy your FastAPI app:

## 📋 Prerequisites

- GitHub repository with your code
- Netlify account (free)

## 🛠️ Deployment Methods

### Method 1: **Direct GitHub Deploy** (Recommended)

1. **Go to Netlify**: [netlify.app](https://netlify.app)
2. **Sign up/Login** with GitHub
3. **New site from Git** → **GitHub**
4. **Select your repository**: `sh13y/Facebook-Video-Download-API`
5. **Configure build settings**:
   - **Build command**: `pip install -r requirements.txt`
   - **Publish directory**: `static`
   - **Functions directory**: `netlify/functions`
6. **Environment variables** (in Site settings):
   ```
   DEBUG=false
   RATE_LIMIT_REQUESTS=10
   RATE_LIMIT_WINDOW=60
   ```
7. **Deploy site**

### Method 2: **Netlify CLI** (Advanced)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy from your project directory
cd "/home/shiey/Downloads/Facebook Video Download API"
netlify deploy --prod --dir=static --functions=netlify/functions
```

## 🌐 **Live URLs**

After deployment:
- **Web Interface**: `https://your-site-name.netlify.app`
- **API Endpoint**: `https://your-site-name.netlify.app/.netlify/functions/app`

## 📁 **Project Structure for Netlify**

```
Facebook-Video-Download-API/
├── static/
│   ├── index.html          # Main web interface
│   └── script.js           # Frontend JavaScript
├── netlify/
│   └── functions/
│       ├── app.py          # Serverless FastAPI handler
│       └── requirements.txt # Function dependencies
├── netlify.toml            # Netlify configuration
├── app/                    # Your FastAPI application
└── requirements.txt        # Main dependencies
```

## ⚙️ **Configuration Details**

### netlify.toml
```toml
[build]
  command = "pip install -r requirements.txt"
  functions = "netlify/functions"
  publish = "static"

[functions]
  python_version = "3.11"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/app/:splat"
  status = 200

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## 🔧 **Environment Variables**

Set these in Netlify Dashboard → Site Settings → Environment Variables:

```
DEBUG=false
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60
```

## 🚨 **Important Limitations**

### Netlify Functions Limits (Free Tier):
- ⏱️ **Execution time**: 10 seconds max
- 💾 **Memory**: 1GB max  
- 📦 **Bundle size**: 50MB max
- 🔢 **Requests**: 125K/month

### ⚠️ **Potential Issues**:
- **ffmpeg**: May not work in serverless environment
- **Large videos**: May timeout due to 10-second limit
- **File downloads**: Limited by function execution time

## 💡 **Alternative: Hybrid Approach**

For better performance, consider this hybrid setup:

1. **Static site on Netlify** (frontend only)
2. **API on Railway/Render** (backend with full capabilities)
3. **CORS enabled** for cross-origin requests

Update your `static/script.js`:
```javascript
const API_URL = 'https://your-api.railway.app'; // Your backend URL

const response = await fetch(`${API_URL}/download`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        url: url,
        quality: quality
    })
});
```

## 🎯 **Recommended Approach**

Given the limitations of serverless functions for video processing:

### **Option A: Full Netlify** (Limited functionality)
- ✅ Free hosting
- ❌ Limited by 10-second execution time
- ❌ No ffmpeg support
- ❌ May timeout on large videos

### **Option B: Hybrid** (Recommended)
- ✅ **Frontend on Netlify** (free static hosting)
- ✅ **Backend on Railway** (full functionality)
- ✅ Best of both worlds

### **Option C: Full Railway** (Easiest)
- ✅ Complete functionality
- ✅ No limitations
- ✅ Simple deployment

## 🚀 **Quick Deploy Commands**

### Deploy to Netlify (Functions):
```bash
# Using Netlify CLI
netlify deploy --prod
```

### Deploy Frontend to Netlify + Backend to Railway:
1. **Netlify**: Deploy `static/` folder only
2. **Railway**: Deploy full application
3. **Update API URL** in frontend

## 📊 **Comparison**

| Approach | Setup | Functionality | Performance | Cost |
|----------|-------|---------------|-------------|------|
| Full Netlify | Easy | Limited | Poor (timeouts) | Free |
| Hybrid | Medium | Full | Excellent | Free |
| Full Railway | Easy | Full | Excellent | Free |

## 🎯 **My Recommendation**

For your Facebook Video Downloader:

1. **Start with Railway** for full functionality
2. **Use Netlify** only for static frontend if needed
3. **Avoid Netlify Functions** for video processing (too limited)

**Railway is still your best bet for a working demo!** 🚀

Would you like me to help you set up the hybrid approach instead?
