import sys
import requests
import json
import time

def explain_config():
    url = "http://localhost:11434/api/generate"
    headers = {
        "Content-Type": "application/json"
    }
    # Replace newline characters with spaces
    data = {
        "model": "llama3",
        "prompt": "Why is the sky blue?",
        "stream": False
    }

    try:
        print(f"Sending request to {url} with data: {json.dumps(data)}")  # Debug: Print request data
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        # Wait for a maximum of 120 seconds for a response
        wait_time = 0
        while wait_time < 0 and response.status_code != 200:
            print("Waiting for response...")
            time.sleep(5)
            wait_time += 5
            response = requests.post(url, headers=headers, data=json.dumps(data))
        
        print(f"Response status code: {response.status_code}")  # Debug: Print response status code
        print(f"Response text: {response.text}")  # Debug: Print response text
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"Response received: {response_data}")  # Debug: Print the response data
            ai_response = response_data.get('response', '')
            return ai_response
        else:
            error_msg = f"Error: Received status code {response.status_code}, Response: {response.text}"
            print(error_msg)  # Debug: Print status code and response text if not 200
            return error_msg
    except Exception as e:
        exception_msg = f"Exception during API call: {e}"
        print(exception_msg)  # Debug: Print any exceptions during the API call
        return exception_msg

if __name__ == "__main__":
    try:             
        test = explain_config()
        print(f"Explanation: {test}")
        
    except Exception as e:
        error_msg = f"Error: {e}"
        print(error_msg)  # Print any exceptions during the script execution