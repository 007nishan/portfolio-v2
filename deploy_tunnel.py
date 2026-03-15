"""
deploy_tunnel.py
----------------
1. Connects to remote server with password (one-time)
2. Installs the SSH public key so future connections are passwordless
3. Kills any stale tunnels
4. Starts cloudflared tunnel and extracts the public URL
5. Prints the public URL
"""

import paramiko
import time
import re
import sys

HOST = "192.168.1.150"
USER = "nishan"
PASSWORD = "6WKW5_3w2w5121"
PORT_TO_EXPOSE = 5001

# Read local public key
import os
pub_key_path = os.path.expanduser("~/.ssh/id_rsa.pub")
with open(pub_key_path, "r") as f:
    pub_key = f.read().strip()


def run(client, cmd, timeout=15, print_output=True):
    """Run a blocking command and return stdout."""
    print(f"  >> {cmd}")
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    stdout.channel.settimeout(timeout)
    try:
        out = stdout.read().decode("utf-8", errors="ignore")
    except Exception:
        out = ""
    try:
        err = stderr.read().decode("utf-8", errors="ignore")
    except Exception:
        err = ""
    if print_output and out.strip():
        print(f"     {out.strip()}")
    if err.strip() and print_output:
        print(f"  [err] {err.strip()}")
    return out.strip()


def run_bg(client, cmd):
    """Fire-and-forget a background command (nohup ... &). Does NOT wait for output."""
    print(f"  >> [bg] {cmd}")
    transport = client.get_transport()
    chan = transport.open_session()
    chan.exec_command(cmd)
    chan.close()


def connect():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASSWORD, timeout=10)
    print(f"[+] Connected to {HOST}")
    return client


def install_ssh_key(client):
    run(client, "mkdir -p ~/.ssh && chmod 700 ~/.ssh")
    # Avoid duplicate keys
    check = run(client, f"grep -qF '{pub_key}' ~/.ssh/authorized_keys 2>/dev/null && echo EXISTS || echo NEW")
    if "NEW" in check:
        run(client, f"echo '{pub_key}' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys")
        print("[+] SSH public key installed — future connections passwordless")
    else:
        print("[+] SSH public key already installed")


def kill_tunnels(client):
    run(client, "pkill -f cloudflared 2>/dev/null || true", timeout=5)
    run(client, "pkill -f ngrok 2>/dev/null || true", timeout=5)
    time.sleep(1)


CF_BIN = "~/.local/bin/cloudflared"
CF_BIN_EXPANDED = "/home/nishan/.local/bin/cloudflared"


def install_cloudflared(client):
    """Install cloudflared to ~/.local/bin (no sudo needed)."""
    check = run(client, f"test -x {CF_BIN_EXPANDED} && echo OK || echo MISSING", print_output=False)
    if "MISSING" in check:
        print("[*] cloudflared not found — installing to ~/.local/bin ...")
        run(client, "mkdir -p ~/.local/bin")
        run(client,
            f"curl -fsSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 "
            f"-o {CF_BIN_EXPANDED} && chmod +x {CF_BIN_EXPANDED}",
            timeout=60
        )
        out = run(client, f"{CF_BIN_EXPANDED} --version 2>&1", print_output=True)
        print(f"[+] cloudflared installed: {out}")
    else:
        out = run(client, f"{CF_BIN_EXPANDED} --version 2>&1", print_output=False)
        print(f"[+] cloudflared already installed: {out}")


def start_cloudflared(client):
    """Start cloudflared and poll for the trycloudflare.com URL."""
    LOG = "/tmp/cf_tunnel.log"
    run(client, f"rm -f {LOG}")
    run_bg(client, f"{CF_BIN_EXPANDED} tunnel --url http://localhost:{PORT_TO_EXPOSE} > {LOG} 2>&1")

    print("[*] Waiting for cloudflared to establish tunnel (up to 35s)...")
    for i in range(35):
        time.sleep(1)
        out = run(client, f"cat {LOG} 2>/dev/null || echo ''", print_output=False)
        match = re.search(r"https://[a-z0-9\-]+\.trycloudflare\.com", out)
        if match:
            return match.group(0)
        sys.stdout.write(f"\r  ...{i+1}s")
        sys.stdout.flush()
    print()
    run(client, f"tail -20 {LOG}")
    return None


def ensure_portfolio_running(client):
    """Make sure the Flask app is running on port 5001."""
    check = run(client, f"ss -tlnp 2>/dev/null | grep :{PORT_TO_EXPOSE} || echo NOT_RUNNING", print_output=False)
    if "NOT_RUNNING" in check or str(PORT_TO_EXPOSE) not in check:
        print(f"[!] Portfolio not running on port {PORT_TO_EXPOSE}, starting it...")
        # Use systemd if available, else start manually as background
        svc = run(client, "systemctl is-active portfolio 2>/dev/null || echo inactive", print_output=False)
        if "active" in svc:
            run(client, "sudo systemctl restart portfolio")
        else:
            run_bg(client, "cd ~/portfolio && source venv/bin/activate && nohup python app.py > /tmp/portfolio.log 2>&1")
        time.sleep(4)
        print(f"[+] Portfolio started")
    else:
        print(f"[+] Portfolio already running on port {PORT_TO_EXPOSE}")


def main():
    print("=" * 55)
    print("  Portfolio Public URL Setup")
    print("=" * 55)

    client = connect()

    print("\n[1] Installing SSH key...")
    install_ssh_key(client)

    print("\n[2] Ensuring portfolio server is running...")
    ensure_portfolio_running(client)

    print("\n[3] Installing cloudflared if needed...")
    install_cloudflared(client)

    print("\n[4] Killing old tunnels...")
    kill_tunnels(client)

    print("\n[5] Starting cloudflared tunnel...")
    url = start_cloudflared(client)

    if url:
        print(f"\n{'='*55}")
        print(f"  --> PUBLIC URL: {url}")
        print(f"{'='*55}")
    else:
        print("\n[!] cloudflared did not return a URL. Dumping log:")
        run(client, "cat /tmp/cf_tunnel.log")
        print("\n[!] Please check if cloudflared is installed on the server.")

    client.close()


if __name__ == "__main__":
    main()
