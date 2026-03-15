import json
import os

PORTFOLIO_DIR = "/home/nishan/portfolio"
CONFIG_FILE = os.path.join(PORTFOLIO_DIR, "claw_config.json")

def setup_config():
    data = {"grok_key": "AIzaSyCjhqXrlhIg44slJUy93o81Wd4Wl_EKMmY"}
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print("[+] Config overwritten successfully with Gemini Key.")

if __name__ == "__main__":
    setup_config()
