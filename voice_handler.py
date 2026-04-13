
import os
import tempfile
import logging

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


async def transcribe_and_analyze(voice_message, bot, ai_call_fn, user_level="beginner"):
    """
    Download voice message, transcribe via Whisper, then analyze grammar.
    Returns (transcription, feedback) or (None, error_msg).
    """
    if not OPENAI_API_KEY:
        return None, (
            "Maaf, fitur analisis suara butuh OpenAI API key.\n"
            "Untuk sekarang, kamu bisa kirim teks aja ya!"
        )

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        # Download voice file
        file_obj = await bot.get_file(voice_message.file_id)
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
            tmp_path = tmp.name

        await file_obj.download_to_drive(tmp_path)

        # Transcribe with Whisper
        with open(tmp_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en",
            )

        os.unlink(tmp_path)
        text = transcript.text.strip()

        if not text:
            return None, "Hmm, aku tidak bisa menangkap suaramu. Coba kirim lagi dengan jelas ya!"

        # Analyze grammar + vocabulary using AI
        level_ctx = {
            "beginner": "Give very simple feedback in Indonesian. Praise effort first.",
            "intermediate": "Give balanced feedback in Indonesian about grammar and vocabulary.",
            "advanced": "Give detailed feedback in Indonesian about grammar, vocabulary, and naturalness.",
        }.get(user_level, "Give simple feedback in Indonesian.")

        analysis_prompt = (
            "You are English Mas/Mbak, a friendly English tutor for Indonesians. "
            "Analyze the following English speech transcription and give feedback. "
            f"{level_ctx}\n\n"
            "Structure your response as:\n"
            "🎤 Yang kamu ucapkan: [transcription]\n"
            "✅ Koreksi grammar: [corrections or 'Sudah bagus!']\n"
            "📝 Versi lebih natural: [improved version]\n"
            "💡 Tips: [1 quick tip]\n"
            "⭐ Skor: X/10\n\n"
            f"Transcription to analyze: \"{text}\""
        )

        feedback = ai_call_fn("gemini", analysis_prompt, analysis_prompt)
        return text, feedback

    except Exception as e:
        logger.error(f"Voice handler error: {e}")
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
        return None, f"Ada masalah saat memproses suaramu. Coba lagi ya! ({str(e)[:50]})"
