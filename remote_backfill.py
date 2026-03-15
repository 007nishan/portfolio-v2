"""
remote_backfill.py
------------------
Runs fcc_sync.py --backfill directly on the remote server
so its own database gets updated to today's challenges.
"""

import paramiko
import time
import sys

HOST = "192.168.1.150"
USER = "nishan"
PASSWORD = "6WKW5_3w2w5121"


def connect():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=10)
    print(f"[+] Connected to {HOST}")
    return client


def run_stream(client, cmd, timeout=300):
    """Run a command and stream its output live."""
    print(f"\n  >> {cmd}\n")
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout, get_pty=True)
    # Stream output line by line
    for line in iter(stdout.readline, ""):
        sys.stdout.write(line)
        sys.stdout.flush()
    exit_code = stdout.channel.recv_exit_status()
    return exit_code


def main():
    print("=" * 60)
    print("  Remote FCC Backfill")
    print("=" * 60)

    client = connect()

    # Run backfill using the server venv
    cmd = "cd ~/portfolio && source venv/bin/activate && python fcc_sync.py --backfill"
    exit_code = run_stream(client, cmd)

    if exit_code == 0:
        print("\n[+] Backfill complete! Server DB is now up to date.")
    else:
        print(f"\n[!] Backfill exited with code {exit_code}")

    # Restart Flask so it picks up fresh data (if not using systemd)
    print("\n[*] Restarting portfolio server...")
    stdin, stdout, stderr = client.exec_command(
        "sudo systemctl restart portfolio 2>/dev/null || "
        "(pkill -f 'python app.py' 2>/dev/null; "
        "cd ~/portfolio && source venv/bin/activate && "
        "nohup python app.py > /tmp/portfolio.log 2>&1 &)"
    )
    time.sleep(3)
    print("[+] Server restarted.")

    client.close()


if __name__ == "__main__":
    main()
