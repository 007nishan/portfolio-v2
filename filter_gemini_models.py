import requests
import json

key = "AIzaSyCjhqXrlhIg44slJUy93o81Wd4Wl_EKMmY"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"

try:
    response = requests.get(url)
    res_json = response.json()
    
    print("=== MODELS SUPPORTING generateContent ===")
    if "models" in res_json:
        for m in res_json["models"]:
            if "generateContent" in m.get("supportedGenerationMethods", []):
                print(f"- {m['name']} ({m.get('displayName', '')})")
    else:
        print("No models key found.")
except Exception as e:
    print(f"Exception: {e}")
