"""
deploy_bridge.py
----------------
Deploys the Telegram Bridge and logic files to the server.
Restarts the portfolio app and starts the Telegram Bot.
"""

import paramiko
import os

HOST = "192.168.1.150"
USER = "nishan"
PASSWORD = "6WKW5_3w2w5121"

LOCAL_DIR = r"c:\Users\NISHAN\Desktop\Test Folder\My Portfolio\portfolio"
REMOTE_DIR = "/home/nishan/portfolio"

FILES = [
    "app.py",
    "telegram_bridge.py",
    "book_generator.py",
    "image_processor.py"
]

def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD)
    print(f"[+] Connected to {HOST}")

    scp = client.open_sftp()
    
    # Upload scripts
    for f in FILES:
        local_path = os.path.join(LOCAL_DIR, f)
        remote_path = os.path.join(REMOTE_DIR, f)
        print(f"[*] Uploading {f}...")
        scp.put(local_path, remote_path)
    
    scp.close()

    # Restart Portfolio App
    print("[*] Reloading Portfolio App...")
    client.exec_command("pkill -f 'python app.py'")
    client.exec_command(f"cd {REMOTE_DIR} && source venv/bin/activate && nohup python app.py > /tmp/portfolio.log 2>&1 &")

    # Start Telegram Bridge
    print("[*] Starting Telegram Bridge...")
    client.exec_command("pkill -f 'python telegram_bridge.py'")
    client.exec_command(f"cd {REMOTE_DIR} && source venv/bin/activate && nohup python telegram_bridge.py > /tmp/bridge.log 2>&1 &")

    print("[+] Deployment Complete. Please check your Telegram Bot @NishanServerBot and press /start")
    client.close()

if __name__ == "__main__":
    main()
