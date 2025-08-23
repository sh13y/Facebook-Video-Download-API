# 🚀 Deployment Guide - Facebook Video Downloader API

## Quick Deploy Options

### 1. **Railway** ⭐ (Recommended - Easy & Fast)

**Why Railway?**
- ✅ Simple one-click deployment
- ✅ Automatic HTTPS
- ✅ Good performance & uptime
- ✅ $5 free credit monthly
- ✅ Easy environment variable management

**Steps:**
1. **Push to GitHub** (if not already done)
2. **Go to Railway**: [railway.app](https://railway.app)
3. **New Project** → **Deploy from GitHub**
4. **Select Repository**: `sh13y/Facebook-Video-Download-API`
5. **Deploy**: Click deploy button
6. **Set Environment Variables**:
   ```
   DEBUG=false
   RATE_LIMIT_REQUESTS=10
   RATE_LIMIT_WINDOW=60
   ```
7. **Custom Domain** (optional): Add your own domain
8. **Live URL**: `https://your-app.railway.app`

**Estimated Setup Time**: 5 minutes

---

### 2. **Render** ⭐ (Great for Python Apps)

**Why Render?**
- ✅ Excellent Python/FastAPI support
- ✅ Automatic deployments from GitHub
- ✅ 750 free hours/month
- ✅ Built-in SSL

**Steps:**
1. **Go to Render**: [render.com](https://render.com)
2. **New Web Service**
3. **Connect GitHub**: Link your repository
4. **Configuration**:
   - **Name**: `facebook-video-downloader`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables**:
   ```
   DEBUG=false
   RATE_LIMIT_REQUESTS=10
   ```
6. **Deploy**: Click "Create Web Service"
7. **Live URL**: `https://facebook-video-downloader.onrender.com`

**Note**: Free tier sleeps after 15 minutes of inactivity

**Estimated Setup Time**: 10 minutes

---

### 3. **Fly.io** (Docker-based)

**Why Fly.io?**
- ✅ Excellent performance
- ✅ Docker support
- ✅ Global edge deployment
- ✅ 2,340 free hours/month

**Steps:**
1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**:
   ```bash
   flyctl auth login
   ```

3. **Launch App**:
   ```bash
   cd your-repo
   flyctl launch
   ```

4. **Configure** (flyctl will generate `fly.toml`):
   ```toml
   app = "facebook-video-downloader"
   
   [env]
   DEBUG = "false"
   RATE_LIMIT_REQUESTS = "10"
   ```

5. **Deploy**:
   ```bash
   flyctl deploy
   ```

6. **Live URL**: `https://facebook-video-downloader.fly.dev`

**Estimated Setup Time**: 15 minutes

---

### 4. **Cyclic** (Serverless)

**Why Cyclic?**
- ✅ Serverless (always awake)
- ✅ Unlimited free deployments
- ✅ Good for APIs

**Steps:**
1. **Go to Cyclic**: [cyclic.sh](https://cyclic.sh)
2. **Deploy from GitHub**
3. **Select Repository**
4. **Automatic deployment**

**Note**: May need minor code adjustments for serverless

---

## 🔧 Pre-Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] All dependencies in `requirements.txt`
- [ ] `Procfile` created (for some platforms)
- [ ] Environment variables configured
- [ ] Docker setup tested (if using Docker)

## 📊 Platform Comparison

| Platform | Free Tier | Uptime | Setup | Performance | Best For |
|----------|-----------|--------|-------|-------------|----------|
| Railway | $5 credit/month | Excellent | ⭐⭐⭐ | High | Production demos |
| Render | 750 hrs/month | Good (sleeps) | ⭐⭐⭐ | Good | Development/testing |
| Fly.io | 2,340 hrs/month | Excellent | ⭐⭐ | High | Global deployment |
| Cyclic | Unlimited | Excellent | ⭐⭐⭐ | Good | Simple APIs |

## 🌍 Recommended Demo URLs

After deployment, your demo will be available at:

- **Railway**: `https://facebook-video-downloader.railway.app`
- **Render**: `https://facebook-video-downloader.onrender.com`
- **Fly.io**: `https://facebook-video-downloader.fly.dev`

## 📝 Post-Deployment Tips

1. **Update README** with your live demo URL
2. **Test thoroughly** with different Facebook video URLs
3. **Monitor usage** to stay within free limits
4. **Set up monitoring** for uptime tracking
5. **Configure custom domain** for professional look

## 🚨 Important Notes

- **Rate Limiting**: Free tiers have request limits
- **Sleep Mode**: Some platforms sleep inactive apps
- **Resource Limits**: Free tiers have CPU/memory constraints
- **Build Time**: Initial deployment may take 5-15 minutes

## 💡 Pro Tips

1. **Railway** is best for demos that need to stay awake
2. **Render** is perfect for development and testing
3. Use **environment variables** for configuration
4. Test locally before deploying
5. Monitor logs for issues

---

**Choose Railway for the easiest deployment experience!** 🚀
