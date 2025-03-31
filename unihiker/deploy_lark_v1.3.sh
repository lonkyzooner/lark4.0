#!/bin/bash
# LARK v1.3 Deployment Script
# Enhanced UI version with badass law enforcement theme

# Colors for terminal output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "===== LARK v1.3 Deployment ====="
echo "Law Enforcement Assistance and Response Kit"
echo -e "${NC}"

# UniHiker IP address
UNIHIKER_IP="10.1.2.3"
UNIHIKER_USER="root"
LARK_DIR="/root/lark"

# Check if UniHiker is reachable
echo -e "${YELLOW}Checking connection to UniHiker...${NC}"
ping -c 1 $UNIHIKER_IP > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Cannot reach UniHiker at $UNIHIKER_IP${NC}"
    echo "Please check the connection and try again."
    exit 1
fi
echo -e "${GREEN}UniHiker is reachable${NC}"

# Create directory on UniHiker
echo -e "${YELLOW}Creating directory on UniHiker...${NC}"
ssh $UNIHIKER_USER@$UNIHIKER_IP "mkdir -p $LARK_DIR"

# Transfer LARK files
echo -e "${YELLOW}Transferring LARK files...${NC}"
scp /Users/bscott/Downloads/L.A.R.K/unihiker/lark_v1.3.py $UNIHIKER_USER@$UNIHIKER_IP:$LARK_DIR/lark.py

# Make files executable
echo -e "${YELLOW}Making files executable...${NC}"
ssh $UNIHIKER_USER@$UNIHIKER_IP "chmod +x $LARK_DIR/lark.py"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
ssh $UNIHIKER_USER@$UNIHIKER_IP "apt-get update && apt-get install -y espeak alsa-utils"

# Create desktop shortcut
echo -e "${YELLOW}Creating desktop shortcut...${NC}"
ssh $UNIHIKER_USER@$UNIHIKER_IP "mkdir -p /root/Desktop"
ssh $UNIHIKER_USER@$UNIHIKER_IP "cat > /root/Desktop/LARK.desktop << EOF
[Desktop Entry]
Type=Application
Name=LARK v1.3
Comment=Law Enforcement Assistant
Exec=python $LARK_DIR/lark.py
Icon=utilities-terminal
Terminal=false
Categories=Utility;
EOF"
ssh $UNIHIKER_USER@$UNIHIKER_IP "chmod +x /root/Desktop/LARK.desktop"

# Set up autostart
echo -e "${YELLOW}Setting up autostart...${NC}"
ssh $UNIHIKER_USER@$UNIHIKER_IP "mkdir -p /root/.config/autostart"
ssh $UNIHIKER_USER@$UNIHIKER_IP "cp /root/Desktop/LARK.desktop /root/.config/autostart/"

# Test LARK
echo -e "${YELLOW}Testing LARK...${NC}"
ssh $UNIHIKER_USER@$UNIHIKER_IP "python $LARK_DIR/lark.py &" &
echo "LARK is starting on the UniHiker"

# Completion message
echo -e "${BLUE}===== Deployment Complete =====${NC}"
echo "LARK v1.3 has been deployed to your UniHiker."
echo "The application will start automatically on boot."
echo "To run manually: Click the LARK desktop shortcut on UniHiker"
