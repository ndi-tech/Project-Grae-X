# GRAE-X LABS - SIMPLIFIED MONITORING DASHBOARD
# No matplotlib required - guaranteed to work!

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import requests
from datetime import datetime
import random

class SimpleDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Grae-X Labs - Social Engineering Monitor")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0c0c0c')
        
        # Attack statistics
        self.victim_count = 0
        self.keystroke_count = 0
        self.credential_count = 0
        self.active_sessions = 0
        
        # Discord webhook
        self.webhook_url = "YOUR_WEBHOOK_HERE"
        
        self.setup_gui()
        self.start_simulation()
        
    def setup_gui(self):
        # Create modern style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#0c0c0c')
        style.configure('TLabel', background='#0c0c0c', foreground='white', font=('Arial', 10))
        style.configure('Title.TLabel', background='#0c0c0c', foreground='#00ff88', font=('Arial', 16, 'bold'))
        style.configure('Metric.TLabel', background='#1a1a1a', foreground='white', font=('Arial', 24, 'bold'))
        style.configure('TButton', font=('Arial', 10))
        
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(header_frame, text="🛡️ GRAE-X LABS SECURITY MONITORING", style='Title.TLabel').pack(side='left')
        ttk.Label(header_frame, text="SOCIAL ENGINEERING ATTACK DASHBOARD", style='TLabel').pack(side='right')
        
        # Metrics Row - Visual progress bars instead of charts
        metrics_frame = ttk.Frame(self.root)
        metrics_frame.pack(fill='x', padx=20, pady=10)
        
        # Create metric cards with progress bars
        self.victims_card = self.create_metric_card(metrics_frame, "🎯 ACTIVE VICTIMS", "0", 0, "#ff6b6b")
        self.keystrokes_card = self.create_metric_card(metrics_frame, "⌨️ KEYSTROKES CAPTURED", "0", 1, "#4ecdc4")
        self.credentials_card = self.create_metric_card(metrics_frame, "🔑 CREDENTIALS FOUND", "0", 2, "#ffd166")
        self.sessions_card = self.create_metric_card(metrics_frame, "📡 ACTIVE SESSIONS", "0", 3, "#06d6a0")
        
        # Main content area
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Real-time activity
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Real-time activity monitor
        activity_label = ttk.Label(left_frame, text="🔍 REAL-TIME ACTIVITY MONITOR", style='Title.TLabel')
        activity_label.pack(anchor='w', pady=(0, 5))
        
        self.activity_text = scrolledtext.ScrolledText(
            left_frame, 
            height=20,
            bg='#1a1a1a',
            fg='#00ff88',
            insertbackground='white',
            font=('Consolas', 10)
        )
        self.activity_text.pack(fill='both', expand=True)
        
        # Right panel - Alerts and stats
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Alerts panel
        alerts_label = ttk.Label(right_frame, text="🚨 SECURITY ALERTS", style='Title.TLabel')
        alerts_label.pack(anchor='w', pady=(0, 5))
        
        self.alerts_text = scrolledtext.ScrolledText(
            right_frame,
            height=10,
            bg='#1a1a1a',
            fg='#ff4444',
            font=('Consolas', 10)
        )
        self.alerts_text.pack(fill='both', expand=True)
        
        # Statistics panel
        stats_label = ttk.Label(right_frame, text="📊 ATTACK STATISTICS", style='Title.TLabel')
        stats_label.pack(anchor='w', pady=(10, 5))
        
        self.stats_text = scrolledtext.ScrolledText(
            right_frame,
            height=8,
            bg='#1a1a1a',
            fg='#ffffff',
            font=('Consolas', 9)
        )
        self.stats_text.pack(fill='both', expand=True)
        
        # Control panel
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(control_frame, text="🔄 SIMULATE NEW VICTIM", command=self.simulate_new_victim).pack(side='left', padx=5)
        ttk.Button(control_frame, text="📊 GENERATE REPORT", command=self.generate_report).pack(side='left', padx=5)
        ttk.Button(control_frame, text="🎬 START LIVE DEMO", command=self.start_live_demo).pack(side='left', padx=5)
        ttk.Button(control_frame, text="🧹 CLEAR LOGS", command=self.clear_logs).pack(side='left', padx=5)
        ttk.Button(control_frame, text="🔴 STOP ALL", command=self.stop_simulation).pack(side='left', padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("🟢 SYSTEM READY - Monitoring for social engineering attacks...")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, style='TLabel')
        status_bar.pack(fill='x', padx=20, pady=5)
        
        self.is_running = True
        
    def create_metric_card(self, parent, title, value, column, color):
        card = tk.Frame(parent, bg='#1a1a1a', relief='raised', borderwidth=2)
        card.grid(row=0, column=column, padx=10, sticky='nsew')
        
        # Title
        title_label = tk.Label(card, text=title, bg='#1a1a1a', fg='white', font=('Arial', 10))
        title_label.pack(pady=(10, 5))
        
        # Value
        value_label = tk.Label(card, text=value, bg='#1a1a1a', fg=color, font=('Arial', 24, 'bold'))
        value_label.pack(pady=(5, 10))
        
        # Progress bar background
        progress_bg = tk.Frame(card, bg='#333333', height=8)
        progress_bg.pack(fill='x', padx=10, pady=(0, 10))
        progress_bg.pack_propagate(False)
        
        # Progress bar
        progress = tk.Frame(progress_bg, bg=color, width=0)
        progress.pack(side='left', fill='y')
        
        parent.columnconfigure(column, weight=1)
        
        # Return both value label and progress bar for updating
        return {'value': value_label, 'progress': progress}
    
    def update_progress_bars(self):
        """Update progress bars based on current metrics"""
        max_victims = 10
        max_keystrokes = 500
        max_credentials = 50
        max_sessions = 5
        
        # Update victim progress
        progress_width = min(100, (self.victim_count / max_victims) * 100)
        self.victims_card['progress'].config(width=progress_width)
        
        # Update keystroke progress  
        progress_width = min(100, (self.keystroke_count / max_keystrokes) * 100)
        self.keystrokes_card['progress'].config(width=progress_width)
        
        # Update credentials progress
        progress_width = min(100, (self.credential_count / max_credentials) * 100)
        self.credentials_card['progress'].config(width=progress_width)
        
        # Update sessions progress
        progress_width = min(100, (self.active_sessions / max_sessions) * 100)
        self.sessions_card['progress'].config(width=progress_width)
    
    def log_activity(self, message, alert=False):
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        
        if alert:
            self.alerts_text.insert('end', log_entry)
            self.alerts_text.see('end')
            # Make alerts red
            self.alerts_text.tag_add('alert', 'end-2l', 'end-1l')
            self.alerts_text.tag_config('alert', foreground='#ff4444')
        else:
            self.activity_text.insert('end', log_entry)
            self.activity_text.see('end')
            
        self.update_stats()
        self.root.update()
    
    def update_metrics(self):
        self.victims_card['value'].config(text=str(self.victim_count))
        self.keystrokes_card['value'].config(text=str(self.keystroke_count))
        self.credentials_card['value'].config(text=str(self.credential_count))
        self.sessions_card['value'].config(text=str(self.active_sessions))
        
        self.update_progress_bars()
    
    def update_stats(self):
        """Update statistics panel"""
        stats_text = f"""
📊 LIVE STATISTICS
==================
🕒 Uptime: {self.get_uptime()}
🎯 Success Rate: {self.get_success_rate()}%
⚡ Keys/Min: {self.get_keys_per_minute():.1f}
🔍 Detection Rate: {self.get_detection_rate()}%

📈 PEAK ACTIVITY
================
Max Victims: {max(3, self.victim_count)}
Max Keystrokes: {max(150, self.keystroke_count)}
Max Credentials: {max(8, self.credential_count)}

🎯 TARGET ANALYSIS
==================
Email Domains: Gmail, Yahoo, Company
Password Patterns: {random.randint(5, 15)} detected
Session Duration: {random.randint(2, 8)} min avg
"""
        
        self.stats_text.delete('1.0', 'end')
        self.stats_text.insert('1.0', stats_text)
    
    def get_uptime(self):
        if not hasattr(self, 'start_time'):
            self.start_time = datetime.now()
        uptime = datetime.now() - self.start_time
        return str(uptime).split('.')[0]  # Remove microseconds
    
    def get_success_rate(self):
        if self.victim_count == 0:
            return 0
        return min(95, (self.credential_count / self.victim_count) * 100)
    
    def get_keys_per_minute(self):
        if not hasattr(self, 'start_time'):
            return 0
        uptime_minutes = (datetime.now() - self.start_time).total_seconds() / 60
        if uptime_minutes == 0:
            return 0
        return self.keystroke_count / uptime_minutes
    
    def get_detection_rate(self):
        if self.keystroke_count == 0:
            return 0
        return min(25, (self.credential_count / self.keystroke_count) * 1000)  # per 1000 keys
    
    def send_discord_alert(self, message):
        """Send alert to Discord"""
        try:
            payload = {
                "content": f"📊 **DASHBOARD**: {message}",
                "username": "Grae-X Monitor"
            }
            requests.post(self.webhook_url, json=payload, timeout=5)
        except:
            pass
    
    def simulate_keystroke_capture(self, victim_id):
        """Simulate keystroke capture from a victim"""
        if not self.is_running:
            return
            
        self.log_activity(f"VICTIM_{victim_id}: Starting keystroke simulation...")
        
        # Different victim profiles for realism
        victim_profiles = [
            {"name": "Business User", "email": "executive@company.com", "typing": "quarterly reports financial data"},
            {"name": "Student", "email": "student@gmail.com", "typing": "homework assignment research paper"},
            {"name": "Developer", "email": "dev@tech.com", "typing": "code repository API keys database"}
        ]
        
        profile = random.choice(victim_profiles)
        
        self.log_activity(f"VICTIM_{victim_id} Profile: {profile['name']}")
        
        # Simulate typing sequence
        typing_sequence = [
            f"Hello, this is {profile['name']}",
            profile['email'],
            f"password{random.randint(1000, 9999)}",
            profile['typing'],
            "Let me check my credentials",
            "user123@yahoo.com",
            "securepass2024"
        ]
        
        for text in typing_sequence:
            if not self.is_running:
                break
                
            time.sleep(random.uniform(2, 4))
            
            # Simulate character-by-character typing
            for char in text:
                if not self.is_running:
                    break
                time.sleep(0.05)
                self.keystroke_count += 1
            
            # Random credential detection
            if random.random() < 0.4:  # 40% chance per message
                if '@' in text and '.' in text:
                    self.credential_count += 1
                    alert_msg = f"🚨 EMAIL CAPTURED from {profile['name']}: {text}"
                    self.log_activity(alert_msg, alert=True)
                    self.send_discord_alert(alert_msg)
                    
                elif 'password' in text.lower():
                    self.credential_count += 1
                    alert_msg = f"🔑 PASSWORD CAPTURED from {profile['name']}: {text}"
                    self.log_activity(alert_msg, alert=True)
                    self.send_discord_alert(alert_msg)
            
            self.update_metrics()
    
    def simulate_new_victim(self):
        """Simulate a new victim"""
        if not self.is_running:
            return
            
        self.victim_count += 1
        self.active_sessions += 1
        victim_id = self.victim_count
        
        self.log_activity(f"🎯 NEW VICTIM DETECTED: VICTIM_{victim_id}")
        self.log_activity(f"📡 Session established with VICTIM_{victim_id}")
        self.send_discord_alert(f"New victim activated: VICTIM_{victim_id}")
        
        # Start simulation in separate thread
        thread = threading.Thread(target=self.simulate_keystroke_capture, args=(victim_id,))
        thread.daemon = True
        thread.start()
        
        # Auto-end session
        def end_session():
            time.sleep(random.randint(20, 35))
            if self.is_running:
                self.active_sessions -= 1
                self.log_activity(f"📴 Session ended with VICTIM_{victim_id}")
                self.update_metrics()
        
        end_thread = threading.Thread(target=end_session)
        end_thread.daemon = True
        end_thread.start()
        
        self.update_metrics()
    
    def start_live_demo(self):
        """Start an interactive live demonstration"""
        self.log_activity("🎬 STARTING LIVE DEMONSTRATION...", alert=True)
        self.send_discord_alert("LIVE DEMO STARTED - Watch for real keystrokes!")
        
        # Create multiple victims for demo
        for i in range(3):
            if self.is_running:
                self.root.after(i * 3000, self.simulate_new_victim)
    
    def start_simulation(self):
        """Start the background simulation"""
        self.log_activity("🟢 Monitoring system initialized")
        self.log_activity("🌐 Fake Windows Update website: http://update-windows-security.com")
        self.log_activity("📧 Phishing campaign: 'Critical Security Update Required'")
        self.log_activity("⏳ Waiting for victims...")
        
        # Auto-start first victim
        self.root.after(5000, self.simulate_new_victim)
        
        # Periodic victim generation
        def periodic_simulation():
            while self.is_running:
                time.sleep(random.randint(15, 30))
                if self.is_running and random.random() > 0.5:
                    self.root.after(0, self.simulate_new_victim)
        
        sim_thread = threading.Thread(target=periodic_simulation)
        sim_thread.daemon = True
        sim_thread.start()
    
    def generate_report(self):
        """Generate attack summary report"""
        report = f"""
📊 GRAE-X LABS ATTACK SUMMARY REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
========================================
🎯 Total Victims: {self.victim_count}
⌨️ Keystrokes Captured: {self.keystroke_count}
🔑 Credentials Found: {self.credential_count}
📡 Active Sessions: {self.active_sessions}
🌐 Attack Vector: Fake Windows Update
📧 Social Engineering: Phishing Email Campaign
⚡ Success Rate: {self.get_success_rate():.1f}%
========================================
"""
        
        self.log_activity("📊 GENERATING ATTACK SUMMARY REPORT...", alert=True)
        self.log_activity(report)
        self.send_discord_alert(f"Attack Report Generated:\n{report}")
    
    def clear_logs(self):
        """Clear all logs"""
        self.activity_text.delete('1.0', 'end')
        self.alerts_text.delete('1.0', 'end')
        self.log_activity("🧹 Logs cleared - Monitoring continues...")
    
    def stop_simulation(self):
        """Stop all simulation"""
        self.is_running = False
        self.log_activity("🔴 SIMULATION STOPPED - All activities halted", alert=True)
        self.send_discord_alert("Dashboard simulation stopped")

def main():
    root = tk.Tk()
    app = SimpleDashboard(root)
    
    def on_closing():
        app.stop_simulation()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()