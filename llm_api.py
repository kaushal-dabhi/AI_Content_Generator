
import requests
import os

# You can set your API key via Streamlit secrets or directly for local testing
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your_default_or_test_key_here")

def generate_reply(persona, message):
    prompt = f"You are a {persona}. Answer the user's question accordingly.\nUser: {message}\nAssistant:"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": f"You are a {persona} personality chatbot."},
            {"role": "user", "content": message}
        ]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def generate_content(prompt, max_tokens=150):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
