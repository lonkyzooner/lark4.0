#!/usr/bin/env python3
"""
LARK Minimal - Simplified version with minimal animations to prevent strobing
"""
from unihiker import GUI
import time
import threading
import subprocess
import os
import socket

# Initialize GUI
gui = GUI()

# States
STATE_READY = 0
STATE_LISTENING = 1
STATE_PROCESSING = 2
STATE_RESPONDING = 3

# Current state
current_state = STATE_READY
mic_active = False

# Colors - using standard color names that UniHiker supports
DARK_BLUE = "navy"
HEADER_BLUE = "darkblue"
CIRCLE_BLUE = "blue"
GREEN = "green"
YELLOW = "yellow"
PURPLE = "purple"
RED = "red"
WHITE = "white"

# State colors
STATE_COLORS = [CIRCLE_BLUE, GREEN, YELLOW, PURPLE]

# Miranda rights (simplified)
MIRANDA_RIGHTS = [
    "You have the right to remain silent.",
    "Anything you say can be used against you in court.",
    "You have the right to an attorney.",
    "If you cannot afford an attorney, one will be appointed for you."
]

# Web server connection settings
SERVER_IP = "10.1.2.101"
SERVER_PORT = 8088
SERVER_URL = f"http://{SERVER_IP}:{SERVER_PORT}"
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

def draw_ui():
    """Draw the UI with minimal animations"""
    # Clear screen with dark background
    gui.clear()
    gui.draw_rect(x=0, y=0, w=240, h=240, color=DARK_BLUE)
    
    # Draw header
    gui.draw_rect(x=0, y=0, w=240, h=30, color=HEADER_BLUE)
    gui.draw_text(text="LARK", x=50, y=15, color=WHITE)
    
    # Draw connection status
    color = GREEN if CONNECTION_STATUS == "Connected" else RED
    gui.draw_circle(x=200, y=15, r=5, color=color)
    
    # Draw main circle
    circle_color = STATE_COLORS[current_state]
    gui.draw_circle(x=120, y=120, r=40, color=circle_color)
    gui.draw_circle(x=120, y=120, r=38, color=DARK_BLUE)
    
    # Draw status text
    status_texts = [
        "Ready",
        "Listening",
        "Processing",
        "Responding"
    ]
    gui.draw_text(text=status_texts[current_state], x=120, y=170, color=WHITE)
    
    # Draw message box
    gui.draw_rect(x=20, y=200, w=200, h=30, color=HEADER_BLUE)
    
    # Show simple message
    if current_state == STATE_READY:
        message = "Say Hey LARK"
    elif current_state == STATE_LISTENING:
        message = "Listening..."
    elif current_state == STATE_PROCESSING:
        message = "Processing..."
    else:
        message = "Miranda Rights"
    
    gui.draw_text(text=message, x=120, y=215, color=WHITE)

def speak(text):
    """Speak text using espeak"""
    try:
        subprocess.run(["espeak", "-v", "en-us", text], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
    except:
        print(f"Would speak: {text}")

def run_miranda_demo():
    """Run Miranda rights demo"""
    global current_state, mic_active
    
    # Listening state
    current_state = STATE_LISTENING
    mic_active = True
    draw_ui()
    time.sleep(2)
    
    # Processing state
    current_state = STATE_PROCESSING
    draw_ui()
    time.sleep(2)
    
    # Responding state
    current_state = STATE_RESPONDING
    draw_ui()
    time.sleep(1)
    
    for right in MIRANDA_RIGHTS:
        speak(right)
        time.sleep(3)
    
    # Back to ready state
    current_state = STATE_READY
    mic_active = False
    draw_ui()

def ui_update_thread():
    """Thread to update UI - with very slow refresh rate"""
    while True:
        draw_ui()
        time.sleep(2)  # Only refresh every 2 seconds

def main():
    """Main function"""
    try:
        # Initial display
        check_server_connection()
        draw_ui()
        speak("LARK minimal activated")
        
        # Start UI update thread with slow refresh
        ui_thread = threading.Thread(target=ui_update_thread)
        ui_thread.daemon = True
        ui_thread.start()
        
        # Run demo after 5 seconds
        time.sleep(5)
        run_miranda_demo()
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        gui.clear()
        print("Exiting LARK")

if __name__ == "__main__":
    main()
