#!/usr/bin/env python3
"""
LARK Speech Module v1.2
Handles speech recognition and synthesis for LARK
"""
import subprocess
import os
import time

class LarkSpeech:
    """Speech handling for LARK"""
    
    def __init__(self):
        """Initialize speech module"""
        self.audio_file = "/tmp/lark_audio.wav"
        self.audio_duration = 5  # seconds
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
    
    def listen(self, duration=None):
        """Record audio from microphone"""
        if duration is None:
            duration = self.audio_duration
            
        try:
            # Remove old audio file if exists
            if os.path.exists(self.audio_file):
                os.remove(self.audio_file)
                
            # Record audio using arecord
            subprocess.run(
                ["arecord", "-d", str(duration), "-f", "cd", "-q", self.audio_file],
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            
            # Check if file exists and has content
            if os.path.exists(self.audio_file) and os.path.getsize(self.audio_file) > 5000:
                return True
            return False
        except Exception as e:
            print(f"Error recording audio: {e}")
            return False
    
    def recognize(self):
        """
        Recognize speech from recorded audio
        
        In a production system, this would use a speech recognition API.
        For this demo, we'll return predefined commands based on audio presence.
        """
        if not os.path.exists(self.audio_file):
            return ""
            
        # Check if file has content (simple audio detection)
        if os.path.getsize(self.audio_file) > 20000:
            return "miranda"
        elif os.path.getsize(self.audio_file) > 10000:
            return "statute"
        else:
            return ""
    
    def speak(self, text):
        """Speak text using espeak"""
        if not text:
            return False
            
        try:
            if self.has_espeak:
                # Use espeak for TTS
                subprocess.run(
                    ["espeak", "-v", "en-us", text],
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE
                )
                return True
            else:
                # Just print if espeak not available
                print(f"Would speak: {text}")
                return False
        except Exception as e:
            print(f"Error speaking text: {e}")
            return False
    
    def detect_wake_word(self, wake_word="lark"):
        """
        Detect wake word in audio
        
        In a production system, this would use a wake word detection system.
        For this demo, we'll simulate detection based on audio presence.
        """
        if self.listen(duration=2):
            # Simple simulation - if audio is detected, assume wake word was spoken
            return True
        return False
    
    def cleanup(self):
        """Clean up temporary files"""
        if os.path.exists(self.audio_file):
            try:
                os.remove(self.audio_file)
            except:
                pass
