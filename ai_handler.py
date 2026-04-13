
import os
from google import genai
from google.genai import types
from openai import OpenAI
from system_prompt import get_system_prompt

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
gemini_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

REPLIT_AI_BASE_URL = os.getenv("AI_INTEGRATIONS_OPENAI_BASE_URL", "")
REPLIT_AI_API_KEY = os.getenv("AI_INTEGRATIONS_OPENAI_API_KEY", "")
if REPLIT_AI_BASE_URL and REPLIT_AI_API_KEY:
    replit_openai_client = OpenAI(base_url=REPLIT_AI_BASE_URL, api_key=REPLIT_AI_API_KEY)
else:
    replit_openai_client = None

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
user_openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

GEMINI_MODELS = [
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash",
]


def generate_ai_response(user_input, user_state, history, user_level="beginner", system_prompt_override=None):
    provider = os.getenv("AI_PROVIDER", "gemini").lower()
    system_prompt = system_prompt_override or get_system_prompt(user_level)

    history_str = "\n".join(
        [f"User: {msg['user']}\nBot: {msg['bot']}" for msg in history[-5:]]
    )
    full_input = f"""
USER STATE: {user_state}

CHAT HISTORY:
{history_str}

USER INPUT:
{user_input}
"""
    return call_ai(provider, system_prompt, full_input)


def call_ai(provider, prompt, input_text):
    if provider == "openai":
        result = call_replit_openai_api(prompt, input_text)
        if result is None:
            result = call_user_openai_api(prompt, input_text)
        return result or "Maaf, layanan AI tidak tersedia saat ini."
    else:
        result = call_gemini_api(prompt, input_text)
        if result is not None:
            return result
        result = call_replit_openai_api(prompt, input_text)
        if result is not None:
            return result
        result = call_user_openai_api(prompt, input_text)
        if result is not None:
            return result
        return "Waduh, semua layanan AI lagi bermasalah nih. Coba lagi beberapa saat ya!"


def call_gemini_api(prompt, input_text):
    if not gemini_client:
        return None
    for model_name in GEMINI_MODELS:
        try:
            response = gemini_client.models.generate_content(
                model=model_name,
                config=types.GenerateContentConfig(system_instruction=prompt),
                contents=input_text,
            )
            return response.text
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "403" in err_str or "401" in err_str:
                return None
            continue
    return None


def call_replit_openai_api(prompt, input_text):
    if not replit_openai_client:
        return None
    try:
        response = replit_openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": input_text},
            ],
        )
        return response.choices[0].message.content
    except Exception:
        return None


def call_user_openai_api(prompt, input_text):
    if not user_openai_client:
        return None
    try:
        response = user_openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": input_text},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception:
        return None
