import requests
import json
import time

def send_request(model, prompt):
    url = f"http://localhost:80/api/{model}/generate"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "keep_alive": 0
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json().get('response', '')
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

if __name__ == "__main__":
    prompt = "Why is the sky blue?"
    models = ["gemma", "aya", "llama3", "mistral", "qwen2", "yi", "phi3", "tinyllama"]
    for model in models:
        result = send_request(model, prompt)
        print(prompt)
        print(f"Response from {model}: {result}\n\n")