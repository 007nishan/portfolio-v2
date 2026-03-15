"""
book_generator.py
-----------------
Automates the creation of "Detailed Illustrative Books" as web pages.
Includes logic for expiring links and Telegram notification.
"""

import os
from datetime import datetime, timedelta
import secrets

BOOKS_DIR = r"c:\Users\NISHAN\Desktop\Test Folder\My Portfolio\portfolio\templates\books"
DATABASE = [] # Placeholder for active links and expiry

def generate_book_page(topic, content):
    token = secrets.token_urlsafe(16)
    expiry = datetime.now() + timedelta(hours=24)
    
    filename = f"{token}.html"
    filepath = os.path.join(BOOKS_DIR, filename)
    
    if not os.path.exists(BOOKS_DIR):
        os.makedirs(BOOKS_DIR)
        
    html_content = f"""
    {{% extends "base.html" %}}
    {{% block title %}}{topic}{{% endblock %}}
    {{% block content %}}
    <div class="container py-5">
        <h1 class="display-3 serif mb-4">{topic}</h1>
        <div class="book-body lead" style="line-height: 2; font-family: serif;">
            {content}
        </div>
        <hr>
        <p class="text-muted small">Special Access Link. Expires on: {expiry}</p>
    </div>
    {{% endblock %}}
    """
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    return f"https://allowing-together-accepts-apache.trycloudflare.com/read/{token}"

# This would be integrated with a background task and Telegram Bot API
print("[*] Book Generator Engine Ready.")
