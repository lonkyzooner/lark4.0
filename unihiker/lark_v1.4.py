#!/usr/bin/env python3
"""
LARK v1.4 - Law Enforcement Assistance and Response Kit
Web-style UI optimized for UniHiker M10
"""
from unihiker import GUI
import time
import threading
import subprocess
import os
import math

# Initialize GUI
gui = GUI()

# States
STATE_READY = 0
STATE_LISTENING = 1
STATE_PROCESSING = 2
STATE_RESPONDING = 3

# Current state and mode
current_state = STATE_READY
animation_frame = 0
mic_active = False

# Colors
DARK_BLUE = "#001a3a"
HEADER_BLUE = "#000c1a"
CIRCLE_BLUE = "#0055aa"
GREEN = "#00A651"
YELLOW = "#FFC72C"
PURPLE = "#7030A0"
RED = "#FF0000"
WHITE = "#FFFFFF"

# State colors
STATE_COLORS = [CIRCLE_BLUE, GREEN, YELLOW, PURPLE]

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

def draw_battery(x, y, level=85):
    """Draw battery indicator"""
    # Battery outline
    gui.draw_rect(x=x-15, y=y-6, w=25, h=12, color=WHITE)
    
    # Battery tip
    gui.draw_rect(x=x+10, y=y-3, w=3, h=6, color=WHITE)
    
    # Battery level
    level_width = int(23 * level / 100)
    gui.draw_rect(x=x-14, y=y-5, w=level_width, h=10, color=GREEN)
    
    # Battery percentage
    gui.draw_text(text=f"{level}%", x=x+20, y=y, color=WHITE)

def draw_mic_indicator(x, y, active=False):
    """Draw microphone indicator"""
    color = GREEN if active else RED
    gui.draw_circle(x=x, y=y, r=6, color=color)
    gui.draw_text(text="Mic", x=x+15, y=y, color=WHITE)

