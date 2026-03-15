import os
import subprocess

PORTFOLIO_DIR = "/home/nishan/portfolio"
CONFIG_FILE = os.path.join(PORTFOLIO_DIR, "claw_config.json")
BOT_LOG = os.path.join(PORTFOLIO_DIR, "bot_run.log")
HEALTH_LOG = os.path.join(PORTFOLIO_DIR, "bot_health.log")

def scrub():
    print("[+] Overwriting config with empty dictionary...")
    with open(CONFIG_FILE, 'w') as f:
        f.write('{"grok_key": null}')
    
    print("[+] Emptying log files for trace-cache safety...")
    if os.path.exists(BOT_LOG):
        with open(BOT_LOG, 'w') as f: f.write('')
    if os.path.exists(HEALTH_LOG):
        with open(HEALTH_LOG, 'w') as f: f.write('')

    print("[+] Cleaning test scripts on server workspace...")
    files_to_remove = [
        "test_gemini.py", "test_gemini_rest.py", "list_gemini_models.py",
        "filter_gemini_models.py", "list_grok_models.py", "claw_config_setup.py"
    ]
    for filename in files_to_remove:
        filepath = os.path.join(PORTFOLIO_DIR, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Removed local API module: {filename}")

if __name__ == "__main__":
    scrub()
