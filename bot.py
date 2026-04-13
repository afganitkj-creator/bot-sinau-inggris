
import os
import logging
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from ai_handler import generate_ai_response, call_ai
from vocab_handler import (
    is_in_vocab_session, is_waiting_category,
    start_vocab_session, handle_category_choice,
    handle_vocab_answer, cancel_vocab_session,
)
from assessment_handler import (
    start_assessment, is_in_assessment,
    handle_assessment_answer, cancel_assessment,
)
from roleplay_handler import (
    start_roleplay, is_in_roleplay, is_choosing_scenario,
    handle_scenario_choice, get_active_scenario_prompt,
    increment_exchange, is_session_ending, cancel_roleplay,
)
from grammar_handler import (
    get_grammar_menu, start_grammar, is_in_grammar, is_choosing_grammar,
    handle_grammar_choice, show_grammar_exercise, handle_grammar_answer,
    cancel_grammar,
)
from voice_handler import transcribe_and_analyze
from user_profile import (
    get_profile, get_level, set_level, get_level_label,
    is_assessment_done, reset_profile,
)
from keep_alive import keep_alive

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

user_context = {}


async def get_or_create_context(user_id):
    if user_id not in user_context:
        user_context[user_id] = {"state": "STATE 1 (LEARNING MODE)", "history": []}
    return user_context[user_id]


# ─── /start ──────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    ctx = await get_or_create_context(user.id)
    ctx["state"] = "STATE 1 (LEARNING MODE)"
    ctx["history"] = []

    has_assessment = is_assessment_done(user.id)
    level_label = get_level_label(user.id) if has_assessment else None

    if has_assessment:
        level_info = f"Level kamu: *{level_label}* — kurikulummu sudah disesuaikan!\n\n"
    else:
        level_info = "Ketik /assessment dulu yuk untuk tau level kamu!\n\n"

    await update.message.reply_text(
        f"Halo {user.first_name}! 👋\n\n"
        "Aku *English Mas/Mbak* — tutor bahasa Inggrismu yang santai dan seru.\n\n"
        f"{level_info}"
        "Yang bisa kamu lakuin:\n"
        "🎯 /assessment — Tes level kamu (10 menit)\n"
        "💬 /roleplay — Simulasi percakapan nyata (wawancara, restoran, dll)\n"
        "📚 /grammar — Belajar grammar step-by-step\n"
        "🃏 /vocab — Latihan kosakata flashcard\n"
        "🎤 Kirim pesan suara — Aku analisis grammar-mu!\n\n"
        "Ketik /menu untuk panduan lengkap.",
        parse_mode="Markdown",
    )


# ─── /menu ───────────────────────────────────────────────────────────────────

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    level_label = get_level_label(user_id)
    await update.message.reply_text(
        f"📚 *Panduan English Mas/Mbak*\n"
        f"Level kamu: *{level_label}*\n\n"
        "*Fitur Utama:*\n"
        "🎯 /assessment — Tes penempatan level (10 soal)\n"
        "💬 /roleplay — Role-play AI: wawancara, restoran, bandara, dll\n"
        "📚 /grammar — Grammar Coach: 10 topik grammar + latihan\n"
        "🃏 /vocab — Flashcard kosakata per topik\n"
        "🎤 Pesan suara — Analisis grammar & koreksi otomatis\n\n"
        "*Belajar Percakapan Bebas:*\n"
        "• Kirim kalimat Inggris → aku bahas\n"
        "• Kirim kalimat Indonesia → aku terjemahkan & ajari\n"
        "• Kirim bebas → aku yang buat materinya\n\n"
        "*Shortcut jawaban:*\n"
        "`1` → Ulangi materi\n"
        "`2` → Latihan lagi\n"
        "`3` → Naik level / materi baru\n\n"
        "*Perintah lain:*\n"
        "/latihan — Mulai soal grammar\n"
        "/stop — Hentikan sesi aktif\n"
        "/reset — Reset sesi dari awal\n"
        "/start — Kembali ke menu utama\n\n"
        "_Santai aja, belajarnya pelan-pelan bareng aku!_ 😊",
        parse_mode="Markdown",
    )


