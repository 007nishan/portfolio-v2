import os

service_content = """[Unit]
Description=OpenClaw Telegram Bridge Client
After=network.target

[Service]
User=nishan
WorkingDirectory=/home/nishan/portfolio
ExecStart=/home/nishan/portfolio/venv/bin/python3 telegram_bridge.py
Restart=always
RestartSec=5
StandardOutput=append:/home/nishan/portfolio/bot_run.log
StandardError=append:/home/nishan/portfolio/bot_run.log

[Install]
WantedBy=multi-user.target
"""

def create_service_script():
    with open("bot.service", "w") as f:
        f.write(service_content)
    print("[+] bot.service file created locally.")

if __name__ == "__main__":
    create_service_script()
