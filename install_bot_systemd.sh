#!/bin/bash
cd /home/nishan/portfolio
venv/bin/python3 setup_bot_systemd.py
echo '6WKW5_3w2w5121' | sudo -S mv bot.service /etc/systemd/system/bot.service
echo '6WKW5_3w2w5121' | sudo -S systemctl daemon-reload
echo '6WKW5_3w2w5121' | sudo -S systemctl enable bot.service
echo '6WKW5_3w2w5121' | sudo -S systemctl restart bot.service
echo "[+] Systemd configuration applied for bot.service"
echo '6WKW5_3w2w5121' | sudo -S systemctl status bot.service --no-pager
