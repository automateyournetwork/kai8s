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

# Initialize session state
if 'selected_models' not in st.session_state:
    st.session_state.selected_models = {model: False for model in ["gemma", "aya", "llama3", "mistral", "wizardlm2", "qwen2", "phi3", "tinyllama", "openchat", "yi", "falcon2"]}
if 'step' not in st.session_state:
    st.session_state.step = 1

# Define the model selection page
def model_selection():
    st.title("Select Models")
    all_models = ["gemma", "aya", "llama3", "mistral", "wizardlm2", "qwen2", "phi3", "tinyllama", "openchat", "yi", "falcon2"]

    def select_all():
        for model in all_models:
            st.session_state.selected_models[model] = True

    def deselect_all():
        for model in all_models:
            st.session_state.selected_models[model] = False

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('Select All Models'):
            select_all()
    with col2:
        if st.button('Deselect All Models'):
            deselect_all()

    col1, col2, col3 = st.columns(3)
    for idx, model in enumerate(all_models):
        col = [col1, col2, col3][idx % 3]
        with col:
            st.session_state.selected_models[model] = st.checkbox(model, value=st.session_state.selected_models[model], key=model)

    if st.button('Next'):
        st.session_state.step = 2

# Define the chat interface page
def chat_interface():
    st.title("KAI8 - Multi-AI Chat with Consensus")
    user_input = st.text_input("Ask a question:")
    selected_models = [model for model in st.session_state.selected_models if st.session_state.selected_models[model]]

    if user_input and st.button("Send"):
        with st.spinner("Thinking..."):
            all_results = []
            for model in selected_models:
                response = send_request(model, user_input)
                st.write(f"Response from {model}: {response}")
                st.markdown("""---""")
                all_results.append({"model": model, "response": response})

            # Attempt to reach a consensus (optional)
            consensus_prompt = (
                f"I am asking you to try and come to consensus with other LLMs on the answer to this question: "
                f"{user_input} Here are the answers from each LLM so far: {all_results}"
            )
            consensus_responses = []
            for model in selected_models:
                consensus_response = send_request(model, consensus_prompt)
                st.write(f"Consensus response from {model}: {consensus_response}")
                st.markdown("""---""")
                consensus_responses.append(consensus_response)

            final_consensus_prompt = (
                f"I am asking you to try and come to consensus with other LLMs on the answer to this question: "
                f"{user_input} Here are the consensus answers from each LLM so far: {consensus_responses}"
            )
            final_consensus_responses = []
            for model in selected_models:
                final_consensus_response = send_request(model, final_consensus_prompt)
                st.write(f"Final consensus response from {model}: {final_consensus_response}")
                st.markdown("""---""")
                final_consensus_responses.append(final_consensus_response)

# Run the Streamlit app
if __name__ == "__main__":
    if st.session_state.step == 1:
        model_selection()
    elif st.session_state.step == 2:
        chat_interface()
