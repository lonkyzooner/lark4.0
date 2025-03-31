# LARK v1.2 - Law Enforcement Assistance and Response Kit

## Overview
LARK (Law Enforcement Assistance and Response Kit) is a voice-activated assistant designed for the UniHiker M10. It provides law enforcement officers with hands-free access to Miranda rights recitation and Louisiana statute lookups.

## Features
- Voice-activated interface
- Visual state indicators (Ready, Listening, Processing, Responding)
- Miranda rights recitation
- Louisiana statute lookup
- Automatic demo mode when not in use
- Minimal, efficient code optimized for the UniHiker display

## Hardware Requirements
- DFRobot UniHiker M10 with 2.8-inch touchscreen
- Built-in microphone
- Speaker (built-in or USB)

## Installation
1. Edit the `deploy_lark_v1.2.sh` script to set your UniHiker's IP address
2. Run the deployment script:
   ```
   chmod +x deploy_lark_v1.2.sh
   ./deploy_lark_v1.2.sh
   ```
3. The script will:
   - Transfer files to the UniHiker
   - Install required dependencies (espeak, alsa-utils)
   - Create a desktop shortcut
   - Set up autostart

## Usage
LARK will start automatically when the UniHiker boots. You can also start it manually by clicking the LARK desktop shortcut.

### Voice Commands
- Say "Miranda" to hear Miranda rights
- Say "Statute" to hear Louisiana DWI statute information

### Visual Indicators
- Blue circle: Ready (waiting for commands)
- Green circle: Listening (recording audio)
- Yellow circle: Processing (analyzing command)
- Purple circle: Responding (speaking information)

## Files
- `lark_v1.2_integrated.py`: Main application (integrated version)
- `deploy_lark_v1.2.sh`: Deployment script

## Troubleshooting
- If the microphone isn't working, ensure alsa-utils is installed
- If text-to-speech isn't working, ensure espeak is installed
- If the display looks incorrect, the application uses absolute positioning that should work on all UniHiker M10 devices

## Version History
- v1.0: Initial prototype
- v1.1: Improved display and voice recognition
- v1.2: Fully integrated version with reliable display and voice functionality
