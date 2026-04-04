import os
import logging
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from ai_handler import generate_ai_response
from vocab_handler import (
    is_in_vocab_session, is_waiting_category,
    start_vocab_session, handle_category_choice,
    handle_vocab_answer, cancel_vocab_session
)
from keep_alive import keep_alive

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Conversation state per user
# Structure: {user_id: {"state": str, "history": list}}
user_context = {}

async def get_or_create_context(user_id):
    if user_id not in user_context:
        user_context[user_id] = {"state": "STATE 1 (LEARNING MODE)", "history": []}
    return user_context[user_id]

# ─── Commands ───────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    ctx = await get_or_create_context(user.id)
    ctx["state"] = "STATE 1 (LEARNING MODE)"
    ctx["history"] = []

    await update.message.reply_text(
        f"Halo {user.first_name}! 👋\n\n"
        "Aku *English Mas/Mbak*, tutor bahasa Inggrismu yang santai.\n\n"
        "Yuk kita belajar bareng! Kamu bisa:\n"
        "• Kirim kalimat bahasa Inggris yang mau dibahas\n"
        "• Kirim bahasa Indonesia yang mau di-Inggris-in\n"
        "• Atau langsung ketik aja, biar aku yang kasih materi\n\n"
        "Ketik /menu untuk lihat panduan lengkap.",
        parse_mode="Markdown"
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📚 *Panduan English Mas/Mbak*\n\n"
        "*Perintah tersedia:*\n"
        "/start — Mulai sesi belajar baru\n"
        "/menu — Tampilkan panduan ini\n"
        "/vocab — Latihan kosakata dengan flashcard\n"
        "/stop — Hentikan sesi flashcard\n"
        "/reset — Reset sesi dari awal\n\n"
        "*Cara belajar biasa:*\n"
        "1️⃣ Kirim kata/kalimat bahasa Inggris → aku bahas\n"
        "2️⃣ Kirim kalimat bahasa Indonesia → aku terjemahkan & ajari\n"
        "3️⃣ Kirim pesan bebas → aku yang tentuin materinya\n\n"
        "*Setelah dapat materi, balas:*\n"
        "`1` → Ulangi materi\n"
        "`2` → Latihan lagi\n"
        "`3` → Naik level / materi baru\n\n"
        "*Flashcard Vocab (/vocab):*\n"
        "🃏 Pilih topik → jawab arti kata → lihat skor!\n"
        "Topik: makanan, warna, keluarga, hewan, tubuh, emosi, aktivitas\n\n"
        "_Santai aja, belajarnya pelan-pelan bareng aku!_ 😊",
        parse_mode="Markdown"
    )

async def vocab_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    text = start_vocab_session(user_id)
    await update.message.reply_text(text, parse_mode="Markdown")

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    text = cancel_vocab_session(user_id)
    await update.message.reply_text(text)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    cancel_vocab_session(user_id)
    if user_id in user_context:
        del user_context[user_id]
    await update.message.reply_text(
        "Sesi belajarmu sudah di-reset! Yuk mulai dari awal lagi.\n"
        "Ketik /start untuk mulai sesi baru."
    )

# ─── Message handler ─────────────────────────────────────────────────────────

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_input = update.message.text.strip()

    # ── Flashcard: waiting for category choice ──
    if is_waiting_category(user_id):
        response, ok = handle_category_choice(user_id, user_input)
        await update.message.reply_text(response, parse_mode="Markdown")
        return

    # ── Flashcard: waiting for vocab answer ──
    if is_in_vocab_session(user_id):
        response, ok = handle_vocab_answer(user_id, user_input)
        if response:
            await update.message.reply_text(response, parse_mode="Markdown")
            return

    # ── Normal conversation mode ──
    ctx = await get_or_create_context(user_id)

    # Map shortcut replies 1/2/3 to readable prompts
    if user_input in ['1', '2', '3']:
        options_map = {
            '1': "Ulangi materi sebelumnya dong, masih kurang paham.",
            '2': "Boleh kasih aku latihan lagi dengan topik yang sama?",
            '3': "Gas naik level! Atau kasih materi baru."
        }
        user_input = options_map[user_input]
        ctx["state"] = "STATE 1 (LEARNING MODE)"

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')

    try:
        response = generate_ai_response(user_input, ctx["state"], ctx["history"])
    except Exception as e:
        response = f"Duh, servernya lagi error nih ({str(e)}). Coba sebentar lagi ya."
        logger.error(f"AI handler error: {e}")

    ctx["history"].append({"user": user_input, "bot": response})

    if ctx["state"] == "STATE 1 (LEARNING MODE)":
        ctx["state"] = "STATE 2 (ANSWER MODE)"

    # Send (handle Telegram's 4096-char limit)
    if len(response) > 4000:
        for i in range(0, len(response), 4000):
            await update.message.reply_text(response[i:i+4000])
    else:
        await update.message.reply_text(response)

# ─── Bot setup ────────────────────────────────────────────────────────────────

async def post_init(application: Application) -> None:
    commands = [
        BotCommand("start", "Mulai sesi belajar baru"),
        BotCommand("menu", "Lihat panduan lengkap"),
        BotCommand("vocab", "Latihan kosakata dengan flashcard"),
        BotCommand("stop", "Hentikan sesi flashcard"),
        BotCommand("reset", "Reset sesi dari awal"),
    ]
    await application.bot.set_my_commands(commands)
    logger.info("Bot commands registered.")

def main() -> None:
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logger.error("TELEGRAM_TOKEN tidak ditemukan. Bot tidak bisa dijalankan.")
        return

    keep_alive()  # Start health check server for UptimeRobot

    application = (
        Application.builder()
        .token(token)
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("vocab", vocab_command))
    application.add_handler(CommandHandler("stop", stop_command))
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot English Mas/Mbak berjalan...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
