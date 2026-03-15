import requests
import json

key = "AIzaSyCjhqXrlhIg44slJUy93o81Wd4Wl_EKMmY"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"

headers = {'Content-Type': 'application/json'}
data = {
    "contents": [{
        "parts": [{"text": "Say 'Online response from Gemini core'"}]
    }]
}

try:
    response = requests.post(url, headers=headers, json=data)
    print("=== TEST RESPONSE ===")
    res_json = response.json()
    print(json.dumps(res_json, indent=2))
    
    # Extract text correctly
    if "candidates" in res_json:
        text = res_json["candidates"][0]["content"]["parts"][0]["text"]
        print(f"\nSUCCESS TEXT: {text}")
    else:
        print("\nERROR: Candidates key absent.")
except Exception as e:
    print(f"=== TEST EXCEPTION ===\n{e}")
