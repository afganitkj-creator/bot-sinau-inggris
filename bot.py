import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

from ai_handler import generate_ai_response

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Simple in-memory dict for user states and history
# Cocok untuk versi 1 (RAM memory)
# Struktur: user_context[user_id] = {"state": "STATE 1", "history": []}
user_context = {}

async def get_or_create_context(user_id):
    if user_id not in user_context:
        user_context[user_id] = {"state": "STATE 1 (LEARNING MODE)", "history": []}
    return user_context[user_id]

async def post_init(application: Application):
    commands = [
        ("start", "Mulai sesi belajar baru"),
        ("menu", "Tampilkan panduan ini"),
        ("reset", "Hapus riwayat memori (mulai level 1)")
    ]
    await application.bot.set_my_commands(commands)
    logger.info("Bot commands (menu button) updated successfully!")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = user.id
    ctx = await get_or_create_context(user_id)
    ctx["state"] = "STATE 1 (LEARNING MODE)"
    ctx["history"] = []
    
    welcome_message = (
        f"Halo {user.first_name}! 👋\n\n"
        "Aku English Mas/Mbak, tutor bahasa Inggrismu yang santai.\n"
        "Yuk kita belajar bareng! Kamu bisa kirim kalimat bahasa Inggris yang mau dibahas, "
        "bahasa Indonesia yang mau di-Inggris-in, atau cukup sapa aja biar aku yang kasih materi."
    )
    await update.message.reply_text(welcome_message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_input = update.message.text
    
    ctx = await get_or_create_context(user_id)
    
    # Handle auto-menu input "1", "2", "3"
    if user_input.strip() in ['1', '2', '3']:
        options_map = {
            '1': "Ulangi materi sebelumnya dong, masih kurang paham.",
            '2': "Boleh kasih aku latihan lagi dengan topik yang sama?",
            '3': "Gas naik level! Atau kasih materi baru."
        }
        user_input = options_map[user_input.strip()]
        # Reset state logic to ask material again
        ctx["state"] = "STATE 1 (LEARNING MODE)"
    else:
        # Basic state switching based on length/context (This is a naive transition for V1)
        # Assuming if they are not picking a menu, and they are in Answer Mode, leave them in Answer Mode
        # The AI itself is the smartest judge, but we force the state into the prompt.
        pass

    # Provide typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    try:
        response = generate_ai_response(user_input, ctx["state"], ctx["history"])
    except Exception as e:
        response = f"Duh, servernya lagi error nih ({str(e)}). Coba sebentar lagi ya."
        logger.error(f"Error calling AI handler: {e}")
    
    # Save to history
    ctx["history"].append({"user": user_input, "bot": response})
    
    # Simple state transition toggler:
    # After AI sends an explanation and an exercise (STATE 1), 
    # the user's next turn is basically answering (STATE 2).
    # Then after AI scores it (STATE 2), it gives 1.2.3 options. 
    # If user replies with 1,2,3 we already set it loop back to STATE 1 above.
    if ctx["state"] == "STATE 1 (LEARNING MODE)":
        ctx["state"] = "STATE 2 (ANSWER MODE)"
        
    # Send message back (handle long message)
    if len(response) > 4000:
        # Telegram max msg is 4096
        for i in range(0, len(response), 4000):
            await update.message.reply_text(response[i:i+4000])
    else:
        await update.message.reply_text(response)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id in user_context:
        del user_context[user_id]
    await update.message.reply_text("Sesi belajarmu sudah di-reset dari awal ya! Yuk kita mulai dari level 1 lagi.")

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    menu_text = (
        "📚 *Menu English Mas/Mbak*\n\n"
        "Gunakan perintah berikut ya:\n"
        "/start - Mulai sesi belajar baru\n"
        "/menu - Menampilkan menu ini\n"
        "/reset - Hapus ingatan percakapan (refresh)\n\n"
        "💡 *Tips Belajar:*\n"
        "1. Ketik kalimat bahasa Indonesia/Inggris apa saja.\n"
        "2. Setelah latihan selesai, balas dengan angka:\n"
        "   *1* -> Ulangi materi tadi dong\n"
        "   *2* -> Minta kalimat latihan lagi\n"
        "   *3* -> Gas materi/topik baru!"
    )
    await update.message.reply_text(menu_text, parse_mode="Markdown")

def main() -> None:
    token = os.getenv("TELEGRAM_TOKEN")
    if not token or token == "your_telegram_bot_token_here":
        logger.error("Token Telegram belum disetting di file .env. Bot tidak bisa dijalankan.")
        return

    # Build bot application
    application = Application.builder().token(token).post_init(post_init).build()

    # Commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(CommandHandler("menu", menu_command))
    
    # Messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    from keep_alive import keep_alive
    keep_alive()

    logger.info("Mantul, bot English Mas/Mbak berjalan...")
    
    # Polling mode (runs until manually stopped)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
