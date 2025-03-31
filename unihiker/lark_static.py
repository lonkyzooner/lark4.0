#!/usr/bin/env python3
"""
LARK Static - Ultra-minimal version with NO animations or threading
"""
from unihiker import GUI
import time
import subprocess
import socket

# Initialize GUI
gui = GUI()

# Colors - using standard color names that UniHiker supports
DARK_BLUE = "navy"
HEADER_BLUE = "darkblue"
CIRCLE_BLUE = "blue"
GREEN = "green"
RED = "red"
WHITE = "white"

# Web server connection settings
SERVER_IP = "10.1.2.101"
SERVER_PORT = 8088
CONNECTION_STATUS = "Unknown"

def check_server_connection():
    """Check if the LARK web server is accessible"""
    global CONNECTION_STATUS
    try:
        # Try to connect to the server
        socket.create_connection((SERVER_IP, SERVER_PORT), timeout=2)
        CONNECTION_STATUS = "Connected"
        return True
    except:
        CONNECTION_STATUS = "Disconnected"
        return False

def draw_static_ui():
    """Draw a completely static UI with no animations"""
    # Clear screen with dark background
    gui.clear()
    gui.draw_rect(x=0, y=0, w=240, h=240, color=DARK_BLUE)
    
    # Draw header
    gui.draw_rect(x=0, y=0, w=240, h=30, color=HEADER_BLUE)
    gui.draw_text(text="LARK", x=50, y=15, color=WHITE)
    
    # Draw connection status
    color = GREEN if CONNECTION_STATUS == "Connected" else RED
    gui.draw_circle(x=200, y=15, r=5, color=color)
    
    # Draw main circle - simple blue circle
    gui.draw_circle(x=120, y=120, r=40, color=CIRCLE_BLUE)
    gui.draw_circle(x=120, y=120, r=38, color=DARK_BLUE)
    
    # Draw status text
    gui.draw_text(text="Ready", x=120, y=170, color=WHITE)
    
    # Draw message box
    gui.draw_rect(x=20, y=200, w=200, h=30, color=HEADER_BLUE)
    gui.draw_text(text="LARK Web Client", x=120, y=215, color=WHITE)

def speak(text):
    """Speak text using espeak"""
    try:
        subprocess.run(["espeak", "-v", "en-us", text], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
    except:
        print(f"Would speak: {text}")

def main():
    """Main function - completely static, no threads"""
    try:
        # Check connection
        check_server_connection()
        
        # Draw static UI once
        draw_static_ui()
        
        # Announce startup
        speak("LARK static version activated")
        
        # Wait for user to press Ctrl+C to exit
        print("Press Ctrl+C to exit")
        while True:
            time.sleep(10)
            # Check connection every 10 seconds but don't redraw UI
            check_server_connection()
            
    except KeyboardInterrupt:
        gui.clear()
        print("Exiting LARK")

if __name__ == "__main__":
    main()
