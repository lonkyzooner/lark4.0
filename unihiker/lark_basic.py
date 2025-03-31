#!/usr/bin/env python3
"""
LARK Basic - Ultra basic version for UniHiker
No touch detection, just a static display
"""
from unihiker import GUI
import time
import subprocess

# Initialize GUI
gui = GUI()

# Colors - using standard color names that UniHiker supports
DARK_BLUE = "navy"
HEADER_BLUE = "darkblue"
CIRCLE_BLUE = "blue"
GREEN = "green"
WHITE = "white"

def draw_ui():
    """Draw a very basic UI"""
    # Clear screen with dark background
    gui.clear()
    gui.draw_rect(x=0, y=0, w=240, h=240, color=DARK_BLUE)
    
    # Draw header
    gui.draw_rect(x=0, y=0, w=240, h=30, color=HEADER_BLUE)
    gui.draw_text(text="LARK", x=50, y=15, color=WHITE)
    
    # Draw main circle - simple blue circle
    gui.draw_circle(x=120, y=100, r=20, color=CIRCLE_BLUE)
    
    # Draw status text
    gui.draw_text(text="Ready", x=120, y=140, color=WHITE)
    
    # Draw message
    gui.draw_text(text="LARK Basic", x=120, y=180, color=WHITE)

def speak(text):
    """Speak text using espeak"""
    try:
        subprocess.run(["espeak", "-v", "en-us", text], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
    except:
        print(f"Would speak: {text}")

def main():
    """Main function - just display static UI"""
    try:
        # Draw initial UI
        draw_ui()
        
        # Announce startup
        speak("LARK basic version activated")
        
        # Keep the program running
        print("Press Ctrl+C to exit")
        while True:
            time.sleep(5)
            
    except KeyboardInterrupt:
        gui.clear()
        print("Exiting LARK")

if __name__ == "__main__":
    main()
