#!/bin/bash
# LARK v1.4 Setup Script
# For manual installation on UniHiker M10

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print banner
echo -e "${BLUE}"
echo "====================================="
echo "  LARK v1.4 Setup Script"
echo "  Law Enforcement Assistance and Response Kit"
echo "====================================="
echo -e "${NC}"

# Install required packages
echo -e "${YELLOW}Installing required packages...${NC}"
apt-get update && apt-get install -y espeak alsa-utils
if [ $? -ne 0 ]; then
    echo -e "${RED}Warning: Failed to install some packages. LARK may have limited functionality.${NC}"
else
    echo -e "${GREEN}Required packages installed.${NC}"
fi

# Create LARK directory
echo -e "${YELLOW}Setting up LARK...${NC}"
mkdir -p /root/lark
cp lark.py /root/lark/
chmod +x /root/lark/lark.py
echo -e "${GREEN}LARK files installed.${NC}"

# Create desktop shortcut
echo -e "${YELLOW}Creating desktop shortcut...${NC}"
mkdir -p /root/Desktop
cat > /root/Desktop/LARK.desktop << EOF
[Desktop Entry]
Type=Application
Name=LARK v1.4
Comment=Law Enforcement Assistant
Exec=python /root/lark/lark.py
Icon=utilities-terminal
Terminal=false
Categories=Utility;
EOF

chmod +x /root/Desktop/LARK.desktop
echo -e "${GREEN}Desktop shortcut created.${NC}"

# Create autostart entry
echo -e "${YELLOW}Setting up autostart...${NC}"
mkdir -p /root/.config/autostart
cp /root/Desktop/LARK.desktop /root/.config/autostart/
echo -e "${GREEN}Autostart configured.${NC}"

echo -e "${BLUE}"
echo "====================================="
echo "  LARK v1.4 Setup Complete!"
echo "====================================="
echo -e "${NC}"
echo "To start LARK, either:"
echo "1. Click the LARK desktop shortcut"
echo "2. Run: python /root/lark/lark.py"
echo ""
echo "LARK will also start automatically when the UniHiker boots up."
echo ""
echo "Enjoy using LARK v1.4!"
