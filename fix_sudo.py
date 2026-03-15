"""
fix_sudo.py
-----------
Forcefully sets up passwordless sudo for 'nishan'
"""
import paramiko

HOST = "192.168.1.150"
USER = "nishan"
PASSWORD = "6WKW5_3w2w5121"

def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD)
    
    # Correct way to write to sudoers: use a heredoc with sudo -S
    sudo_entry = f"{USER} ALL=(ALL) NOPASSWD:ALL"
    cmd = f"echo '{PASSWORD}' | sudo -S bash -c \"echo '{sudo_entry}' > /etc/sudoers.d/90-nishan-overrides && chmod 0440 /etc/sudoers.d/90-nishan-overrides\""
    
    print(f"[*] Applying passwordless sudo rule...")
    stdin, stdout, stderr = client.exec_command(cmd)
    print(stdout.read().decode())
    print(stderr.read().decode())
    
    # Verify
    print("[*] Verifying...")
    stdin, stdout, stderr = client.exec_command("sudo -n whoami")
    res = stdout.read().decode().strip()
    if res == "root":
        print("[+] Passwordless sudo is now WORKING.")
    else:
        print(f"[-] Still failed. Output: {res}")
        print(stderr.read().decode())

    client.close()

if __name__ == "__main__":
    main()
