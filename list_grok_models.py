import openai
import json
import os

PORTFOLIO_DIR = "/home/nishan/portfolio"
CONFIG_FILE = os.path.join(PORTFOLIO_DIR, "claw_config.json")

def list_models():
    if not os.path.exists(CONFIG_FILE):
        print("CONFIG_FILE_NOT_FOUND")
        return

    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    
    key = config.get("grok_key")
    if not key:
        print("KEY_NOT_FOUND")
        return

    client = openai.OpenAI(api_key=key, base_url="https://api.x.ai/v1")
    
    try:
        models = client.models.list()
        print("\n=== AVAILABLE MODELS ===")
        for m in models:
            print(f"- {m.id}")
        print("========================\n")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    list_models()
