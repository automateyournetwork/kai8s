import streamlit as st
import requests
import json

# Define the function to send requests to the models
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

# Streamlit app UI
def chat_interface():
    st.title("KAI8 - Multi-AI Chat with Consensus")
    user_input = st.text_input("Ask a question:")
    models = ["gemma", "aya", "llama3", "mistral", "wizardlm2", "qwen2", "phi3", "tinyllama", "openchat"]

    if user_input and st.button("Send"):
        with st.spinner("Thinking..."):
            all_results = []
            for model in models:
                response = send_request(model, user_input)
                st.write(f"Response from {model}: {response}")
                all_results.append({"model": model, "response": response})

            # Attempt to reach a consensus (optional)
            consensus_prompt = (
                f"I am asking you to try and come to consensus with other LLMs on the answer to this question: "
                f"{user_input} Here are the answers from each LLM so far: {all_results}"
            )
            consensus_responses = []
            for model in models:
                consensus_response = send_request(model, consensus_prompt)
                st.write(f"Consensus response from {model}: {consensus_response}")
                consensus_responses.append(consensus_response)

            final_consensus_prompt = (
                f"I am asking you to try and come to consensus with other LLMs on the answer to this question: "
                f"{user_input} Here are the consensus answers from each LLM so far: {consensus_responses}"
            )
            final_consensus_responses = []
            for model in models:
                final_consensus_response = send_request(model, final_consensus_prompt)
                st.write(f"Final consensus response from {model}: {final_consensus_response}")
                final_consensus_responses.append(final_consensus_response)

# Run the Streamlit app
if __name__ == "__main__":
    chat_interface()
