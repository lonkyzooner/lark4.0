#!/usr/bin/env python3
"""
LARK v1.2 - Law Enforcement Assistance and Response Kit
Fully integrated version for UniHiker M10
"""
from unihiker import GUI
import time
import threading
import subprocess
import os

# States
STATE_READY = 0
STATE_LISTENING = 1
STATE_PROCESSING = 2
STATE_RESPONDING = 3

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

class LarkApp:
    """LARK Application for UniHiker"""
    
    def __init__(self):
        """Initialize LARK application"""
        # Initialize GUI
        self.gui = GUI()
        
        # Current state and mode
        self.current_state = STATE_READY
        self.current_mode = 0  # 0=Miranda, 1=Statute
        
        # Wake word active flag
        self.wake_word_active = False
        
        # Audio file path
        self.audio_file = "/tmp/lark_audio.wav"
        
        # Check for espeak
        self.has_espeak = self._check_espeak()
    
    def _check_espeak(self):
        """Check if espeak is installed"""
        try:
            result = subprocess.run(["which", "espeak"], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
            return result.returncode == 0
        except:
            return False
    
    def draw_ui(self):
        """Draw the UI with absolute positioning"""
        # Clear screen
        self.gui.clear()
        
        # Draw time at top left
        time_str = time.strftime("%H:%M")
        self.gui.draw_text(text=time_str, x=40, y=20)
        
        # Draw LARK at top center
        self.gui.draw_text(text="LARK", x=120, y=20)
        
        # Draw status circle in center
        self.gui.draw_circle(x=120, y=100, r=20, color=COLORS[self.current_state])
        
        # Draw state name in circle
        self.gui.draw_text(text=STATE_NAMES[self.current_state], x=120, y=100)
        
        # Draw mode at bottom
        mode_text = "Miranda" if self.current_mode == 0 else "Statute"
        self.gui.draw_text(text=mode_text, x=120, y=180)
        
        # Draw wake word indicator if active
        if self.wake_word_active:
            self.gui.draw_text(text="Mic Active", x=120, y=220)
    
    def show_message(self, text):
        """Show a message below the circle"""
        # Clear message area
        self.gui.draw_rect(x=40, y=130, w=160, h=30)
        
        # Show text (keep it short)
        short_text = text[:15] if len(text) > 15 else text
        self.gui.draw_text(text=short_text, x=120, y=140)
    
    def speak(self, text):
        """Speak text using espeak"""
        try:
            if self.has_espeak:
                subprocess.run(["espeak", "-v", "en-us", text], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
            else:
                print(f"Would speak: {text}")
        except:
            print(f"Would speak: {text}")
    
    def listen_for_audio(self):
        """Record audio and check if it contains speech"""
        try:
            # Record 3 seconds of audio
            subprocess.run(["arecord", "-d", "3", "-f", "cd", "-q", self.audio_file], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
            
            # Check if file exists and has content
            if os.path.exists(self.audio_file) and os.path.getsize(self.audio_file) > 10000:
                return True
            else:
                return False
        except:
            return False
    
    def process_audio(self):
        """Process audio to determine command"""
        # In a real implementation, this would use speech recognition
        # For this demo, we'll simulate recognition based on current mode
        if self.current_mode == 0:
            return "miranda"
        else:
            return "statute"
    
    def run_miranda_demo(self):
        """Run Miranda rights demo"""
        # Listening state
        self.current_state = STATE_LISTENING
        self.draw_ui()
        self.show_message("Listening")
        time.sleep(1)
        
        # Processing state
        self.current_state = STATE_PROCESSING
        self.draw_ui()
        self.show_message("Processing")
        time.sleep(1)
        
        # Responding state
        self.current_state = STATE_RESPONDING
        self.draw_ui()
        
        # Show Miranda rights
        for right in MIRANDA_RIGHTS:
            self.show_message(right)
            self.speak(right)
            time.sleep(2)
        
        # Back to ready
        self.current_state = STATE_READY
        self.draw_ui()
    
    def run_statute_demo(self):
        """Run statute lookup demo"""
        # Listening state
        self.current_state = STATE_LISTENING
        self.draw_ui()
        self.show_message("Listening")
        time.sleep(1)
        
        # Processing state
        self.current_state = STATE_PROCESSING
        self.draw_ui()
        self.show_message("Processing")
        time.sleep(1)
        
        # Responding state
        self.current_state = STATE_RESPONDING
        self.draw_ui()
        
        # Show statute info
        statute = "14:98"  # DWI statute
        self.show_message(f"Statute {statute}")
        self.speak(f"Louisiana Statute {statute}")
        time.sleep(2)
        
        self.show_message(STATUTES[statute])
        self.speak(STATUTES[statute])
        time.sleep(3)
        
        # Back to ready
        self.current_state = STATE_READY
        self.draw_ui()
    
    def listen_for_wake_word(self):
        """Listen for wake word activation"""
        while True:
            # Only check when in ready state
            if self.current_state == STATE_READY:
                # Check for audio input
                self.wake_word_active = True
                self.draw_ui()
                
                if self.listen_for_audio():
                    # Audio detected, process command
                    command = self.process_audio()
                    
                    # Run appropriate demo
                    if "miranda" in command.lower():
                        self.run_miranda_demo()
                    elif "statute" in command.lower() or "law" in command.lower():
                        self.run_statute_demo()
                
                # Reset wake word flag
                self.wake_word_active = False
                self.draw_ui()
            
            # Sleep to prevent CPU overuse
            time.sleep(0.5)
    
    def auto_demo_cycle(self):
        """Auto cycle between demos when no voice input"""
        while True:
            # Only run when in ready state and not listening for wake word
            if self.current_state == STATE_READY and not self.wake_word_active:
                # Wait a bit before starting demo
                time.sleep(5)
                
                # If still in ready state and not listening, run demo
                if self.current_state == STATE_READY and not self.wake_word_active:
                    # Run current demo
                    if self.current_mode == 0:
                        self.run_miranda_demo()
                    else:
                        self.run_statute_demo()
                    
                    # Switch modes
                    self.current_mode = 1 - self.current_mode
                    self.draw_ui()
            
            # Sleep to prevent CPU overuse
            time.sleep(1)
    
    def run(self):
        """Run the LARK application"""
        try:
            # Initial display
            self.draw_ui()
            self.show_message("LARK v1.2")
            self.speak("LARK version 1.2 activated")
            time.sleep(2)
            
            # Start wake word detection in background
            wake_thread = threading.Thread(target=self.listen_for_wake_word)
            wake_thread.daemon = True
            wake_thread.start()
            
            # Start auto demo in background
            demo_thread = threading.Thread(target=self.auto_demo_cycle)
            demo_thread.daemon = True
            demo_thread.start()
            
            # Keep main thread alive and update time
            while True:
                if self.current_state == STATE_READY:
                    # Redraw UI to update time
                    self.draw_ui()
                time.sleep(10)
                
        except KeyboardInterrupt:
            self.gui.clear()
            print("Exiting LARK")

def main():
    """Main function"""
    app = LarkApp()
    app.run()

if __name__ == "__main__":
    main()
