#!/bin/bash
cd /home/nishan/portfolio
# Install beautifulsoup4 if not present
venv/bin/pip install bs4 requests lxml --quiet
venv/bin/python3 scrape_book.py
echo "[+] Textbook Scraped and Stored securely."
