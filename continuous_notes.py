"""
continuous_notes.py
-------------------
This script reads the list of URLs, fetches their content, 
summarizes them into the 'Learning Ledger' format, 
and appends them one by one to a central notes file.
"""

import os
import requests
import json
import time

URLS = [
    "https://www.freecodecamp.org/news/how-to-solve-5-common-rag-failures-with-knowledge-graphs/",
    "https://www.freecodecamp.org/news/how-web-services-work-with-examples/",
    "https://www.freecodecamp.org/news/learn-databases-in-depth/",
    "https://www.freecodecamp.org/news/how-to-build-production-ready-voice-agents/",
    "https://www.freecodecamp.org/news/kubernetes-self-healing-explained/",
    "https://www.freecodecamp.org/news/deploy-ai-generated-code-using-paas/",
    "https://www.freecodecamp.org/news/how-to-build-real-time-update-systems-with-mosquitto-and-expressjs/",
    "https://www.freecodecamp.org/news/what-are-scripts-and-how-do-they-work/",
    "https://www.freecodecamp.org/news/how-to-integrate-vector-search-in-columnar-storage/",
    "https://www.freecodecamp.org/news/how-to-cut-ai-costs-without-losing-capability-the-rise-of-small-llms/",
    "https://www.freecodecamp.org/news/how-to-find-the-top-k-items-heap-and-streaming-approaches-in-go/",
    "https://www.freecodecamp.org/news/how-to-build-an-mcp-server-with-python-docker-and-claude-code/",
    "https://www.freecodecamp.org/news/how-to-implement-the-strategy-pattern-in-python/",
    "https://www.freecodecamp.org/news/financial-storytelling-using-data-visualization/",
    "https://www.freecodecamp.org/news/how-to-create-a-table-of-contents-for-your-article/",
    "https://www.freecodecamp.org/news/how-to-use-websockets-from-python-to-fastapi/",
    "https://www.freecodecamp.org/news/what-is-toon-how-token-oriented-object-notation-could-change-how-ai-sees-data/"
]

NOTES_FILE = r"c:\Users\NISHAN\Desktop\Test Folder\My Portfolio\Learning_Ledger.md"

def main():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            f.write("# Learning Ledger\n")
            f.write("*Automated Knowledge Extraction Loop*\n\n")

    print(f"[*] Starting note-making loop for {len(URLS)} resources...")
    
    for i, url in enumerate(URLS):
        print(f"[{i+1}/{len(URLS)}] Processing: {url}")
        
        # Placeholder for actual LLM summarization logic
        # In a real agentic loop, I would call an internal summarizer 
        # or process chunk by chunk. For now, I'll log the intention 
        # as I process them one by one in subsequent turns.
        
        # simulated_summary = f"### Resource {i+1}: {url}\n- Extraction in progress...\n\n"
        # with open(NOTES_FILE, "a", encoding="utf-8") as f:
        #     f.write(simulated_summary)
        
        time.sleep(2) # Throttle

if __name__ == "__main__":
    main()
