LARK v1.4 - INSTALLATION INSTRUCTIONS
=================================

This package contains the LARK v1.4 application with the new web-style UI
designed specifically for the UniHiker M10.

QUICK INSTALLATION:
------------------
1. Copy this entire folder to your UniHiker
2. SSH into your UniHiker
3. Navigate to the folder
4. Run: bash setup.sh

MANUAL INSTALLATION:
------------------
If the setup script doesn't work, follow these steps:

1. Copy lark.py to /root/lark/ on your UniHiker
2. Make it executable: chmod +x /root/lark/lark.py
3. Install dependencies: apt-get install -y espeak alsa-utils
4. Create a desktop shortcut (see README_v1.4.md for details)

FEATURES:
--------
- Web-style UI with law enforcement blue theme
- Status indicators for microphone and battery
- Visual state feedback with animations
- Miranda rights recitation
- Louisiana statute lookup

For more details, see the included README_v1.4.md file.

TROUBLESHOOTING:
--------------
- If you have display issues, try rebooting the UniHiker
- Ensure the microphone and speaker are properly connected
- Check that espeak and alsa-utils are installed

For support, contact the LARK development team.
