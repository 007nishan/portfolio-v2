#!/bin/bash
cd /home/nishan/portfolio
venv/bin/python3 scrub_keys.py
echo '6WKW5_3w2w5121' | sudo -S systemctl restart bot.service
echo "[+] API Configuration Cleared securely."
