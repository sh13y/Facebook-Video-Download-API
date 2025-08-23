const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');

const app = express();
app.use(cors());
app.use(express.json());

// POST /download - expects { url: "facebook_video_url" }
app.post('/download', (req, res) => {
  const { url } = req.body;
  if (!url) {
    return res.status(400).json({ error: 'No URL provided' });
  }
  // Stream video file from yt-dlp directly to response
  const { spawn } = require('child_process');
  const ytDlp = spawn('yt-dlp', ['-f', 'best', '-o', '-', url]);
  res.setHeader('Content-Type', 'video/mp4');
  res.setHeader('Content-Disposition', 'attachment; filename="video.mp4"');
  ytDlp.stdout.pipe(res);
  ytDlp.stderr.on('data', (data) => {
    console.error(`yt-dlp error: ${data}`);
  });
  ytDlp.on('error', (err) => {
    res.status(500).json({ error: err.message });
  });
  ytDlp.on('close', (code) => {
    if (code !== 0) {
      res.end();
    }
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
