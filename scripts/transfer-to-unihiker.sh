#!/bin/bash
# Script to transfer LARK standalone demo to UniHiker M10

# Default values
UNIHIKER_IP="192.168.1.1"  # Default IP, will be overridden by user input
UNIHIKER_USER="pi"         # Default username for UniHiker
TARGET_DIR="/home/pi"      # Default target directory on UniHiker

# Function to display usage information
usage() {
  echo "Usage: $0 [options]"
  echo "Options:"
  echo "  -i, --ip IP_ADDRESS    IP address of the UniHiker (required)"
  echo "  -u, --user USERNAME    Username for SSH login (default: pi)"
  echo "  -d, --dir DIRECTORY    Target directory on UniHiker (default: /home/pi)"
  echo "  -h, --help             Display this help message"
  exit 1
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -i|--ip)
      UNIHIKER_IP="$2"
      shift 2
      ;;
    -u|--user)
      UNIHIKER_USER="$2"
      shift 2
      ;;
    -d|--dir)
      TARGET_DIR="$2"
      shift 2
      ;;
    -h|--help)
      usage
      ;;
    *)
      echo "Error: Unknown option $1"
      usage
      ;;
  esac
done

# Check if IP address is provided
if [[ "$UNIHIKER_IP" == "192.168.1.1" ]]; then
  echo "Error: UniHiker IP address is required"
  usage
fi

echo "🚀 Transferring LARK to UniHiker M10..."
echo "IP Address: $UNIHIKER_IP"
echo "Username: $UNIHIKER_USER"
echo "Target Directory: $TARGET_DIR"

# Create a temporary directory for the files
TEMP_DIR=$(mktemp -d)
echo "Creating temporary directory: $TEMP_DIR"

# Copy the standalone demo to the temp directory
cp ../standalone-demo.html "$TEMP_DIR/lark.html"

# Create a simple startup script
cat > "$TEMP_DIR/start-lark.sh" << 'EOF'
#!/bin/bash
# LARK Startup Script for UniHiker M10

echo "Starting LARK on UniHiker M10..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
  echo "Error: Python 3 is not installed"
  exit 1
fi

# Start a simple HTTP server
echo "Starting web server on port 8080..."
python3 -m http.server 8080 &
SERVER_PID=$!

# Open the browser (if available)
if command -v chromium-browser &> /dev/null; then
  echo "Opening LARK in browser..."
  sleep 2
  chromium-browser http://localhost:8080/lark.html &
elif command -v firefox &> /dev/null; then
  echo "Opening LARK in browser..."
  sleep 2
  firefox http://localhost:8080/lark.html &
else
  echo "No browser found. Please open http://localhost:8080/lark.html manually."
fi

echo ""
echo "LARK is now running!"
echo "Access it at: http://localhost:8080/lark.html"
echo ""
echo "Press Ctrl+C to stop the server"

# Wait for user to press Ctrl+C
trap "kill $SERVER_PID; echo 'Server stopped'; exit" INT
wait
EOF

# Make the startup script executable
chmod +x "$TEMP_DIR/start-lark.sh"

# Create a README file
cat > "$TEMP_DIR/README.txt" << 'EOF'
LARK for UniHiker M10
=====================

This is a simplified version of the LARK (Law Enforcement Assistance and Response Kit)
application specifically designed for the UniHiker M10 device.

To start LARK:
1. Run the startup script: ./start-lark.sh
2. Open your browser and navigate to: http://localhost:8080/lark.html

If the browser doesn't open automatically, you can manually open it and
navigate to the URL mentioned above.

Features:
- Voice-first interface with visual feedback
- Simulated wake word detection ("Hey LARK")
- Visual feedback for different states (idle, listening, processing, responding)
- No microphone permissions required
EOF

# Transfer files to the UniHiker
echo "Transferring files to UniHiker..."
scp -r "$TEMP_DIR/"* "$UNIHIKER_USER@$UNIHIKER_IP:$TARGET_DIR"

# Check if transfer was successful
if [ $? -eq 0 ]; then
  echo "✅ Transfer successful!"
  echo ""
  echo "To start LARK on the UniHiker:"
  echo "1. SSH into the UniHiker: ssh $UNIHIKER_USER@$UNIHIKER_IP"
  echo "2. Navigate to the directory: cd $TARGET_DIR"
  echo "3. Run the startup script: ./start-lark.sh"
  echo ""
  echo "Or you can run these commands remotely:"
  echo "ssh $UNIHIKER_USER@$UNIHIKER_IP \"cd $TARGET_DIR && ./start-lark.sh\""
else
  echo "❌ Transfer failed. Please check your connection and try again."
fi

# Clean up temporary directory
rm -rf "$TEMP_DIR"
echo "Cleaned up temporary files"
