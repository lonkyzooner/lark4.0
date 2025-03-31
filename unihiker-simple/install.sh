#!/bin/bash
# LARK UniHiker Installation Script

echo "Installing LARK on UniHiker M10..."

# Make the server script executable
chmod +x serve.py

# Create a desktop shortcut
cat > ~/Desktop/LARK.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=LARK
Comment=Law Enforcement Assistance and Response Kit
Exec=python3 $(pwd)/serve.py
Icon=web-browser
Terminal=true
Categories=Utility;
EOF

chmod +x ~/Desktop/LARK.desktop

echo "Installation complete!"
echo ""
echo "To start LARK:"
echo "1. Double-click the LARK icon on your desktop, or"
echo "2. Run: python3 $(pwd)/serve.py"
echo ""
echo "Then open your web browser and navigate to: http://localhost:8080"
