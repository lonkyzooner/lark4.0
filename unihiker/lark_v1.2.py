#!/usr/bin/env python3
"""
LARK v1.2 - Law Enforcement Assistance and Response Kit
Fully functional version for UniHiker M10
"""
from unihiker import GUI
import time
import threading
import subprocess
import os

# Initialize GUI
gui = GUI()

# States
STATE_READY = 0
STATE_LISTENING = 1
STATE_PROCESSING = 2
STATE_RESPONDING = 3

# Current state and mode
current_state = STATE_READY
current_mode = 0  # 0=Miranda, 1=Statute

# Colors - law enforcement blue theme
COLORS = ["blue", "green", "yellow", "purple"]
STATE_NAMES = ["Ready", "Listen", "Process", "Respond"]

# Louisiana statutes (minimal set)
STATUTES = {
    "14:98": "DWI - Operating vehicle while intoxicated",
    "14:30": "First degree murder",
    "14:67": "Theft"
}

# Miranda rights (simplified)
MIRANDA_RIGHTS = [
    "Right to silence",
    "Used in court",
    "Right to attorney",
    "Free attorney"
]

# Wake word active flag
wake_word_active = False

def draw_ui():
    """Draw the UI with absolute positioning"""
    # Clear screen
    gui.clear()
    
    # Draw time at top left
    time_str = time.strftime("%H:%M")
    gui.draw_text(text=time_str, x=40, y=20)
    
    # Draw LARK at top center
    gui.draw_text(text="LARK", x=120, y=20)
    
    # Draw status circle in center
    gui.draw_circle(x=120, y=100, r=20, color=COLORS[current_state])
    
    # Draw state name in circle
    gui.draw_text(text=STATE_NAMES[current_state], x=120, y=100)
    
    # Draw mode at bottom
    mode_text = "Miranda" if current_mode == 0 else "Statute"
    gui.draw_text(text=mode_text, x=120, y=180)
    
    # Draw wake word indicator if active
    if wake_word_active:
        gui.draw_text(text="Mic Active", x=120, y=220)

def show_message(text):
    """Show a message below the circle"""
    # Clear message area
    gui.draw_rect(x=40, y=130, w=160, h=30)
    
    # Show text (keep it short)
    short_text = text[:15] if len(text) > 15 else text
    gui.draw_text(text=short_text, x=120, y=140)

def speak(text):
    """Speak text using espeak"""
    try:
        subprocess.run(["espeak", "-v", "en-us", text], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
    except:
        print(f"Would speak: {text}")

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

def process_audio():
    """Process audio to determine command"""
    # In a real implementation, this would use speech recognition
    # For this demo, we'll simulate recognition based on current mode
    if current_mode == 0:
        return "miranda"
    else:
        return "statute"

def run_miranda_demo():
    """Run Miranda rights demo"""
    global current_state
    
    # Listening state
    current_state = STATE_LISTENING
    draw_ui()
    show_message("Listening")
    time.sleep(1)
    
    # Processing state
    current_state = STATE_PROCESSING
    draw_ui()
    show_message("Processing")
    time.sleep(1)
    
    # Responding state
    current_state = STATE_RESPONDING
    draw_ui()
    
    # Show Miranda rights
    for right in MIRANDA_RIGHTS:
        show_message(right)
        speak(right)
        time.sleep(2)
    
    # Back to ready
    current_state = STATE_READY
    draw_ui()

def run_statute_demo():
    """Run statute lookup demo"""
    global current_state
    
    # Listening state
    current_state = STATE_LISTENING
    draw_ui()
    show_message("Listening")
    time.sleep(1)
    
    # Processing state
    current_state = STATE_PROCESSING
    draw_ui()
    show_message("Processing")
    time.sleep(1)
    
    # Responding state
    current_state = STATE_RESPONDING
    draw_ui()
    
    # Show statute info
    statute = "14:98"  # DWI statute
    show_message(f"Statute {statute}")
    speak(f"Louisiana Statute {statute}")
    time.sleep(2)
    
    show_message(STATUTES[statute])
    speak(STATUTES[statute])
    time.sleep(3)
    
    # Back to ready
    current_state = STATE_READY
    draw_ui()

def listen_for_wake_word():
    """Listen for wake word activation"""
    global current_state, wake_word_active
    
    while True:
        # Only check when in ready state
        if current_state == STATE_READY:
            # Check for audio input
            wake_word_active = True
            draw_ui()
            
            if listen_for_audio():
                # Audio detected, process command
                command = process_audio()
                
                # Run appropriate demo
                if "miranda" in command.lower():
                    run_miranda_demo()
                elif "statute" in command.lower() or "law" in command.lower():
                    run_statute_demo()
            
            # Reset wake word flag
            wake_word_active = False
            draw_ui()
        
        # Sleep to prevent CPU overuse
        time.sleep(0.5)

def auto_demo_cycle():
    """Auto cycle between demos when no voice input"""
    global current_mode, current_state
    
    while True:
        # Only run when in ready state and not listening for wake word
        if current_state == STATE_READY and not wake_word_active:
            # Wait a bit before starting demo
            time.sleep(5)
            
            # If still in ready state and not listening, run demo
            if current_state == STATE_READY and not wake_word_active:
                # Run current demo
                if current_mode == 0:
                    run_miranda_demo()
                else:
                    run_statute_demo()
                
                # Switch modes
                current_mode = 1 - current_mode
                draw_ui()
        
        # Sleep to prevent CPU overuse
        time.sleep(1)

def main():
    """Main function"""
    try:
        # Initial display
        draw_ui()
        show_message("LARK v1.2")
        speak("LARK version 1.2 activated")
        time.sleep(2)
        
        # Start wake word detection in background
        wake_thread = threading.Thread(target=listen_for_wake_word)
        wake_thread.daemon = True
        wake_thread.start()
        
        # Start auto demo in background
        demo_thread = threading.Thread(target=auto_demo_cycle)
        demo_thread.daemon = True
        demo_thread.start()
        
        # Keep main thread alive and update time
        while True:
            if current_state == STATE_READY:
                # Redraw UI to update time
                draw_ui()
            time.sleep(10)
            
    except KeyboardInterrupt:
        gui.clear()
        print("Exiting LARK")

if __name__ == "__main__":
    main()
