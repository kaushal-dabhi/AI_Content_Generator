
# 🧠 AI Content Generator

This is a Streamlit-based web app that generates various types of creative content using the LLaMA 3 model via the Groq API.

---

## 🚀 Features

- Blog posts, Tweets, LinkedIn posts, Product Descriptions, etc.
- Tone control (Formal, Casual, Humorous, etc.)
- Optional keywords
- Demo fallback when API is rate-limited
- Download generated content
- Easy to deploy on Streamlit Cloud

---

## 📁 File Structure

- `app.py` – Streamlit frontend
- `llm_api.py` – API handler using Groq's LLaMA 3
- `README.md` – Project documentation

---

## 🔑 Setup Instructions

1. **Install dependencies:**

```bash
pip install streamlit requests
```

2. **Add your API Key:**

Create `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

3. **Run the app:**

```bash
streamlit run app.py
```

---

## 🌐 Deployment

You can deploy it to:

- [Streamlit Cloud](https://streamlit.io/cloud)
- Hugging Face Spaces
- Local server

---

## 🔗 API Info

This uses the [Groq LLaMA 3 API](https://console.groq.com/usage). Check your quota and limits before deploying live.

