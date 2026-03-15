import requests
from bs4 import BeautifulSoup
import os
import re
import json

TEXTBOOK_DIR = "/home/nishan/portfolio/data/textbook"
os.makedirs(TEXTBOOK_DIR, exist_ok=True)

urls = [
    "https://bsc-iitm.github.io/python-textbook/",
    "https://bsc-iitm.github.io/python-textbook/chapter-0/lesson-0/",
    "https://bsc-iitm.github.io/python-textbook/chapter-1/lesson-1.1/",
    "https://bsc-iitm.github.io/python-textbook/chapter-1/lesson-1.2/",
    "https://bsc-iitm.github.io/python-textbook/chapter-1/lesson-1.3/",
    "https://bsc-iitm.github.io/python-textbook/chapter-1/lesson-1.4/",
    "https://bsc-iitm.github.io/python-textbook/chapter-1/lesson-1.5/",
    "https://bsc-iitm.github.io/python-textbook/chapter-1/lesson-1.6/",
    "https://bsc-iitm.github.io/python-textbook/chapter-2/lesson-2.1/",
    "https://bsc-iitm.github.io/python-textbook/chapter-2/lesson-2.2/",
    "https://bsc-iitm.github.io/python-textbook/chapter-2/lesson-2.3/",
    "https://bsc-iitm.github.io/python-textbook/chapter-2/lesson-2.4/",
    "https://bsc-iitm.github.io/python-textbook/chapter-3/lesson-3.1/",
    "https://bsc-iitm.github.io/python-textbook/chapter-3/lesson-3.2/",
    "https://bsc-iitm.github.io/python-textbook/chapter-3/lesson-3.3/",
    "https://bsc-iitm.github.io/python-textbook/chapter-3/lesson-3.4/",
    "https://bsc-iitm.github.io/python-textbook/chapter-3/lesson-3.5/",
    "https://bsc-iitm.github.io/python-textbook/chapter-3/lesson-3.6/",
    "https://bsc-iitm.github.io/python-textbook/chapter-4/lesson-4.1/",
    "https://bsc-iitm.github.io/python-textbook/chapter-4/lesson-4.2/",
    "https://bsc-iitm.github.io/python-textbook/chapter-4/lesson-4.3/",
    "https://bsc-iitm.github.io/python-textbook/chapter-4/lesson-4.4/",
    "https://bsc-iitm.github.io/python-textbook/chapter-5/lesson-5.1/",
    "https://bsc-iitm.github.io/python-textbook/chapter-5/lesson-5.2/",
    "https://bsc-iitm.github.io/python-textbook/chapter-5/lesson-5.3/",
    "https://bsc-iitm.github.io/python-textbook/chapter-5/lesson-5.4/",
    "https://bsc-iitm.github.io/python-textbook/chapter-5/lesson-5.5/",
    "https://bsc-iitm.github.io/python-textbook/chapter-5/lesson-5.6/",
    "https://bsc-iitm.github.io/python-textbook/chapter-6/lesson-6.1/",
    "https://bsc-iitm.github.io/python-textbook/chapter-6/lesson-6.2/",
    "https://bsc-iitm.github.io/python-textbook/chapter-6/lesson-6.3/",
    "https://bsc-iitm.github.io/python-textbook/chapter-6/lesson-6.4/",
    "https://bsc-iitm.github.io/python-textbook/chapter-6/lesson-6.5/",
    "https://bsc-iitm.github.io/python-textbook/chapter-7/lesson-7.1/",
    "https://bsc-iitm.github.io/python-textbook/chapter-7/lesson-7.2/",
    "https://bsc-iitm.github.io/python-textbook/chapter-7/lesson-7.3/",
    "https://bsc-iitm.github.io/python-textbook/chapter-7/lesson-7.4/",
    "https://bsc-iitm.github.io/python-textbook/chapter-7/lesson-7.5/",
    "https://bsc-iitm.github.io/python-textbook/chapter-8/lesson-8.1/",
    "https://bsc-iitm.github.io/python-textbook/chapter-8/lesson-8.2/",
    "https://bsc-iitm.github.io/python-textbook/chapter-8/lesson-8.3/",
    "https://bsc-iitm.github.io/python-textbook/chapter-8/lesson-8.4/"
]

def scrape():
    book_index = []
    for url in urls:
        print(f"Scraping {url}...")
        try:
            res = requests.get(url, timeout=10)
            if res.status_code != 200:
                print(f"Skipped {url} due to code {res.status_code}")
                continue
            
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Find the main content area (usually article or main tag for docs)
            main_content = soup.find('article') or soup.find('main') or soup.body
            
            if main_content:
                # Remove IIT Madras logos or references explicitly
                for img in main_content.find_all('img'):
                    if 'iitm' in img.get('src', '').lower() or 'logo' in img.get('src', '').lower():
                        img.decompose()
                
                text_content = main_content.get_text('\n', strip=True)
                
                # Regex scrubs for IIT Madras
                text_content = re.sub(r'IIT\s*Madras', 'University', text_content, flags=re.IGNORECASE)
                text_content = re.sub(r'BSc\s*Degree', 'Python Course', text_content, flags=re.IGNORECASE)
                text_content = re.sub(r'IITM', 'University', text_content, flags=re.IGNORECASE)
                
                # Save to file
                filename = url.strip('/').split('/')[-1] if len(url.strip('/').split('/')) > 3 else "index"
                filename = filename.replace('.', '-') + ".txt"
                filepath = os.path.join(TEXTBOOK_DIR, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                
                book_index.append({
                    "url": url,
                    "file": filename,
                    "title": soup.title.string if soup.title else "Untitled"
                })
                print(f"Saved {filename}")
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    with open(os.path.join(TEXTBOOK_DIR, "index.json"), 'w') as f:
        json.dump(book_index, f, indent=4)
    print("[+] Scraped and cleaned complete textbook index.")

if __name__ == "__main__":
    scrape()
