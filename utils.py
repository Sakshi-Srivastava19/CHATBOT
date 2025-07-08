import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Load key from Streamlit secrets or .env fallback
API_KEY = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY"))
API_URL = "https://openrouter.ai/v1/chat/completions"


HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

BOT_PERSONAS = {
    "Study Assistant": "You are a helpful AI tutor for school and college topics.",
    "Travel Guide": "You are a travel expert helping users discover destinations and plan trips.",
    "Therapist": "You are a kind and empathetic listener offering mental support.",
    "Career Coach": "You guide users with resumes, job interviews, and professional growth.",
    "Friendly Chat": "You are a cheerful, casual chatbot who just loves to chat about anything!"
}

def get_bot_response(user_input: str, role: str) -> str:
    try:
        system_prompt = BOT_PERSONAS.get(role, BOT_PERSONAS["Friendly Chat"])
        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        }
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"
