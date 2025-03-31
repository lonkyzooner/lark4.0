#!/bin/bash
# Simple deployment script for LARK on UniHiker M10

echo "Creating simple deployment for UniHiker..."

# Create a deployment directory
DEPLOY_DIR="unihiker-deploy"
mkdir -p $DEPLOY_DIR

# Copy the standalone demo file
cp ../unihiker-demo.html $DEPLOY_DIR/index.html

# Copy any necessary assets
mkdir -p $DEPLOY_DIR/sounds
cp -r ../public/sounds/* $DEPLOY_DIR/sounds/

# Create a simple server script
cat > $DEPLOY_DIR/serve.py << 'EOF'
#!/usr/bin/env python3
"""
Simple HTTP server for LARK on UniHiker
"""
import http.server
import socketserver
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

print(f"Starting server at http://localhost:{PORT}")
print(f"Serving files from: {DIRECTORY}")
print("Press Ctrl+C to stop")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
EOF

# Make the server script executable
chmod +x $DEPLOY_DIR/serve.py

# Create a README file
cat > $DEPLOY_DIR/README.txt << 'EOF'
LARK for UniHiker M10 - Simple Deployment

To run the application:
1. Copy this entire directory to the UniHiker M10
2. On the UniHiker, navigate to this directory
3. Run: python3 serve.py
4. Open a web browser and go to: http://localhost:8080

If you encounter any issues:
- Make sure Python 3 is installed on the UniHiker
- Check that port 8080 is not in use
- Ensure the UniHiker has a working web browser
EOF

echo "Simple deployment created in: $DEPLOY_DIR"
echo "To deploy to UniHiker:"
echo "1. Copy the $DEPLOY_DIR directory to the UniHiker"
echo "2. Run: python3 serve.py"
echo "3. Open browser to http://localhost:8080"
