import openai

key = "AIzaSyCjhqXrlhIg44slJUy93o81Wd4Wl_EKMmY"
client = openai.OpenAI(api_key=key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

try:
    response = client.chat.completions.create(
        model="gemini-1.5-flash",
        messages=[{"role": "user", "content": "Hello, responding from server. Say 'Gemini Online'"}]
    )
    print("=== TEST SUCCESS ===")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"=== TEST FAILED ===\n{e}")