def draw_ui():
    """Draw the web-style UI"""
    global animation_frame
    
    # Clear screen with dark background
    gui.clear()
    gui.draw_rect(x=0, y=0, w=240, h=240, color=DARK_BLUE)
    
    # Draw border
    gui.draw_rect(x=0, y=0, w=240, h=240, color=CIRCLE_BLUE, fill=False)
    
    # Draw header bar
    gui.draw_rect(x=0, y=0, w=240, h=30, color=HEADER_BLUE)
    
    # Draw LARK title
    gui.draw_text(text="LARK v1.0", x=50, y=15, color=WHITE)
    
    # Draw mic indicator
    draw_mic_indicator(x=160, y=15, active=mic_active)
    
    # Draw battery
    draw_battery(x=200, y=15, level=85)
    
    # Draw main circle
    circle_color = STATE_COLORS[current_state]
    
    # Pulse animation for ready state
    if current_state == STATE_READY:
        pulse_size = 3 * math.sin(animation_frame * 0.1)
        gui.draw_circle(x=120, y=120, r=80 + int(pulse_size), color=circle_color, fill=False)
    
    gui.draw_circle(x=120, y=120, r=80, color=circle_color, fill=False)
    
    # Draw LARK text in center
    gui.draw_text(text="LARK", x=120, y=120, color=WHITE, size=36)
    
    # Draw status text
    status_texts = [
        "Ready. Say \"Hey LARK\" to activate.",
        "Listening...",
        "Processing...",
        "Responding..."
    ]
    gui.draw_text(text=status_texts[current_state], x=120, y=210, color=WHITE)
    
    # Draw message box
    gui.draw_rect(x=20, y=230, w=200, h=40, color=HEADER_BLUE)
    
    # Show welcome message or current response
    if current_state == STATE_READY:
        message = "Welcome to LARK. Say \"Hey LARK\" to activate."
    elif current_state == STATE_LISTENING:
        message = "I'm listening. What can I help you with?"
    elif current_state == STATE_PROCESSING:
        message = "Processing your request..."
    else:
        # In responding state, show Miranda rights based on animation frame
        index = (animation_frame // 30) % len(MIRANDA_RIGHTS)
        message = MIRANDA_RIGHTS[index]
    
    # Truncate message if too long
    if len(message) > 30:
        message = message[:27] + "..."
    
    gui.draw_text(text=message, x=120, y=250, color=WHITE)
    
    # Increment animation frame
    animation_frame = (animation_frame + 1) % 120

def listen_for_audio():
    """Record audio and check if it contains speech"""
    audio_file = "/tmp/lark_audio.wav"
    
    try:
        # Record 3 seconds of audio
        subprocess.run(["arecord", "-d", "3", "-f", "cd", "-q", audio_file], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
        
        # Check if file exists and has content
        if os.path.exists(audio_file) and os.path.getsize(audio_file) > 10000:
            return True
        else:
            return False
    except:
        return False

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
    for i in range(20):
        draw_ui()
        time.sleep(0.1)
    
    # Processing state
    current_state = STATE_PROCESSING
    for i in range(20):
        draw_ui()
        time.sleep(0.1)
    
    # Responding state
    current_state = STATE_RESPONDING
    for right in MIRANDA_RIGHTS:
        speak(right)
        for i in range(30):
            draw_ui()
            time.sleep(0.1)
    
    # Back to ready state
    current_state = STATE_READY
    mic_active = False
    draw_ui()

def run_statute_demo():
    """Run statute lookup demo"""
    global current_state, mic_active
    
    # Listening state
    current_state = STATE_LISTENING
    mic_active = True
    for i in range(20):
        draw_ui()
        time.sleep(0.1)
    
    # Processing state
    current_state = STATE_PROCESSING
    for i in range(20):
        draw_ui()
        time.sleep(0.1)
    
    # Responding state
    current_state = STATE_RESPONDING
    statute = "14:98"  # DWI statute
    speak(f"Louisiana Statute {statute}")
    for i in range(30):
        draw_ui()
        time.sleep(0.1)
    
    speak(STATUTES[statute])
    for i in range(30):
        draw_ui()
        time.sleep(0.1)
    
    # Back to ready state
    current_state = STATE_READY
    mic_active = False
    draw_ui()

def listen_for_wake_word():
    """Listen for wake word activation"""
    global current_state, mic_active
    
    while True:
        # Only check when in ready state
        if current_state == STATE_READY:
            # Simulate wake word detection
            if listen_for_audio():
                # Process command (simplified for demo)
                command = "miranda"  # Default to Miranda demo
                
                # Run appropriate demo
                if "miranda" in command.lower():
                    run_miranda_demo()
                elif "statute" in command.lower():
                    run_statute_demo()
        
        # Sleep to prevent CPU overuse
        time.sleep(0.5)

def ui_update_thread():
    """Thread to update UI animations"""
    while True:
        # Update UI with animations
        draw_ui()
        time.sleep(0.1)

def auto_demo_cycle():
    """Auto cycle between demos when no voice input"""
    global current_state
    
    while True:
        # Only run when in ready state
        if current_state == STATE_READY:
            # Wait a bit before starting demo
            time.sleep(15)
            
            # If still in ready state, run demo
            if current_state == STATE_READY:
                # Alternate between demos
                if (int(time.time()) // 30) % 2 == 0:
                    run_miranda_demo()
                else:
                    run_statute_demo()
        
        # Sleep to prevent CPU overuse
        time.sleep(1)

def main():
    """Main function"""
    try:
        # Initial display
        draw_ui()
        speak("LARK version 1.4 activated")
        
        # Start UI update thread
        ui_thread = threading.Thread(target=ui_update_thread)
        ui_thread.daemon = True
        ui_thread.start()
        
        # Start wake word detection in background
        wake_thread = threading.Thread(target=listen_for_wake_word)
        wake_thread.daemon = True
        wake_thread.start()
        
        # Start auto demo in background
        demo_thread = threading.Thread(target=auto_demo_cycle)
        demo_thread.daemon = True
        demo_thread.start()
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        gui.clear()
        print("Exiting LARK")

if __name__ == "__main__":
    main()
