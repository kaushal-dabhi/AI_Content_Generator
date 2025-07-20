
import requests
import streamlit as st

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

def generate_reply(persona, message):
    if not message:
        return "Please enter a message."

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",  # ✅ Groq-supported model
        "messages": [
            {"role": "system", "content": f"You are a {persona} personality chatbot."},
            {"role": "user", "content": message}
        ]
    }

    # DEBUG: Print payload info
    print("=== DEBUG GROQ ===")
    print("Headers:", headers)
    print("Payload:", data)

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
