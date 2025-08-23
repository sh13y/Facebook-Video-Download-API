#!/bin/bash

# 🚀 Pre-deployment Test Script for Render
# This script tests your app locally before deploying to Render

echo "🔍 Testing Facebook Video Downloader before Render deployment..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📋 Installing dependencies..."
pip install -r requirements.txt

# Set environment variables for testing
export DEBUG=false
export RATE_LIMIT_REQUESTS=10
export RATE_LIMIT_WINDOW=60
export HOST=0.0.0.0
export PORT=8000

# Check if ffmpeg is available
echo "🔧 Checking ffmpeg availability..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ ffmpeg is available"
else
    echo "❌ ffmpeg not found - install with: sudo apt install ffmpeg"
    exit 1
fi

# Test the application
echo "🧪 Testing application startup..."
timeout 10s python -m app.main &
APP_PID=$!

# Wait for app to start
sleep 5

# Test health endpoint
echo "🏥 Testing health endpoint..."
curl -f http://localhost:8000/health > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    kill $APP_PID 2>/dev/null
    exit 1
fi

# Test static files
echo "🌐 Testing static files..."
curl -f http://localhost:8000/ > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Static files served correctly"
else
    echo "❌ Static files not found"
    kill $APP_PID 2>/dev/null
    exit 1
fi

# Clean up
kill $APP_PID 2>/dev/null

echo ""
echo "🎉 All tests passed! Your app is ready for Render deployment."
echo ""
echo "📋 Next steps:"
echo "1. Push your code to GitHub"
echo "2. Go to render.com"
echo "3. Create new Web Service"
echo "4. Connect your GitHub repo"
echo "5. Use these settings:"
echo "   - Build: pip install -r requirements.txt"
echo "   - Start: uvicorn app.main:app --host 0.0.0.0 --port \$PORT"
echo "   - Environment: DEBUG=false"
echo ""
echo "🌟 Your app will be live at: https://your-app-name.onrender.com"
