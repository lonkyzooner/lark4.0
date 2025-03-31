#!/usr/bin/env python3
"""
LARK Browser Launcher - Launches a browser to connect to the LARK web server
This approach avoids the GUI library limitations of the UniHiker
"""
import subprocess
import time
import socket
import os

# Web server connection settings
SERVER_IP = "10.1.2.101"  # Your Mac's IP address
SERVER_PORT = 8088
SERVER_URL = f"http://{SERVER_IP}:{SERVER_PORT}"

def check_server_connection():
    """Check if the LARK web server is accessible"""
    try:
        # Try to connect to the server
        socket.create_connection((SERVER_IP, SERVER_PORT), timeout=2)
        print(f"✅ Connected to LARK server at {SERVER_URL}")
        return True
    except:
        print(f"❌ Could not connect to LARK server at {SERVER_URL}")
        return False

def launch_browser():
    """Launch the browser to connect to the LARK web server"""
    try:
        # First try with chromium
        print("Attempting to launch Chromium browser...")
        subprocess.run(["chromium-browser", "--kiosk", SERVER_URL], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
        return True
    except:
        try:
            # Then try with firefox
            print("Attempting to launch Firefox browser...")
            subprocess.run(["firefox", "--kiosk", SERVER_URL], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
            return True
        except:
            try:
                # Then try with midori
                print("Attempting to launch Midori browser...")
                subprocess.run(["midori", "-e", "Fullscreen", SERVER_URL], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
                return True
            except:
                # Finally try with any available browser
                print("Attempting to launch any available browser...")
                subprocess.run(["x-www-browser", SERVER_URL], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
                return True

def main():
    """Main function"""
    print("LARK Browser Launcher")
    print("=====================")
    
    # Check if server is running
    print(f"Checking connection to LARK server at {SERVER_URL}...")
    if not check_server_connection():
        print("Please make sure the LARK web server is running on your Mac.")
        print(f"Server should be accessible at {SERVER_URL}")
        print("You can start it by running 'node server.js' in the web-lark directory.")
        
        # Ask if user wants to continue anyway
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Exiting. Please start the server and try again.")
            return
    
    # Launch browser
    print("Launching browser to connect to LARK web server...")
    if launch_browser():
        print("Browser launched successfully!")
    else:
        print("Failed to launch browser.")
        print("Please manually open a browser and navigate to:")
        print(SERVER_URL)
    
    print("\nPress Ctrl+C to exit")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting LARK Browser Launcher")

if __name__ == "__main__":
    main()
