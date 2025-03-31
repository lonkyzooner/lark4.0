#!/usr/bin/env python3
"""
LARK Simple - Extremely simplified version for UniHiker
Uses direct button press detection instead of event callbacks
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
YELLOW = "yellow"
PURPLE = "purple"
RED = "red"
WHITE = "white"

# Current status
STATUS_MESSAGE = "Ready"
CONNECTION_STATUS = "Unknown"

# Web server connection settings
SERVER_IP = "10.1.2.101"
SERVER_PORT = 8088

# Miranda rights (simplified)
MIRANDA_RIGHTS = [
    "You have the right to remain silent.",
    "Anything you say can be used against you in court.",
    "You have the right to an attorney.",
    "If you cannot afford an attorney, one will be appointed for you."
]

# Louisiana statutes (minimal set)
STATUTES = {
    "14:98": "DWI - Operating vehicle while intoxicated",
    "14:30": "First degree murder",
    "14:67": "Theft"
}

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
    """Draw the UI with buttons"""
    global STATUS_MESSAGE
    
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
    gui.draw_circle(x=120, y=100, r=30, color=CIRCLE_BLUE)
    gui.draw_circle(x=120, y=100, r=28, color=DARK_BLUE)
    gui.draw_text(text="LARK", x=120, y=100, color=WHITE)
    
    # Draw status text
    gui.draw_text(text=STATUS_MESSAGE, x=120, y=140, color=WHITE)
    
    # Draw buttons
    draw_button(x=60, y=170, w=100, h=30, text="Miranda", color=PURPLE)
    draw_button(x=180, y=170, w=100, h=30, text="Statute", color=GREEN)
    draw_button(x=120, y=210, w=200, h=30, text="Check Connection", color=YELLOW)

def draw_button(x, y, w, h, text, color):
    """Draw a button with text"""
    # Draw button background
    gui.draw_rect(x=x-(w//2), y=y-(h//2), w=w, h=h, color=color)
    
    # Draw button text
    gui.draw_text(text=text, x=x, y=y, color=WHITE)

def speak(text):
    """Speak text using espeak"""
    try:
        subprocess.run(["espeak", "-v", "en-us", text], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
    except:
        print(f"Would speak: {text}")

def check_button_press(x, y):
    """Check if a button was pressed at coordinates x,y"""
    global STATUS_MESSAGE
    
    # Miranda button (60, 170)
    if 10 <= x <= 110 and 155 <= y <= 185:
        STATUS_MESSAGE = "Miranda Rights"
        draw_ui()
        run_miranda()
        return True
    
    # Statute button (180, 170)
    elif 130 <= x <= 230 and 155 <= y <= 185:
        STATUS_MESSAGE = "Statute Lookup"
        draw_ui()
        run_statute()
        return True
    
    # Check Connection button (120, 210)
    elif 20 <= x <= 220 and 195 <= y <= 225:
        STATUS_MESSAGE = "Checking..."
        draw_ui()
        if check_server_connection():
            STATUS_MESSAGE = "Connected"
        else:
            STATUS_MESSAGE = "Disconnected"
        draw_ui()
        return True
    
    return False

def run_miranda():
    """Run Miranda rights demo"""
    # Speak Miranda rights
    for right in MIRANDA_RIGHTS:
        speak(right)
        time.sleep(3)  # Pause between rights
    
    # Reset status
    global STATUS_MESSAGE
    STATUS_MESSAGE = "Ready"
    draw_ui()

def run_statute():
    """Run statute lookup demo"""
    statute = "14:98"  # DWI statute
    
    # Speak statute
    speak(f"Louisiana Statute {statute}")
    time.sleep(2)
    speak(STATUTES[statute])
    time.sleep(2)
    
    # Reset status
    global STATUS_MESSAGE
    STATUS_MESSAGE = "Ready"
    draw_ui()

def main():
    """Main function with manual button detection"""
    try:
        # Check connection
        check_server_connection()
        
        # Draw initial UI
        draw_ui()
        
        # Announce startup
        speak("LARK simple version activated")
        
        # Simple button detection loop
        while True:
            # Check for touch events manually
            touch = gui.get_touch()
            if touch:
                x, y = touch
                check_button_press(x, y)
                # Wait a bit to avoid multiple detections
                time.sleep(0.5)
            
            # Sleep to prevent CPU overuse
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        gui.clear()
        print("Exiting LARK")

if __name__ == "__main__":
    main()
