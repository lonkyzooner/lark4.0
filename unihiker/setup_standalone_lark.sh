#!/bin/bash
# Setup script for standalone LARK on UniHiker
# This script installs Node.js and sets up the LARK web server

echo "Setting up standalone LARK on UniHiker..."
echo "=========================================="

# Create directory structure
echo "Creating directory structure..."
mkdir -p /root/lark/web-lark

# Install Node.js if not already installed
if ! command -v node &> /dev/null; then
    echo "Installing Node.js..."
    apt-get update
    apt-get install -y nodejs npm
fi

# Copy files from USB drive if available, otherwise instruct manual copy
if [ -d "/media/usb/L.A.R.K" ]; then
    echo "Found LARK files on USB drive, copying..."
    cp -r /media/usb/L.A.R.K/web-lark/* /root/lark/web-lark/
    cp /media/usb/L.A.R.K/unihiker/lark_unihiker.html /root/lark/web-lark/
else
    echo "Please copy the LARK files to /root/lark/web-lark/ manually"
    echo "You'll need to copy:"
    echo "  - All files from the web-lark directory"
    echo "  - The lark_unihiker.html file from the unihiker directory"
fi

# Create startup script
echo "Creating startup script..."
cat > /root/lark/start_lark.sh << 'EOL'
#!/bin/bash
# Start script for LARK on UniHiker

# Change to the LARK directory
cd /root/lark/web-lark

# Start the LARK web server
node server.js &

# Wait for server to start
sleep 3

# Launch browser in kiosk mode
if command -v chromium-browser &> /dev/null; then
    chromium-browser --kiosk http://localhost:8088 &
elif command -v firefox &> /dev/null; then
    firefox --kiosk http://localhost:8088 &
elif command -v midori &> /dev/null; then
    midori -e Fullscreen http://localhost:8088 &
else
    x-www-browser http://localhost:8088 &
fi

echo "LARK started! Press Ctrl+C to exit."
wait
EOL

# Make startup script executable
chmod +x /root/lark/start_lark.sh

# Create modified server.js for local use
cat > /root/lark/web-lark/server.js << 'EOL'
const express = require('express');
const path = require('path');
const app = express();
const port = 8088;

// Middleware for JSON parsing
app.use(express.json());

// Serve static files from the current directory
app.use(express.static(__dirname));

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'lark_unihiker.html'));
});

// API endpoint for commands
app.post('/api/command', (req, res) => {
  const command = req.body.command;
  console.log('Received command:', command);
  
  // Process command locally
  // This would integrate with local TTS or other functionality
  
  res.json({ status: 'success', message: 'Command received' });
});

// Status endpoint
app.get('/api/status', (req, res) => {
  res.json({ status: 'online' });
});

// Start the server
app.listen(port, 'localhost', () => {
  console.log(`LARK web interface running at http://localhost:${port}`);
});
EOL

# Create package.json
cat > /root/lark/web-lark/package.json << 'EOL'
{
  "name": "lark-web",
  "version": "1.0.0",
  "description": "LARK Web Interface for UniHiker",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.2"
  }
}
EOL

# Install dependencies
echo "Installing Node.js dependencies..."
cd /root/lark/web-lark
npm install

# Create autostart entry if possible
if [ -d "/etc/xdg/autostart" ]; then
    echo "Creating autostart entry..."
    cat > /etc/xdg/autostart/lark.desktop << 'EOL'
[Desktop Entry]
Type=Application
Name=LARK
Comment=LARK Law Enforcement Assistant
Exec=/root/lark/start_lark.sh
Terminal=false
X-GNOME-Autostart-enabled=true
EOL
fi

echo ""
echo "Setup complete!"
echo "To start LARK, run: /root/lark/start_lark.sh"
echo ""
echo "To make LARK start automatically on boot:"
echo "1. Add this line to /etc/rc.local before 'exit 0':"
echo "   /root/lark/start_lark.sh &"
echo ""
echo "Note: You may need to install additional packages:"
echo "- For text-to-speech: apt-get install espeak"
echo "- For browser: apt-get install chromium-browser"
