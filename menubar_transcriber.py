#!/usr/bin/env python3
"""
Menu bar speech-to-text transcriber that works system-wide
"""

import logging
import os
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime

import numpy as np
import pyperclip
import rumps
import scipy.io.wavfile as wavfile
import sounddevice as sd
import whisper
from pynput import keyboard
from pynput.keyboard import Key


def setup_logging():
    """Setup logging to write to user's home directory"""
    log_dir = os.path.expanduser("~/Library/Logs/Transcrybe")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"transcrybe_{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.info(f"Logging initialized - log file: {log_file}")
    return log_file

class TranscribeApp(rumps.App):
    def __init__(self):
        super(TranscribeApp, self).__init__("🎙️", quit_button=None)
        
        # Setup logging first
        self.log_file = setup_logging()
        logging.info("TranscribeApp initializing...")
        
        self.model = None
        self.is_recording = False
        self.audio_data = []
        self.temp_file = None
        self.hotkeys = None
        
        # Audio settings
        self.CHANNELS = 1
        self.RATE = 16000
        
        # Menu items
        self.menu = [
            "Start Recording",
            None,  # Separator
            "Request Permissions",
            "Settings",
            "Show Log File",
            None,
            "Quit"
        ]
        
        # Request permissions on startup
        threading.Thread(target=self._request_permissions, daemon=True).start()
        
        # Load Whisper model in background
        threading.Thread(target=self._load_model, daemon=True).start()
        
        # Setup global hotkey
        self._setup_hotkey()
    
    def _load_model(self):
        """Load Whisper model in background"""
        try:
            logging.info("Loading Whisper model...")
            rumps.notification("Transcrybe", "Loading speech model...", "")
            self.model = whisper.load_model("base")
            self.title = "🎙️"  # Ready indicator
            logging.info("Whisper model loaded successfully")
            rumps.notification("Transcrybe", "Ready!", "Press Cmd+Shift+Space to record")
        except Exception as e:
            logging.error(f"Failed to load Whisper model: {e}")
            rumps.notification("Transcrybe", "Error", f"Failed to load model: {e}")
    
    def _request_permissions(self):
        """Request necessary permissions by triggering system dialogs"""
        logging.info("Requesting system permissions...")
        stream = None
        test_hotkeys = None
        try:
            # Request microphone permission by trying to access it
            logging.info("Testing microphone access...")
            stream = sd.InputStream(samplerate=16000, channels=1, dtype=np.float32)
            stream.start()
            stream.read(1)
            logging.info("Microphone access successful")
            
            # Request accessibility permission by trying to use keyboard controller
            logging.info("Testing accessibility access...")
            kb = keyboard.Controller()
            logging.info("Accessibility access successful")
            
            # Request input monitoring by trying to listen for keys
            try:
                logging.info("Testing input monitoring access...")
                test_hotkeys = keyboard.GlobalHotKeys({'<f24>': lambda: None})
                test_hotkeys.start()
                logging.info("Input monitoring access successful")
            except Exception as e:
                logging.warning(f"Input monitoring test failed: {e}")
                
        except Exception as e:
            logging.error(f"Permission request failed: {e}")
        finally:
            if stream:
                try:
                    stream.stop()
                    stream.close()
                except:
                    pass
            if test_hotkeys:
                try:
                    test_hotkeys.stop()
                except:
                    pass
    
    def _setup_hotkey(self):
        """Setup global hotkey listener"""
        try:
            logging.info("Setting up global hotkey: Cmd+Shift+Space")
            self.hotkeys = keyboard.GlobalHotKeys({
                '<cmd>+<shift>+<space>': self._toggle_recording
            })
            self.hotkeys.start()
            logging.info("Global hotkey setup successful")
        except Exception as e:
            logging.error(f"Hotkey setup failed: {e}")
            rumps.notification("Transcrybe", "Error", f"Hotkey setup failed: {e}")
    
    def _toggle_recording(self):
        """Toggle recording on/off"""
        logging.info("Hotkey triggered: toggle recording")
        if not self.model:
            logging.warning("Recording toggle failed: model not loaded yet")
            rumps.notification("Transcrybe", "Not Ready", "Model still loading...")
            return
            
        if self.is_recording:
            logging.info("Stopping recording...")
            self._stop_recording()
        else:
            logging.info("Starting recording...")
            self._start_recording()
    
    def _start_recording(self):
        """Start recording"""
        if self.is_recording:
            return
            
        self.is_recording = True
        self.audio_data = []
        self.title = "🔴"  # Recording indicator
        
        rumps.notification("Transcrybe", "Recording", "Speak now...")
        
        # Record in background thread
        threading.Thread(target=self._record_audio, daemon=True).start()
    
    def _stop_recording(self):
        """Stop recording and transcribe"""
        if not self.is_recording:
            return
            
        self.is_recording = False
        self.title = "⏳"  # Processing indicator
        
        # Process in background thread
        threading.Thread(target=self._process_recording, daemon=True).start()
    
    def _record_audio(self):
        """Record audio data"""
        stream = None
        try:
            stream = sd.InputStream(samplerate=self.RATE, channels=self.CHANNELS, dtype=np.float32)
            stream.start()
            
            while self.is_recording:
                try:
                    audio_chunk, _ = stream.read(1024)
                    self.audio_data.append(audio_chunk)
                    time.sleep(0.01)
                except sd.PortAudioError:
                    break
        except Exception as e:
            rumps.notification("Transcrybe", "Error", f"Recording failed: {e}")
        finally:
            if stream:
                try:
                    stream.stop()
                    stream.close()
                except:
                    pass
    
    def _process_recording(self):
        """Process recorded audio and transcribe"""
        try:
            if not self.audio_data:
                self.title = "🎙️"
                rumps.notification("Transcrybe", "Error", "No audio recorded")
                return
            
            # Save audio file
            self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            audio_array = np.concatenate(self.audio_data, axis=0)
            audio_int16 = (audio_array * 32767).astype(np.int16)
            wavfile.write(self.temp_file.name, self.RATE, audio_int16)
            
            # Transcribe
            result = self.model.transcribe(self.temp_file.name, fp16=False)
            text = result["text"].strip()
            
            if text:
                # Copy to clipboard
                pyperclip.copy(text)
                
                # Try multiple pasting methods
                pasted = False
                
                # Method 1: pynput
                try:
                    logging.info(f"Attempting pynput paste for: {text[:50]}...")
                    kb = keyboard.Controller()
                    time.sleep(0.1)
                    with kb.pressed(Key.cmd):
                        kb.press('v')
                        kb.release('v')
                    time.sleep(0.1)  # Give it time to paste
                    pasted = True
                    logging.info("pynput paste succeeded")
                    rumps.notification("Transcrybe", "Success!", f"Pasted: {text}")
                except Exception as e:
                    logging.warning(f"pynput paste failed: {e}")
                
                # Method 2: Try with longer delay
                if not pasted:
                    try:
                        logging.info("Attempting second paste method...")
                        time.sleep(0.5)
                        kb = keyboard.Controller()
                        kb.tap(Key.cmd, modifier=Key.cmd)  # Different approach
                        kb.tap('v')
                        pasted = True
                        logging.info("Second paste method succeeded")
                        rumps.notification("Transcrybe", "Success!", f"Pasted: {text}")
                    except Exception as e:
                        logging.warning(f"Second paste method failed: {e}")
                
                # Method 3: Direct keystroke
                if not pasted:
                    try:
                        logging.info("Attempting Quartz paste method...")
                        import Quartz

                        # Create key down event for Cmd+V
                        cmd_down = Quartz.CGEventCreateKeyboardEvent(None, 55, True)  # Cmd key
                        v_down = Quartz.CGEventCreateKeyboardEvent(None, 9, True)   # V key
                        v_up = Quartz.CGEventCreateKeyboardEvent(None, 9, False)
                        cmd_up = Quartz.CGEventCreateKeyboardEvent(None, 55, False)
                        
                        # Set Cmd modifier on V key events
                        Quartz.CGEventSetFlags(v_down, Quartz.kCGEventFlagMaskCommand)
                        Quartz.CGEventSetFlags(v_up, Quartz.kCGEventFlagMaskCommand)
                        
                        # Post events
                        Quartz.CGEventPost(Quartz.kCGHIDEventTap, cmd_down)
                        Quartz.CGEventPost(Quartz.kCGHIDEventTap, v_down)
                        Quartz.CGEventPost(Quartz.kCGHIDEventTap, v_up)
                        Quartz.CGEventPost(Quartz.kCGHIDEventTap, cmd_up)
                        
                        pasted = True
                        logging.info("Quartz paste succeeded")
                        rumps.notification("Transcrybe", "Success!", f"Pasted: {text}")
                    except Exception as e:
                        logging.warning(f"Quartz paste failed: {e}")
                
                if not pasted:
                    logging.warning("All paste methods failed - text copied to clipboard")
                    rumps.notification("Transcrybe", "Copied to Clipboard", f"Press Cmd+V to paste: {text}")
            else:
                rumps.notification("Transcrybe", "No Speech", "No speech detected")
            
            self.title = "🎙️"  # Ready
            
        except Exception as e:
            self.title = "🎙️"
            rumps.notification("Transcrybe", "Error", f"Processing failed: {e}")
        finally:
            # Cleanup
            if self.temp_file and os.path.exists(self.temp_file.name):
                os.unlink(self.temp_file.name)
    
    @rumps.clicked("Start Recording")
    def start_recording_menu(self, _):
        """Menu item to start recording"""
        self._toggle_recording()
    
    @rumps.clicked("Request Permissions")
    def request_permissions_menu(self, _):
        """Manually request permissions"""
        self._request_permissions()
        rumps.alert("Permissions", "Permission dialogs should appear.\n\nIf not, manually grant:\n1. Microphone access\n2. Accessibility access\n3. Input Monitoring access\n\nIn System Settings → Privacy & Security")
    
    @rumps.clicked("Settings")
    def settings(self, _):
        """Show settings info"""
        rumps.alert("Settings", "Global Hotkey: Cmd+Shift+Space\n\nIf auto-paste isn't working:\n1. Click 'Request Permissions' above\n2. Grant all requested permissions\n3. Restart the app")
    
    @rumps.clicked("Show Log File")
    def show_log_file(self, _):
        """Open log file location"""
        log_dir = os.path.expanduser("~/Library/Logs/Transcrybe")
        subprocess.run(["open", log_dir])
    
    @rumps.clicked("Quit")
    def quit_app(self, _):
        """Quit application"""
        # Stop recording if active
        self.is_recording = False
        
        # Stop hotkey listener
        if self.hotkeys:
            try:
                self.hotkeys.stop()
            except:
                pass
        
        # Cleanup temp file
        if self.temp_file and os.path.exists(self.temp_file.name):
            try:
                os.unlink(self.temp_file.name)
            except:
                pass
                
        rumps.quit_application()

if __name__ == "__main__":
    app = TranscribeApp()
    app.run()