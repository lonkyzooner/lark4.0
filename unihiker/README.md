# LARK v1.2 - Law Enforcement Assistance and Response Kit

## Overview
LARK (Law Enforcement Assistance and Response Kit) is a voice-activated assistant designed for the UniHiker M10. It provides law enforcement officers with hands-free access to Miranda rights recitation and Louisiana statute lookups.

## Features
- Voice-activated interface with wake word detection
- Visual state indicators (Ready, Listening, Processing, Responding)
- Miranda rights recitation
- Louisiana statute lookup
- Automatic demo mode when not in use
- Minimal, efficient code optimized for the UniHiker display

## Hardware Requirements
- DFRobot UniHiker M10 with 2.8-inch touchscreen
- Built-in microphone
- Speaker (built-in or USB)

## Files
- `lark_v1.2.py`: Main application with all functionality integrated
- `lark.py`: Renamed version of lark_v1.2.py for deployment

## Installation on UniHiker
1. Connect to your UniHiker via SSH:
   ```
   ssh root@[UniHiker-IP-Address]
   ```

2. Create the LARK directory:
   ```
   mkdir -p ~/lark
   ```

3. Copy the LARK files to the UniHiker:
   ```
   # From your local machine:
   scp lark_v1.2.py root@[UniHiker-IP-Address]:~/lark/lark.py
   ```

4. Install dependencies on the UniHiker:
   ```
   apt-get update && apt-get install -y espeak alsa-utils
   ```

5. Make the script executable:
   ```
   chmod +x ~/lark/lark.py
   ```

6. Create a desktop shortcut:
   ```
   mkdir -p ~/Desktop
   cat > ~/Desktop/LARK.desktop << EOF
   [Desktop Entry]
   Type=Application
   Name=LARK v1.2
   Comment=Law Enforcement Assistant
   Exec=python ~/lark/lark.py
   Icon=utilities-terminal
   Terminal=false
   EOF
   chmod +x ~/Desktop/LARK.desktop
   ```

7. Set up autostart:
   ```
   mkdir -p ~/.config/autostart
   cp ~/Desktop/LARK.desktop ~/.config/autostart/
   ```

## Usage
LARK will start automatically when the UniHiker boots. You can also start it manually by clicking the LARK desktop shortcut or running:
```
python ~/lark/lark.py
```

### Voice Commands
- Say "Miranda" to hear Miranda rights
- Say "Statute" to hear Louisiana DWI statute information

### Visual Indicators
- Blue circle: Ready (waiting for commands)
- Green circle: Listening (recording audio)
- Yellow circle: Processing (analyzing command)
- Purple circle: Responding (speaking information)

## Troubleshooting
- If the microphone isn't working, ensure alsa-utils is installed
- If text-to-speech isn't working, ensure espeak is installed
- If the display looks incorrect, try rebooting the UniHiker

## Version History
- v1.0: Initial prototype
- v1.1: Improved display and voice recognition
- v1.2: Fully integrated version with reliable display and voice functionality
