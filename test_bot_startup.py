import subprocess
import time

print("Starting bot in foreground...")
p = subprocess.Popen(["/home/nishan/portfolio/venv/bin/python3", "/home/nishan/portfolio/telegram_bridge.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait 5 seconds to catch boot crash or start
time.sleep(5)

# Check if process is still running
if p.poll() is None:
    print("\n[+] Bot started successfully and is still running foreground!")
    p.terminate()
else:
    print("\n[-] Bot CRASHED on startup!")
    stdout, stderr = p.communicate()
    print("=== STDOUT ===")
    print(stdout.decode('utf-8', 'ignore'))
    print("=== STDERR ===")
    print(stderr.decode('utf-8', 'ignore'))
    print("===============")
