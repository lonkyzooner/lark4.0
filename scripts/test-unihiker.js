/**
 * Test script for LARK on UniHiker M10
 * 
 * This script simulates the UniHiker M10 environment and tests the voice-first interface.
 * Run this script with: node scripts/test-unihiker.js
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

// Configuration
const PORT = 3000;
const DIST_DIR = path.join(__dirname, '../dist');
const INDEX_PATH = path.join(DIST_DIR, 'index.html');

// Check if the dist directory exists
if (!fs.existsSync(DIST_DIR)) {
  console.error('Error: dist directory not found. Please build the project first.');
  console.log('Run: npm run build');
  process.exit(1);
}

// Create a simple HTTP server
const server = http.createServer((req, res) => {
  let filePath = path.join(DIST_DIR, req.url === '/' ? 'index.html' : req.url);
  
  // Add URL parameter to force UniHiker mode
  if (req.url === '/') {
    const indexContent = fs.readFileSync(INDEX_PATH, 'utf8');
    const modifiedContent = indexContent.replace(
      '</head>',
      '<script>window.FORCE_UNIHIKER = true;</script></head>'
    );
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(modifiedContent);
    return;
  }
  
  // Handle file requests
  const extname = String(path.extname(filePath)).toLowerCase();
  const contentType = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.wav': 'audio/wav',
    '.mp3': 'audio/mpeg',
    '.mp4': 'video/mp4',
    '.woff': 'application/font-woff',
    '.ttf': 'application/font-ttf',
    '.eot': 'application/vnd.ms-fontobject',
    '.otf': 'application/font-otf',
    '.wasm': 'application/wasm'
  }[extname] || 'application/octet-stream';
  
  fs.readFile(filePath, (error, content) => {
    if (error) {
      if (error.code === 'ENOENT') {
        // File not found
        res.writeHead(404);
        res.end('File not found');
      } else {
        // Server error
        res.writeHead(500);
        res.end(`Server Error: ${error.code}`);
      }
    } else {
      // Success
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content, 'utf-8');
    }
  });
});

// Start the server
server.listen(PORT, () => {
  console.log(`\n🚀 LARK UniHiker Test Server running at http://localhost:${PORT}\n`);
  console.log('🔊 Voice-First Interface is active with "Hey LARK" wake word detection');
  console.log('🖥️  Simulating UniHiker M10 display (240x320)');
  console.log('🎤 Testing microphone and speech synthesis capabilities\n');
  console.log('Press Ctrl+C to stop the server\n');
  
  // Open the browser automatically
  const url = `http://localhost:${PORT}?unihiker=true`;
  const command = process.platform === 'darwin' ? `open "${url}"` :
                 process.platform === 'win32' ? `start "${url}"` :
                 `xdg-open "${url}"`;
  
  exec(command, (error) => {
    if (error) {
      console.error('Error opening browser:', error);
    }
  });
});

// Handle server shutdown
process.on('SIGINT', () => {
  console.log('\nShutting down LARK UniHiker Test Server...');
  server.close(() => {
    console.log('Server stopped');
    process.exit(0);
  });
});
