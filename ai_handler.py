import os
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv
from system_prompt import SYSTEM_PROMPT

load_dotenv()

# Setup Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
    genai.configure(api_key=GEMINI_API_KEY)

# Setup OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY and OPENAI_API_KEY != "your_openai_api_key_here":
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
else:
    openai_client = None

def generate_ai_response(user_input, user_state, history):
    provider = os.getenv("AI_PROVIDER", "gemini").lower()
    
    # Format the history string (Ambil 5 pasang percakapan terakhir)
    history_str = "\n".join([f"User: {msg['user']}\nBot: {msg['bot']}" for msg in history[-5:]])
    
    full_input = f"""
USER STATE: {user_state}

CHAT HISTORY:
{history_str}

USER INPUT:
{user_input}
"""
    return call_ai(provider, SYSTEM_PROMPT, full_input)

def call_ai(provider, prompt, input_text):
    if provider == "openai":
        return call_openai_api(prompt, input_text)
    else:
        return call_gemini_api(prompt, input_text)

def call_gemini_api(prompt, input_text):
    try:
        # Menggunakan model flash untuk respons cepat
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=prompt)
        response = model.generate_content(input_text)
        return response.text
    except Exception as e:
        return f"Waduh, ada sedikit masalah teknis nih (Gemini: {str(e)}). Coba ketik ulang ya!"

def call_openai_api(prompt, input_text):
    try:
        if not openai_client:
            return "Waduh, kunci API OpenAI belum diatur nih di server."
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": input_text}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Waduh, ada sedikit masalah teknis nih (OpenAI: {str(e)}). Coba ketik ulang ya!"
