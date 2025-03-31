/**
 * Optimization script for LARK on UniHiker M10
 * 
 * This script applies performance optimizations for the UniHiker M10 device.
 * Run this script after building the application and before deploying to the device.
 * 
 * Run this script with: node scripts/optimize-unihiker.js
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Configuration
const DIST_DIR = path.join(__dirname, '../dist');
const INDEX_HTML = path.join(DIST_DIR, 'index.html');
const ASSETS_DIR = path.join(DIST_DIR, 'assets');

console.log('🔧 Optimizing LARK for UniHiker M10...');

// Function to get all JS files in the assets directory
function getJsFiles(dir) {
  return fs.readdirSync(dir)
    .filter(file => file.endsWith('.js'))
    .map(file => path.join(dir, file));
}

// Add UniHiker-specific optimizations to index.html
try {
  console.log('📝 Modifying index.html for UniHiker...');
  
  let indexContent = fs.readFileSync(INDEX_HTML, 'utf8');
  
  // Add viewport meta tag optimized for UniHiker's screen
  if (!indexContent.includes('viewport')) {
    indexContent = indexContent.replace(
      '<head>',
      '<head>\n  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">'
    );
  }
  
  // Add UniHiker flag to force UniHiker mode
  if (!indexContent.includes('FORCE_UNIHIKER')) {
    indexContent = indexContent.replace(
      '</head>',
      '  <script>window.FORCE_UNIHIKER = true;</script>\n</head>'
    );
  }
  
  // Add preconnect for LiveKit to improve connection speed
  if (!indexContent.includes('preconnect') && !indexContent.includes('livekit.cloud')) {
    indexContent = indexContent.replace(
      '</head>',
      '  <link rel="preconnect" href="https://lark-za4hpayr.livekit.cloud" crossorigin>\n</head>'
    );
  }
  
  // Add offline capability hint
  if (!indexContent.includes('manifest.json')) {
    indexContent = indexContent.replace(
      '</head>',
      '  <link rel="manifest" href="/manifest.json">\n</head>'
    );
    
    // Create a basic manifest file
    const manifestPath = path.join(DIST_DIR, 'manifest.json');
    const manifestContent = JSON.stringify({
      "name": "LARK - Law Enforcement Assistance and Response Kit",
      "short_name": "LARK",
      "start_url": "/",
      "display": "standalone",
      "background_color": "#003087",
      "theme_color": "#003087",
      "icons": [
        {
          "src": "/favicon.ico",
          "sizes": "48x48",
          "type": "image/x-icon"
        }
      ]
    }, null, 2);
    
    fs.writeFileSync(manifestPath, manifestContent);
    console.log('✅ Created manifest.json for offline capabilities');
  }
  
  fs.writeFileSync(INDEX_HTML, indexContent);
  console.log('✅ Modified index.html successfully');
} catch (error) {
  console.error('❌ Error modifying index.html:', error);
}

// Create a service worker for offline capabilities
try {
  console.log('🔄 Creating service worker for offline capabilities...');
  
  const swPath = path.join(DIST_DIR, 'sw.js');
  const swContent = `// LARK Service Worker for UniHiker M10
const CACHE_NAME = 'lark-unihiker-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json',
  '/favicon.ico',
  ${getJsFiles(ASSETS_DIR).map(file => `'/${path.relative(DIST_DIR, file)}'`).join(',\n  ')}
];

// Install event - cache assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch event - serve from cache if available
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit - return response
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
`;
  
  fs.writeFileSync(swPath, swContent);
  console.log('✅ Created service worker successfully');
  
  // Register the service worker in index.html
  let indexContent = fs.readFileSync(INDEX_HTML, 'utf8');
  if (!indexContent.includes('serviceWorker')) {
    const swRegistration = `
  <script>
    // Register service worker for offline capabilities
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
          .then(registration => {
            console.log('ServiceWorker registration successful with scope: ', registration.scope);
          })
          .catch(error => {
            console.log('ServiceWorker registration failed: ', error);
          });
      });
    }
  </script>`;
    
    indexContent = indexContent.replace('</body>', `${swRegistration}\n</body>`);
    fs.writeFileSync(INDEX_HTML, indexContent);
    console.log('✅ Registered service worker in index.html');
  }
} catch (error) {
  console.error('❌ Error creating service worker:', error);
}

// Create a startup script for the UniHiker
try {
  console.log('📜 Creating startup script for UniHiker...');
  
  const startupPath = path.join(DIST_DIR, 'start-lark.sh');
  const startupContent = `#!/bin/bash
# LARK UniHiker Startup Script

echo "Starting LARK on UniHiker M10..."

# Set the web server directory
WEB_DIR="/var/www/html"

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
  echo "This script must be run as root" 
  exit 1
fi

# Copy LARK files to web server directory
echo "Copying LARK files to web server..."
cp -r ./* $WEB_DIR/

# Set appropriate permissions
chmod -R 755 $WEB_DIR

# Start the web server if not already running
if command -v nginx &> /dev/null; then
  if ! systemctl is-active --quiet nginx; then
    echo "Starting nginx web server..."
    systemctl start nginx
  fi
elif command -v lighttpd &> /dev/null; then
  if ! systemctl is-active --quiet lighttpd; then
    echo "Starting lighttpd web server..."
    systemctl start lighttpd
  fi
else
  echo "No supported web server found. Please install nginx or lighttpd."
  exit 1
fi

echo ""
echo "LARK is now available at http://localhost"
echo "You can access it from the UniHiker's web browser"
echo ""
echo "For best experience:"
echo "1. Connect a USB speaker for audio output"
echo "2. Use the wake word 'Hey LARK' to activate"
echo "3. Speak commands clearly into the microphone"
echo ""
echo "Press Ctrl+C to stop this script"

# Keep the script running to prevent it from closing
while true; do
  sleep 1
done
`;
  
  fs.writeFileSync(startupPath, startupContent);
  fs.chmodSync(startupPath, 0o755); // Make executable
  console.log('✅ Created startup script successfully');
} catch (error) {
  console.error('❌ Error creating startup script:', error);
}

console.log('✅ Optimization completed successfully');
console.log('');
console.log('📱 The application is now optimized for UniHiker M10');
console.log('To deploy to the device:');
console.log('1. Copy the dist directory to the UniHiker');
console.log('2. Run the start-lark.sh script on the device');
console.log('3. Access LARK via the UniHiker web browser');
