#!/bin/bash
# LARK v1.2 Deployment Script
# Transfers LARK files to the UniHiker and sets up dependencies

# Set your UniHiker's IP address here
UNIHIKER_IP="10.1.2.3"  # Change this to your actual IP
UNIHIKER_USER="root"
LARK_DIR="/root/lark"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}===== LARK v1.2 Deployment =====${NC}"

# Check connection
echo -e "${YELLOW}Checking connection to UniHiker...${NC}"
ping -c 1 $UNIHIKER_IP > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${RED}Cannot reach UniHiker at $UNIHIKER_IP${NC}"
    echo "Please check the IP address and ensure the UniHiker is connected."
    exit 1
fi
echo -e "${GREEN}UniHiker is reachable${NC}"

# Create directory
echo -e "${YELLOW}Creating directory on UniHiker...${NC}"
ssh $UNIHIKER_USER@$UNIHIKER_IP "mkdir -p $LARK_DIR"

# Transfer files
echo -e "${YELLOW}Transferring LARK files...${NC}"
scp lark_v1.2_integrated.py $UNIHIKER_USER@$UNIHIKER_IP:$LARK_DIR/lark.py
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to transfer main LARK file${NC}"
    exit 1
fi

# Make executable
echo -e "${YELLOW}Making files executable...${NC}"
ssh $UNIHIKER_USER@$UNIHIKER_IP "chmod +x $LARK_DIR/*.py"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
ssh $UNIHIKER_USER@$UNIHIKER_IP "apt-get update && apt-get install -y espeak alsa-utils"

# Create desktop shortcut
echo -e "${YELLOW}Creating desktop shortcut...${NC}"
ssh $UNIHIKER_USER@$UNIHIKER_IP "mkdir -p /root/Desktop"
ssh $UNIHIKER_USER@$UNIHIKER_IP "cat > /root/Desktop/LARK.desktop << EOF
[Desktop Entry]
Type=Application
Name=LARK
Comment=Law Enforcement Assistant
Exec=python $LARK_DIR/lark.py
Icon=utilities-terminal
Terminal=false
EOF"

# Create autostart entry
echo -e "${YELLOW}Setting up autostart...${NC}"
ssh $UNIHIKER_USER@$UNIHIKER_IP "mkdir -p /root/.config/autostart"
ssh $UNIHIKER_USER@$UNIHIKER_IP "cp /root/Desktop/LARK.desktop /root/.config/autostart/"

# Test run
echo -e "${YELLOW}Testing LARK...${NC}"
ssh $UNIHIKER_USER@$UNIHIKER_IP "cd $LARK_DIR && python lark.py &" &
echo -e "${GREEN}LARK is starting on the UniHiker${NC}"

echo -e "${GREEN}===== Deployment Complete =====${NC}"
echo "LARK v1.2 has been deployed to your UniHiker."
echo "The application will start automatically on boot."
echo "To run manually: Click the LARK desktop shortcut on UniHiker"
