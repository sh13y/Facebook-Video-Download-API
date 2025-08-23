# Facebook Video Downloader API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
No authentication required.

## Rate Limiting
- **Limit**: 10 requests per 60 seconds per IP
- **Headers**: Rate limit information included in response headers

## Endpoints

### GET /
**Description**: Serve the main web interface

**Response**: HTML page

---

### GET /health
**Description**: Health check endpoint

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "service": "Facebook Video Downloader API"
}
```

---

### POST /download
**Description**: Download Facebook video and get direct download link

**Request Body**:
```json
{
  "url": "string (required)",
  "quality": "string (optional, default: best)"
}
```

**Quality Options**: `best`, `worst`, `360p`, `720p`, `1080p`

**Success Response** (200):
```json
{
  "status": "success",
  "video_info": {
    "title": "string",
    "duration": 828,
    "thumbnail": "string (URL)",
    "uploader": "string",
    "view_count": 1000000,
    "upload_date": "string (YYYYMMDD)"
  },
  "download_url": "string (direct download URL)",
  "available_formats": [
    {
      "quality": "720p",
      "format_id": "string",
      "ext": "mp4",
      "filesize": 50000000,
      "url": "string"
    }
  ]
}
```

**Error Response** (400):
```json
{
  "status": "error",
  "message": "Invalid Facebook URL provided",
  "error_code": "INVALID_REQUEST"
}
```

---

### POST /info
**Description**: Get Facebook video information without download URL

**Request Body**: Same as `/download`

**Response**: Same as `/download` but without `download_url`

---

### GET /qualities
**Description**: Get list of supported video qualities

**Response**:
```json
{
  "status": "success",
  "qualities": ["best", "worst", "360p", "720p", "1080p"],
  "descriptions": {
    "best": "Best available quality",
    "worst": "Worst available quality",
    "360p": "360p resolution",
    "720p": "720p resolution",
    "1080p": "1080p resolution"
  }
}
```

## Supported URL Formats

- `https://www.facebook.com/watch/?v=123456789`
- `https://www.facebook.com/username/videos/123456789`
- `https://www.facebook.com/share/v/abc123/`
- `https://fb.watch/abc123/`

## Error Codes

| Code | Description |
|------|-------------|
| `INVALID_REQUEST` | Invalid request parameters |
| `PROCESSING_ERROR` | Error processing video |
| `INTERNAL_ERROR` | Internal server error |
| `RATE_LIMIT_EXCEEDED` | Rate limit exceeded |

## Examples

### cURL Example
```bash
curl -X POST "http://localhost:8000/download" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.facebook.com/share/v/17GS54EKBN/",
    "quality": "best"
  }'
```

### JavaScript Example
```javascript
const response = await fetch('/download', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://www.facebook.com/share/v/17GS54EKBN/',
    quality: 'best'
  })
});

const data = await response.json();
console.log(data);
```

### Python Example
```python
import requests

response = requests.post('http://localhost:8000/download', json={
    'url': 'https://www.facebook.com/share/v/17GS54EKBN/',
    'quality': 'best'
})

data = response.json()
print(data)
```
