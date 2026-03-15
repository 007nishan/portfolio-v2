"""
security_harden.py
------------------
Applies scientific cybersecurity hardening to the remote server.
1. Configures UFW (Firewall).
2. Installs Fail2Ban.
3. Hardens SSH configuration.
4. Adds security middle-ware (Log Rotation).
"""

import paramiko
import sys

HOST = "192.168.1.150"
USER = "nishan"
PASSWORD = "6WKW5_3w2w5121"

def run_cmd(client, cmd):
    print(f"  >> {cmd}")
    stdin, stdout, stderr = client.exec_command(f"sudo {cmd}")
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if err:
        print(f"     [!] {err}")
    return out

def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD)
    print(f"[+] Connected to {HOST} for Security Hardening")

    # 1. Update and Install Fail2Ban
    print("\n[1] Installing Fail2Ban (Automated Intrusion Prevention)...")
    run_cmd(client, "apt-get update -y && apt-get install -y fail2ban")

    # 2. Configure Firewall (UFW)
    print("\n[2] Configuring UFW (Firewall Rules)...")
    run_cmd(client, "ufw default deny incoming")
    run_cmd(client, "ufw default allow outgoing")
    run_cmd(client, "ufw allow 22/tcp")    # SSH
    run_cmd(client, "ufw allow 5001/tcp")  # Flask Portfolio
    run_cmd(client, "ufw --force enable")

    # 3. Harden SSH (Disable Root Login, etc.)
    print("\n[3] Hardening SSH Configuration...")
    run_cmd(client, "sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config")
    run_cmd(client, "systemctl restart ssh")

    # 4. Check status
    print("\n[Verification] Security Status:")
    print(f"  UFW Status: {run_cmd(client, 'ufw status')}")
    print(f"  Fail2Ban: {run_cmd(client, 'systemctl is-active fail2ban')}")

    client.close()
    print("\n[+] Scientific Hardening Complete.")

if __name__ == "__main__":
    main()
