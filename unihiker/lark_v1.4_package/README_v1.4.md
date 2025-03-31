# LARK v1.4 - Law Enforcement Assistance and Response Kit

## Overview
LARK v1.4 features a completely redesigned web-style UI that matches modern law enforcement tools. It provides a clean, professional interface with visual state indicators and improved user feedback.

## Features
- Web-style UI with dark blue law enforcement theme
- Status indicators for microphone and battery
- Large central LARK logo with pulsing animation
- Visual state changes (Ready → Listening → Processing → Responding)
- Miranda rights recitation
- Louisiana statute lookup
- Automatic demo mode

## Files
- `lark_v1.4.py` - Main application with web-style UI

## Manual Installation on UniHiker

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
   scp lark_v1.4.py root@[UniHiker-IP-Address]:~/lark/lark.py
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
   Name=LARK v1.4
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

### Visual Indicators
- Blue pulsing circle: Ready (waiting for commands)
- Green circle: Listening (recording audio)
- Yellow circle: Processing (analyzing command)
- Purple circle: Responding (speaking information)

## Troubleshooting
- If the microphone isn't working, ensure alsa-utils is installed
- If text-to-speech isn't working, ensure espeak is installed
- If the display looks incorrect, try rebooting the UniHiker

## Version History
- v1.0-1.2: Initial prototypes with basic functionality
- v1.3: Enhanced UI with law enforcement theme
- v1.4: Web-style UI with improved visual feedback and animations
