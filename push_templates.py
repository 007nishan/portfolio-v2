"""
push_templates.py - Push updated HTML templates to the live server
"""
import paramiko
import paramiko.sftp_client
import os

HOST = "192.168.1.150"
USER = "nishan"
PASSWORD = "6WKW5_3w2w5121"

LOCAL_TEMPLATES = r"c:\Users\NISHAN\Desktop\Test Folder\My Portfolio\portfolio\templates"
REMOTE_TEMPLATES = "/home/nishan/portfolio/templates"

FILES = ["home.html", "challenge_detail.html", "base.html"]

def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=10)
    print(f"[+] Connected to {HOST}")

    sftp = client.open_sftp()
    for fname in FILES:
        local = os.path.join(LOCAL_TEMPLATES, fname)
        remote = f"{REMOTE_TEMPLATES}/{fname}"
        sftp.put(local, remote)
        print(f"[+] Uploaded {fname}")
    sftp.close()

    # Restart flask to pick up template changes (Jinja2 caches templates)
    stdin, stdout, stderr = client.exec_command(
        "sudo systemctl restart portfolio 2>/dev/null || pkill -HUP -f 'python app.py' 2>/dev/null || true"
    )
    stdout.read()
    print("[+] Server reloaded — templates live!")
    client.close()

if __name__ == "__main__":
    main()
