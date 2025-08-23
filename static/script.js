// Facebook Video Downloader - Frontend JavaScript
// Made in Ceylon 🇱🇰 with ❤️ by sh13y

class FacebookVideoDownloader {
    constructor() {
        this.form = document.getElementById('downloadForm');
        this.loadingState = document.getElementById('loadingState');
        this.results = document.getElementById('results');
        this.errorState = document.getElementById('errorState');
        this.downloadBtn = document.getElementById('downloadBtn');
        
        this.init();
    }
    
    init() {
        this.form.addEventListener('submit', this.handleSubmit.bind(this));
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        const url = document.getElementById('videoUrl').value.trim();
        const quality = document.querySelector('input[name="quality"]:checked').value;
        
        if (!this.isValidFacebookUrl(url)) {
            this.showError('Please enter a valid Facebook video URL');
            return;
        }
        
        this.showLoading();
        
        try {
            const response = await fetch('/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: url,
                    quality: quality
                })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail?.message || data.message || 'Failed to download video');
            }
            
            this.showResults(data);
            
        } catch (error) {
            console.error('Download error:', error);
            this.showError(error.message || 'An error occurred while processing your request');
        }
    }
    
    isValidFacebookUrl(url) {
        const facebookUrlPatterns = [
            // Standard Facebook domains
            /^https?:\/\/(www\.|web\.|m\.)?facebook\.com\/.*$/,
            // Short URLs
            /^https?:\/\/fb\.watch\/.*$/
        ];
        
        return facebookUrlPatterns.some(pattern => pattern.test(url));
    }
    
    showLoading() {
        this.hideAllStates();
        this.loadingState.classList.remove('hidden');
        this.downloadBtn.disabled = true;
        this.downloadBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Processing...';
    }
    
    showResults(data) {
        this.hideAllStates();
        
        const videoInfo = document.getElementById('videoInfo');
        const downloadLink = document.getElementById('downloadLink');
        
        // Populate video information
        videoInfo.innerHTML = `
            <div class="grid md:grid-cols-2 gap-4">
                <div>
                    <p class="text-sm font-medium text-gray-700">Title:</p>
                    <p class="text-sm text-gray-600 break-words">${this.escapeHtml(data.video_info.title || 'N/A')}</p>
                </div>
                <div>
                    <p class="text-sm font-medium text-gray-700">Duration:</p>
                    <p class="text-sm text-gray-600">${this.formatDuration(data.video_info.duration)}</p>
                </div>
                <div>
                    <p class="text-sm font-medium text-gray-700">Uploader:</p>
                    <p class="text-sm text-gray-600">${this.escapeHtml(data.video_info.uploader || 'N/A')}</p>
                </div>
                <div>
                    <p class="text-sm font-medium text-gray-700">Views:</p>
                    <p class="text-sm text-gray-600">${this.formatNumber(data.video_info.view_count)}</p>
                </div>
            </div>
        `;
        
        // Set download link with streaming endpoint
        const videoId = this.generateVideoId(data.video_info.title);
        const streamUrl = `/stream/${videoId}?url=${encodeURIComponent(data.download_url)}`;
        downloadLink.href = streamUrl;
        downloadLink.download = this.generateFileName(data.video_info.title);
        
        // Remove the custom onclick handler - use native download
        downloadLink.onclick = null;
        
        this.results.classList.remove('hidden');
        this.resetButton();
    }
    
    showError(message) {
        this.hideAllStates();
        document.getElementById('errorMessage').textContent = message;
        this.errorState.classList.remove('hidden');
        this.resetButton();
    }
    
    hideAllStates() {
        this.loadingState.classList.add('hidden');
        this.results.classList.add('hidden');
        this.errorState.classList.add('hidden');
    }
    
    resetButton() {
        this.downloadBtn.disabled = false;
        this.downloadBtn.innerHTML = '<i class="fas fa-download mr-2"></i>Download Video';
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    formatDuration(seconds) {
        if (!seconds) return 'N/A';
        
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const remainingSeconds = seconds % 60;
        
        if (hours > 0) {
            return `${hours}:${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
        }
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
    
    formatNumber(num) {
        if (!num) return 'N/A';
        return num.toLocaleString();
    }
    
    generateFileName(title) {
        if (!title) return 'facebook_video.mp4';
        
        // Clean title for filename
        const cleanTitle = title
            .replace(/[^\w\s-]/g, '') // Remove special characters
            .replace(/\s+/g, '_') // Replace spaces with underscores
            .substring(0, 50); // Limit length
            
        return `${cleanTitle}.mp4`;
    }
    
    generateVideoId(title) {
        if (!title) return 'facebook_video';
        
        // Create a simple ID from title
        return title
            .replace(/[^\w\s-]/g, '') // Remove special characters
            .replace(/\s+/g, '_') // Replace spaces with underscores
            .toLowerCase()
            .substring(0, 30); // Limit length
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FacebookVideoDownloader();
});

// Add some UI enhancements
document.addEventListener('DOMContentLoaded', () => {
    // Add smooth scrolling for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Add input validation feedback
    const urlInput = document.getElementById('videoUrl');
    urlInput.addEventListener('input', function() {
        const url = this.value.trim();
        const isValid = url === '' || /^https?:\/\/(www\.)?(facebook\.com|fb\.watch)/.test(url);
        
        this.classList.toggle('border-red-300', !isValid && url !== '');
        this.classList.toggle('border-green-300', isValid && url !== '');
    });
});
