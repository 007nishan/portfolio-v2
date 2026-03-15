"""
server_maintenance.py
---------------------
1. Extends the LVM partition to use the full 250GB SSD.
2. Configures passwordless sudo for the user so subsequent tasks don't hang.
"""

import paramiko
import time

HOST = "192.168.1.150"
USER = "nishan"
PASSWORD = "6WKW5_3w2w5121"

def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD)
    print(f"[+] Connected to {HOST}")

    def run_with_sudo(cmd):
        print(f"  >> sudo {cmd}")
        # Using -S to pass password via stdin
        full_cmd = f"echo '{PASSWORD}' | sudo -S {cmd}"
        stdin, stdout, stderr = client.exec_command(full_cmd)
        out = stdout.read().decode()
        err = stderr.read().decode()
        return out, err

    print("\n[1] Extending Disk (LVM)...")
    # 1. Extend the Logical Volume to 100% of free space in the Volume Group
    out, err = run_with_sudo("lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv")
    print(out if out else err)

    # 2. Resize the filesystem to fill the newly extended volume
    print("\n[2] Resizing Filesystem...")
    out, err = run_with_sudo("resize2fs /dev/ubuntu-vg/ubuntu-lv")
    print(out if out else err)

    print("\n[3] Configuring Passwordless Sudo (for seamless automation)...")
    # This adds a line to /etc/sudoers.d/ so 'nishan' never needs a password for sudo
    sudo_rule = f"{USER} ALL=(ALL) NOPASSWD:ALL"
    cmd = f"echo '{sudo_rule}' | tee /etc/sudoers.d/90-nishan-overrides"
    out, err = run_with_sudo(cmd)
    
    print("\n[Verification] Checking new disk size:")
    stdin, stdout, stderr = client.exec_command("df -h /")
    print(stdout.read().decode())

    client.close()

if __name__ == "__main__":
    main()
