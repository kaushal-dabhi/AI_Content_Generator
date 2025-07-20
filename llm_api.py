import requests
from datetime import datetime, timedelta
import streamlit as st

# Globals to track rate limit
next_request_time = None

def generate_content(prompt, max_tokens=150):
    """
    Calls Groq Llama 3 model for content generation via the Chat Completions API.
    Handles rate limits and quota limits gracefully.
    Raises Exception with a clear message as needed.
    """
    global next_request_time
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = st.secrets.get("GROQ_API_KEY")
    
    # Early check for missing API key
    if not api_key:
        raise Exception("GROQ_API_KEY not found in Streamlit secrets. Please check your .streamlit/secrets.toml configuration.")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant who generates high-quality creative content."
            },
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }

    # Rate limit: honor cooldown
    if next_request_time and datetime.now() < next_request_time:
        wait = (next_request_time - datetime.now()).seconds
        raise Exception(f"Rate limit previously reached. Please retry after {wait} seconds.")

    response = requests.post(api_url, headers=headers, json=payload, timeout=30)

    # Handle explicit rate limit response
    if response.status_code == 429:
        retry_after = int(response.headers.get("retry-after", "60"))
        next_request_time = datetime.now() + timedelta(seconds=retry_after)
        raise Exception(f"Rate limit exceeded. Try again in {retry_after} seconds.")

    # Handle quota exhaustion proactively
    rem_requests = int(response.headers.get("x-ratelimit-remaining-requests", "1"))
    if rem_requests <= 0:
        raise Exception("Daily quota exhausted. Please wait for quota to reset.")

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()