# ─── /assessment ─────────────────────────────────────────────────────────────

async def assessment_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    text = start_assessment(user_id)
    await update.message.reply_text(text, parse_mode="Markdown")


# ─── /roleplay ───────────────────────────────────────────────────────────────

async def roleplay_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    text = start_roleplay(user_id)
    await update.message.reply_text(text, parse_mode="Markdown")


# ─── /grammar ────────────────────────────────────────────────────────────────

async def grammar_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    args = context.args

    if args and args[0].lower() == "menu":
        await update.message.reply_text(get_grammar_menu(), parse_mode="Markdown")
        return

    # Continue from last topic or start from topic 1
    text = start_grammar(user_id)
    await update.message.reply_text(text, parse_mode="Markdown")


# ─── /latihan ────────────────────────────────────────────────────────────────

async def latihan_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    text = show_grammar_exercise(user_id)
    if text:
        await update.message.reply_text(text, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            "Kamu belum buka topik grammar. Ketik /grammar dulu ya!",
        )


# ─── /vocab ──────────────────────────────────────────────────────────────────

async def vocab_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    text = start_vocab_session(user_id)
    await update.message.reply_text(text, parse_mode="Markdown")


# ─── /stop ───────────────────────────────────────────────────────────────────

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    msgs = []

    if is_in_assessment(user_id):
        cancel_assessment(user_id)
        msgs.append("Sesi assessment dihentikan.")
    if is_in_roleplay(user_id):
        msgs.append(cancel_roleplay(user_id))
    if is_in_grammar(user_id):
        cancel_grammar(user_id)
        msgs.append("Sesi grammar dihentikan.")
    if is_in_vocab_session(user_id) or is_waiting_category(user_id):
        msgs.append(cancel_vocab_session(user_id))

    if msgs:
        await update.message.reply_text("\n".join(msgs))
    else:
        await update.message.reply_text(
            "Tidak ada sesi aktif yang berjalan.\nKetik /menu untuk lihat pilihan belajar."
        )


# ─── /reset ──────────────────────────────────────────────────────────────────

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    cancel_assessment(user_id)
    cancel_roleplay(user_id)
    cancel_grammar(user_id)
    cancel_vocab_session(user_id)
    reset_profile(user_id)
    if user_id in user_context:
        del user_context[user_id]
    await update.message.reply_text(
        "Semua sesi dan profil kamu sudah di-reset!\n"
        "Ketik /start untuk mulai dari awal."
    )


# ─── Voice message handler ────────────────────────────────────────────────────

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    level = get_level(user_id)

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )
    await update.message.reply_text(
        "🎤 Aku lagi analisis suaramu... sebentar ya!"
    )

    transcription, feedback = await transcribe_and_analyze(
        voice_message=update.message.voice,
        bot=context.bot,
        ai_call_fn=call_ai,
        user_level=level,
    )

    if transcription:
        await update.message.reply_text(feedback, parse_mode="Markdown")
    else:
        await update.message.reply_text(feedback)


