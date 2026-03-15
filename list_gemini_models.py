import requests
import json

key = "AIzaSyCjhqXrlhIg44slJUy93o81Wd4Wl_EKMmY"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"

try:
    response = requests.get(url)
    print("=== AVAILABLE MODELS ===")
    res_json = response.json()
    print(json.dumps(res_json, indent=2))
except Exception as e:
    print(f"=== TEST EXCEPTION ===\n{e}")
