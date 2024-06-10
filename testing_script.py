import requests
import json

def send_request(prompt):
    url = "http://localhost:80/api/generate"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json().get('response', '')
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

if __name__ == "__main__":
    prompt = "Why is the sky blue?"
    result = send_request(prompt)
    print(f"Response: {result}")