# ─── Text message handler ─────────────────────────────────────────────────────

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_input = update.message.text.strip()

    # ── 1. Assessment session ──
    if is_in_assessment(user_id):
        response, is_done, level = handle_assessment_answer(user_id, user_input)
        if is_done and level:
            set_level(user_id, level)
        await update.message.reply_text(response, parse_mode="Markdown")
        return

    # ── 2. Role-play: choosing scenario ──
    if is_choosing_scenario(user_id):
        response, ok, scenario_prompt = handle_scenario_choice(user_id, user_input)
        await update.message.reply_text(response, parse_mode="Markdown")
        return

    # ── 3. Role-play: active session ──
    if is_in_roleplay(user_id):
        scenario_prompt = get_active_scenario_prompt(user_id)
        count = increment_exchange(user_id)

        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )

        if is_session_ending(user_id):
            ending_prompt = (
                scenario_prompt + "\n\nThis is the final exchange. "
                "Wrap up the scenario naturally, then give a paragraph of "
                "feedback in Indonesian about the user's English performance "
                "(grammar, vocabulary, confidence). Be encouraging!"
            )
            response = call_ai("gemini", ending_prompt, user_input)
            cancel_roleplay(user_id)
        else:
            response = call_ai("gemini", scenario_prompt, user_input)

        if len(response) > 4000:
            for i in range(0, len(response), 4000):
                await update.message.reply_text(response[i : i + 4000])
        else:
            await update.message.reply_text(response)
        return

    # ── 4. Grammar: choosing topic ──
    if is_choosing_grammar(user_id):
        response, ok = handle_grammar_choice(user_id, user_input)
        await update.message.reply_text(response, parse_mode="Markdown")
        return

    # ── 5. Grammar: answering exercise ──
    if is_in_grammar(user_id):
        result = handle_grammar_answer(user_id, user_input)
        if result:
            response, _ = result
            await update.message.reply_text(response, parse_mode="Markdown")
            return

    # ── 6. Vocab: waiting for category ──
    if is_waiting_category(user_id):
        response, ok = handle_category_choice(user_id, user_input)
        await update.message.reply_text(response, parse_mode="Markdown")
        return

    # ── 7. Vocab: answering flashcard ──
    if is_in_vocab_session(user_id):
        response, ok = handle_vocab_answer(user_id, user_input)
        if response:
            await update.message.reply_text(response, parse_mode="Markdown")
            return

    # ── 8. Normal conversation mode ──
    ctx = await get_or_create_context(user_id)
    level = get_level(user_id)

    if user_input in ["1", "2", "3"]:
        options_map = {
            "1": "Ulangi materi sebelumnya dong, masih kurang paham.",
            "2": "Boleh kasih aku latihan lagi dengan topik yang sama?",
            "3": "Gas naik level! Atau kasih materi baru.",
        }
        user_input = options_map[user_input]
        ctx["state"] = "STATE 1 (LEARNING MODE)"

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    try:
        response = generate_ai_response(
            user_input, ctx["state"], ctx["history"], user_level=level
        )
    except Exception as e:
        response = f"Duh, servernya lagi error nih ({str(e)[:50]}). Coba sebentar lagi ya."
        logger.error(f"AI handler error: {e}")

    ctx["history"].append({"user": user_input, "bot": response})

    if ctx["state"] == "STATE 1 (LEARNING MODE)":
        ctx["state"] = "STATE 2 (ANSWER MODE)"

    if len(response) > 4000:
        for i in range(0, len(response), 4000):
            await update.message.reply_text(response[i : i + 4000])
    else:
        await update.message.reply_text(response)


# ─── Bot setup ─────────────────────────────────────────────────────────────────

async def post_init(application: Application) -> None:
    commands = [
        BotCommand("start", "Mulai / kembali ke menu utama"),
        BotCommand("assessment", "Tes penempatan level (10 soal)"),
        BotCommand("roleplay", "Simulasi percakapan nyata dengan AI"),
        BotCommand("grammar", "Grammar Coach — belajar tata bahasa"),
        BotCommand("latihan", "Mulai soal latihan grammar"),
        BotCommand("vocab", "Flashcard kosakata per topik"),
        BotCommand("menu", "Lihat panduan lengkap"),
        BotCommand("stop", "Hentikan sesi aktif"),
        BotCommand("reset", "Reset semua sesi & profil"),
    ]
    await application.bot.set_my_commands(commands)
    logger.info("Bot commands registered.")


def main() -> None:
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logger.error("TELEGRAM_TOKEN tidak ditemukan. Bot tidak bisa dijalankan.")
        return

    keep_alive()

    application = (
        Application.builder().token(token).post_init(post_init).build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("assessment", assessment_command))
    application.add_handler(CommandHandler("roleplay", roleplay_command))
    application.add_handler(CommandHandler("grammar", grammar_command))
    application.add_handler(CommandHandler("latihan", latihan_command))
    application.add_handler(CommandHandler("vocab", vocab_command))
    application.add_handler(CommandHandler("stop", stop_command))
    application.add_handler(CommandHandler("reset", reset))

    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    logger.info("Bot English Mas/Mbak berjalan...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
