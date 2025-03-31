#!/usr/bin/env python3
"""
LARK v1.3 - Law Enforcement Assistance and Response Kit
Enhanced UI with badass law enforcement theme for UniHiker M10
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
STATE_ERROR = 4

# Current state and mode
current_state = STATE_READY
current_mode = 0  # 0=Miranda, 1=Statute
animation_frame = 0
wake_word_active = False

# Law enforcement blue theme
LAW_BLUE = "#003087"
COLORS = ["#003087", "#00A651", "#FFC72C", "#7030A0", "#FF0000"]
STATE_NAMES = ["READY", "LISTEN", "PROCESS", "RESPOND", "ERROR"]

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

def draw_badge():
    """Draw police badge background"""
    # Badge outline
    gui.draw_circle(x=120, y=100, r=60, color="#C0C0C0")
    gui.draw_circle(x=120, y=100, r=55, color="#000080")
    gui.draw_circle(x=120, y=100, r=50, color="#000080")
    
    # Badge star points
    for i in range(5):
        angle = i * (2 * math.pi / 5) - math.pi/2
        x1 = 120 + 45 * math.cos(angle)
        y1 = 100 + 45 * math.sin(angle)
        gui.draw_line(x0=120, y0=100, x1=int(x1), y1=int(y1), color="#FFD700", width=3)
    
    # Badge center
    gui.draw_circle(x=120, y=100, r=20, color="#000080")

def draw_status_circle():
    """Draw animated status circle based on current state"""
    global animation_frame
    
    # Base circle
    color = COLORS[current_state]
    
    # Different animations for different states
    if current_state == STATE_READY:
        # Pulsing circle
        size = 15 + int(5 * math.sin(animation_frame * 0.2))
        gui.draw_circle(x=120, y=100, r=size, color=color)
    elif current_state == STATE_LISTENING:
        # Expanding circles
        gui.draw_circle(x=120, y=100, r=20, color=color)
        size = 5 + (animation_frame % 15)
        gui.draw_circle(x=120, y=100, r=size, color="#FFFFFF")
    elif current_state == STATE_PROCESSING:
        # Spinning circle
        gui.draw_circle(x=120, y=100, r=20, color=color)
        angle = animation_frame * 0.2
        x = 120 + 15 * math.cos(angle)
        y = 100 + 15 * math.sin(angle)
        gui.draw_circle(x=int(x), y=int(y), r=5, color="#FFFFFF")
    elif current_state == STATE_RESPONDING:
        # Wave pattern
        gui.draw_circle(x=120, y=100, r=20, color=color)
        for i in range(5):
            x = 120 + (i-2) * 10
            y = 100 + int(5 * math.sin((animation_frame * 0.2) + i))
            gui.draw_circle(x=x, y=y, r=3, color="#FFFFFF")
    else:  # ERROR
        # Flashing circle
        if (animation_frame // 5) % 2 == 0:
            gui.draw_circle(x=120, y=100, r=20, color=color)
        else:
            gui.draw_circle(x=120, y=100, r=20, color="#FFFFFF")
    
    # Increment animation frame
    animation_frame = (animation_frame + 1) % 60

def draw_ui():
    """Draw the enhanced UI with law enforcement theme"""
    # Clear screen with dark background
    gui.clear()
    gui.draw_rect(x=0, y=0, w=240, h=240, color="#000020")
    
    # Draw header bar
    gui.draw_rect(x=0, y=0, w=240, h=30, color="#000080")
    
    # Draw time at top left
    time_str = time.strftime("%H:%M")
    gui.draw_text(text=time_str, x=40, y=15, color="#FFFFFF")
    
    # Draw LARK at top center
    gui.draw_text(text="L.A.R.K", x=120, y=15, color="#FFFFFF")
    
    # Draw badge background
    draw_badge()
    
    # Draw status circle with animation
    draw_status_circle()
    
    # Draw state name in center
    gui.draw_text(text=STATE_NAMES[current_state], x=120, y=100, color="#FFFFFF")
    
    # Draw mode indicator
    mode_text = "MIRANDA" if current_mode == 0 else "STATUTE"
    gui.draw_rect(x=60, y=160, w=120, h=25, color="#000080")
    gui.draw_text(text=mode_text, x=120, y=172, color="#FFFFFF")
    
    # Draw wake word indicator if active
    if wake_word_active:
        gui.draw_rect(x=60, y=190, w=120, h=20, color="#A00000")
        gui.draw_text(text="MIC ACTIVE", x=120, y=200, color="#FFFFFF")

def show_message(text):
    """Show a message in a styled box"""
    # Draw message box
    gui.draw_rect(x=40, y=130, w=160, h=25, color="#000080")
    
    # Show text (keep it short)
    short_text = text[:20] if len(text) > 20 else text
    gui.draw_text(text=short_text, x=120, y=142, color="#FFFFFF")

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
    for i in range(20):  # Animation frames
        draw_ui()
        time.sleep(0.1)
    
    # Processing state
    current_state = STATE_PROCESSING
    for i in range(20):  # Animation frames
        draw_ui()
        time.sleep(0.1)
    
    # Responding state
    current_state = STATE_RESPONDING
    draw_ui()
    
    # Show Miranda rights
    for right in MIRANDA_RIGHTS:
        show_message(right)
        speak(right)
        for i in range(20):  # Animation frames during speech
            draw_ui()
            time.sleep(0.1)
    
    # Back to ready
    current_state = STATE_READY
    draw_ui()

def run_statute_demo():
    """Run statute lookup demo"""
    global current_state
    
    # Listening state
    current_state = STATE_LISTENING
    for i in range(20):  # Animation frames
        draw_ui()
        time.sleep(0.1)
    
    # Processing state
    current_state = STATE_PROCESSING
    for i in range(20):  # Animation frames
        draw_ui()
        time.sleep(0.1)
    
    # Responding state
    current_state = STATE_RESPONDING
    draw_ui()
    
    # Show statute info
    statute = "14:98"  # DWI statute
    show_message(f"Statute {statute}")
    speak(f"Louisiana Statute {statute}")
    for i in range(20):  # Animation frames
        draw_ui()
        time.sleep(0.1)
    
    show_message(STATUTES[statute])
    speak(STATUTES[statute])
    for i in range(30):  # Animation frames
        draw_ui()
        time.sleep(0.1)
    
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
            for i in range(50):  # Animation frames during wait
                if current_state != STATE_READY or wake_word_active:
                    break
                draw_ui()
                time.sleep(0.1)
            
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
        time.sleep(0.1)

def ui_update_thread():
    """Thread to update UI animations"""
    global current_state
    
    while True:
        # Update UI with animations
        draw_ui()
        time.sleep(0.1)

def main():
    """Main function"""
    try:
        # Initial display
        draw_ui()
        show_message("LARK v1.3")
        speak("LARK version 1.3 activated")
        time.sleep(2)
        
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
