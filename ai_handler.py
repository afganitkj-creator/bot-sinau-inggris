import os
from google import genai
from google.genai import types
from openai import OpenAI
from system_prompt import SYSTEM_PROMPT

# Setup Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
gemini_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

# Setup Replit AI integration (OpenAI-compatible, no user API key needed)
REPLIT_AI_BASE_URL = os.getenv("AI_INTEGRATIONS_OPENAI_BASE_URL", "")
REPLIT_AI_API_KEY = os.getenv("AI_INTEGRATIONS_OPENAI_API_KEY", "")
if REPLIT_AI_BASE_URL and REPLIT_AI_API_KEY:
    replit_openai_client = OpenAI(base_url=REPLIT_AI_BASE_URL, api_key=REPLIT_AI_API_KEY)
else:
    replit_openai_client = None

# Setup user's own OpenAI key as last-resort fallback
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
user_openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# Gemini model fallback chain
GEMINI_MODELS = [
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash",
]

def generate_ai_response(user_input, user_state, history):
    provider = os.getenv("AI_PROVIDER", "gemini").lower()

    # Format the history string (last 5 exchanges)
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
        # Try Replit AI first, then user's own key
        result = call_replit_openai_api(prompt, input_text)
        if result is None:
            result = call_user_openai_api(prompt, input_text)
        return result
    else:
        # Try Gemini → Replit AI → user's own OpenAI key
        gemini_result = call_gemini_api(prompt, input_text)
        if gemini_result is not None:
            return gemini_result

        replit_result = call_replit_openai_api(prompt, input_text)
        if replit_result is not None:
            return replit_result

        user_result = call_user_openai_api(prompt, input_text)
        if user_result is not None:
            return user_result

        return "Waduh, semua layanan AI lagi bermasalah nih. Coba lagi beberapa saat ya!"

def call_gemini_api(prompt, input_text):
    """Returns response text on success, None on failure."""
    if not gemini_client:
        return None

    last_error = None
    for model_name in GEMINI_MODELS:
        try:
            response = gemini_client.models.generate_content(
                model=model_name,
                config=types.GenerateContentConfig(system_instruction=prompt),
                contents=input_text,
            )
            return response.text
        except Exception as e:
            last_error = e
            err_str = str(e)
            # Stop trying other models on quota/auth errors
            if "429" in err_str or "403" in err_str or "401" in err_str:
                return None
            # Try next model on not-found errors
            continue

    return None

def call_replit_openai_api(prompt, input_text):
    """Returns response text on success, None on failure."""
    if not replit_openai_client:
        return None
    try:
        response = replit_openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": input_text}
            ],
        )
        return response.choices[0].message.content
    except Exception:
        return None

def call_user_openai_api(prompt, input_text):
    """Returns response text on success, None on failure."""
    if not user_openai_client:
        return None
    try:
        response = user_openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": input_text}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception:
        return None
