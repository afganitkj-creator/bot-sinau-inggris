
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
    start_grammar, start_grammar_menu,
    is_in_grammar, is_choosing_grammar,
    handle_grammar_choice, show_grammar_exercise,
    handle_grammar_answer, cancel_grammar,
)
from stories_handler import (
    start_story_menu, is_in_story, is_choosing_story,
    handle_story_choice, handle_story_input, cancel_story,
)
from voice_handler import transcribe_and_analyze
from gamification import (
    add_xp, xp_notification, check_and_update_streak,
    get_xp_bar, hearts_display, lose_heart, get_hearts,
    refill_time_str, format_weekly_challenge, increment_weekly_stat,
)
from leaderboard import format_leaderboard, update_leaderboard
from user_profile import (
    get_level, set_level, get_level_label,
    is_assessment_done, reset_profile, is_premium, set_premium,
)
from keep_alive import keep_alive

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

user_context = {}


# ─── Helpers ─────────────────────────────────────────────────────────────────

def cancel_all_sessions(user_id):
    cancel_assessment(user_id)
    cancel_roleplay(user_id)
    cancel_grammar(user_id)
    cancel_vocab_session(user_id)
    cancel_story(user_id)


async def get_or_create_context(user_id):
    if user_id not in user_context:
        user_context[user_id] = {"state": "STATE 1 (LEARNING MODE)", "history": []}
    return user_context[user_id]


async def safe_reply(update, text, parse_mode="Markdown"):
    try:
        await update.message.reply_text(text, parse_mode=parse_mode)
    except Exception:
        try:
            await update.message.reply_text(text)
        except Exception as e:
            logger.error(f"Failed to send message: {e}")


def get_display_name(user):
    return user.first_name or user.username or f"User{user.id}"


async def send_streak_notification(update, streak, bonus_xp, leveled_up, level_name):
    msg = f"🔥 *Streak {streak} hari!* +{bonus_xp} XP bonus"
    if leveled_up:
        msg += f"\n🎉 *Level Up! → {level_name}*"
    await safe_reply(update, msg)


# ─── /start ──────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    cancel_all_sessions(user.id)
    ctx = await get_or_create_context(user.id)
    ctx["state"] = "STATE 1 (LEARNING MODE)"
    ctx["history"] = []

    name = get_display_name(user)
    xp = (lambda p: p.get("xp", 0))(__import__("user_profile").get_profile(user.id))
    xp_bar = get_xp_bar(xp)

    if is_assessment_done(user.id):
        level_info = f"Level bahasa: *{get_level_label(user.id)}*\n{xp_bar}\n\n"
    else:
        level_info = "💡 Ketik /assessment dulu untuk tes level kamu!\n\n"

    await safe_reply(update,
        f"Halo {name}! 👋\n\n"
        "Aku *English Mas/Mbak* — tutor bahasa Inggrismu yang santai.\n\n"
        f"{level_info}"
        "Yang bisa kamu lakuin:\n"
        "🎯 /assessment — Tes penempatan level\n"
        "💬 /roleplay — Simulasi percakapan nyata\n"
        "📚 /grammar — Grammar Coach\n"
        "📖 /story — Baca cerita interaktif\n"
        "🃏 /vocab — Flashcard kosakata\n"
        "🎤 Kirim pesan suara — Aku analisis grammar-mu!\n\n"
        "👤 /profil — Lihat statistik & perkembangan\n"
        "🏆 /leaderboard — Papan peringkat\n"
        "Ketik /menu untuk panduan lengkap."
    )


# ─── /menu ───────────────────────────────────────────────────────────────────

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    level_label = get_level_label(user_id)
    await safe_reply(update,
        f"📚 *Panduan English Mas/Mbak*\n"
        f"Level: *{level_label}* | /profil untuk detail\n\n"
        "*🎓 Belajar:*\n"
        "🎯 /assessment — Tes penempatan level (10 soal)\n"
        "💬 /roleplay — Role-play AI: wawancara, restoran, dll\n"
        "📚 /grammar — Grammar Coach (10 topik)\n"
        "📖 /story — Cerita interaktif (5 cerita)\n"
        "🃏 /vocab — Flashcard kosakata\n"
        "🎤 Pesan suara — Analisis grammar otomatis\n\n"
        "*🏆 Gamifikasi:*\n"
        "👤 /profil — XP, level, streak, hati\n"
        "🏆 /leaderboard — Top learners\n"
        "💎 /premium — Fitur premium\n\n"
        "*Percakapan Bebas:*\n"
        "• Kirim kalimat Inggris → aku bahas\n"
        "• Kirim kalimat Indonesia → aku terjemahkan\n"
        "• Kirim bebas → aku buat materi\n\n"
        "*Shortcut:* `1` Ulangi · `2` Latihan · `3` Naik level\n\n"
        "*/grammar menu* — Pilih topik grammar\n"
        "*/stop* — Hentikan sesi aktif\n"
        "*/reset* — Reset semua\n\n"
        "_Santai aja, belajarnya pelan-pelan bareng aku!_ 😊"
    )


# ─── /profil ─────────────────────────────────────────────────────────────────

async def profil_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = user.id
    name = get_display_name(user)

    import user_profile as up
    profile = up.get_profile(user_id)
    xp = profile.get("xp", 0)
    streak = profile.get("streak", 0)

    xp_bar = get_xp_bar(xp)
    hearts = hearts_display(user_id)
    rank_line = ""
    from leaderboard import get_user_rank
    rank = get_user_rank(user_id)
    if rank:
        rank_line = f"🏆 Ranking: *#{rank}*\n"

    level_label = get_level_label(user_id)
    assessment_status = "✅ Selesai" if is_assessment_done(user_id) else "❌ Belum (ketik /assessment)"
    premium_badge = "💎 *PREMIUM*" if is_premium(user_id) else "Standar (ketik /premium)"

    weekly = format_weekly_challenge(user_id)

    await safe_reply(update,
        f"👤 *Profil — {name}*\n\n"
        f"📊 Level bahasa: *{level_label}*\n"
        f"Assessment: {assessment_status}\n\n"
        f"🎮 *Level XP:*\n{xp_bar}\n\n"
        f"🔥 Streak: *{streak} hari* berturut-turut\n"
        f"{rank_line}"
        f"Akun: {premium_badge}\n\n"
        f"❤️ Hati: {hearts}\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📅 *Tantangan Minggu Ini:*\n{weekly}\n\n"
        f"Ketik /leaderboard untuk lihat papan peringkat!"
    )


# ─── /leaderboard ─────────────────────────────────────────────────────────────

async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    text = format_leaderboard(user_id)
    await safe_reply(update, text)


# ─── /premium ─────────────────────────────────────────────────────────────────

async def premium_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if is_premium(user_id):
        await safe_reply(update,
            "💎 *Kamu sudah Premium!*\n\n"
            "✅ Hati tak terbatas (unlimited hearts)\n"
            "✅ Prioritas akses fitur baru\n"
            "✅ Badge Premium di profil\n\n"
            "Terima kasih sudah mendukung bot ini! 🙏"
        )
        return

    await safe_reply(update,
        "💎 *Super English Mas/Mbak*\n\n"
        "*Fitur Premium:*\n"
        "❤️ Hati tak terbatas — belajar tanpa batas salah\n"
        "⚡ Akses prioritas semua fitur\n"
        "🏅 Badge Premium di leaderboard\n"
        "📊 Statistik belajar detail\n"
        "🎯 Kurikulum personalisasi lebih dalam\n\n"
        "*Cara mendapatkan Premium:*\n"
        "Hubungi admin bot ini untuk informasi lebih lanjut.\n\n"
        "_Bot ini gratis sepenuhnya untuk semua pengguna. Premium mendukung pengembangan bot!_ 🙏"
    )


# ─── /assessment ─────────────────────────────────────────────────────────────

async def assessment_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    cancel_roleplay(user_id)
    cancel_grammar(user_id)
    cancel_vocab_session(user_id)
    cancel_story(user_id)
    text = start_assessment(user_id)
    await safe_reply(update, text)


# ─── /roleplay ───────────────────────────────────────────────────────────────

async def roleplay_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    cancel_assessment(user_id)
    cancel_grammar(user_id)
    cancel_vocab_session(user_id)
    cancel_story(user_id)
    text = start_roleplay(user_id)
    await safe_reply(update, text)


# ─── /grammar ────────────────────────────────────────────────────────────────

async def grammar_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    cancel_assessment(user_id)
    cancel_roleplay(user_id)
    cancel_vocab_session(user_id)
    cancel_story(user_id)

    args = context.args
    if args and args[0].lower() == "menu":
        text = start_grammar_menu(user_id)
    else:
        text = start_grammar(user_id)
    await safe_reply(update, text)


# ─── /latihan ────────────────────────────────────────────────────────────────

async def latihan_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    text = show_grammar_exercise(user_id)
    if text:
        await safe_reply(update, text)
    else:
        await update.message.reply_text(
            "Kamu belum buka topik grammar.\n"
            "Ketik /grammar untuk mulai, atau /grammar menu untuk pilih topik."
        )


# ─── /story ──────────────────────────────────────────────────────────────────

async def story_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    cancel_assessment(user_id)
    cancel_roleplay(user_id)
    cancel_grammar(user_id)
    cancel_vocab_session(user_id)
    text = start_story_menu(user_id)
    await safe_reply(update, text)


# ─── /vocab ──────────────────────────────────────────────────────────────────

async def vocab_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    cancel_assessment(user_id)
    cancel_roleplay(user_id)
    cancel_grammar(user_id)
    cancel_story(user_id)
    text = start_vocab_session(user_id)
    await safe_reply(update, text)


# ─── /stop ───────────────────────────────────────────────────────────────────

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    msgs = []
    if is_in_assessment(user_id):
        cancel_assessment(user_id); msgs.append("Sesi assessment dihentikan.")
    if is_in_roleplay(user_id) or is_choosing_scenario(user_id):
        msgs.append(cancel_roleplay(user_id))
    if is_in_grammar(user_id) or is_choosing_grammar(user_id):
        cancel_grammar(user_id); msgs.append("Sesi grammar dihentikan.")
    if is_in_vocab_session(user_id) or is_waiting_category(user_id):
        msgs.append(cancel_vocab_session(user_id))
    if is_in_story(user_id) or is_choosing_story(user_id):
        cancel_story(user_id); msgs.append("Sesi cerita dihentikan.")

    if msgs:
        await update.message.reply_text("\n".join(msgs))
    else:
        await update.message.reply_text(
            "Tidak ada sesi aktif.\nKetik /menu untuk lihat pilihan belajar."
        )


# ─── /reset ──────────────────────────────────────────────────────────────────

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    cancel_all_sessions(user_id)
    reset_profile(user_id)
    if user_id in user_context:
        del user_context[user_id]
    await update.message.reply_text(
        "Semua sesi dan profil kamu sudah di-reset!\n"
        "Ketik /start untuk mulai dari awal."
    )


# ─── Voice handler ────────────────────────────────────────────────────────────

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    level = get_level(user_id)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await update.message.reply_text("🎤 Aku lagi analisis suaramu... sebentar ya!")

    _, feedback = await transcribe_and_analyze(
        voice_message=update.message.voice,
        bot=context.bot,
        ai_call_fn=call_ai,
        user_level=level,
    )
    await safe_reply(update, feedback)


# ─── Main message handler ─────────────────────────────────────────────────────

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = user.id
    user_input = update.message.text.strip()
    name = get_display_name(user)

    # ── Daily streak check (once per day) ──
    streak, is_new_day, bonus_xp, lvl_up, lvl_name = check_and_update_streak(user_id, name)
    if is_new_day and streak >= 2:
        await send_streak_notification(update, streak, bonus_xp, lvl_up, lvl_name)

    # ── 1. Assessment ──────────────────────────────────────────────────────────
    if is_in_assessment(user_id):
        response, is_done, level = handle_assessment_answer(user_id, user_input)
        if is_done and level:
            set_level(user_id, level)
            xp_got, new_xp, lu, ln = add_xp(user_id, "assessment_complete", name)
            response += xp_notification(xp_got, new_xp, lu, ln)
        await safe_reply(update, response)
        return

    # ── 2. Story: choosing ────────────────────────────────────────────────────
    if is_choosing_story(user_id):
        response, ok = handle_story_choice(user_id, user_input)
        await safe_reply(update, response)
        return

    # ── 3. Story: active ─────────────────────────────────────────────────────
    if is_in_story(user_id):
        response, xp_from_story = handle_story_input(user_id, user_input)
        if response is None:
            pass
        else:
            if xp_from_story > 0:
                import user_profile as up
                up.get_profile(user_id)["xp"] = up.get_profile(user_id).get("xp", 0) + xp_from_story
                update_leaderboard(user_id, up.get_profile(user_id)["xp"], name)
                # Track weekly stats
                if "Selesai" in response or "Cerita Selesai" in response:
                    increment_weekly_stat(user_id, "stories_read")
            await safe_reply(update, response)
        return

    # ── 4. Role-play: choosing scenario ──────────────────────────────────────
    if is_choosing_scenario(user_id):
        response, ok, _ = handle_scenario_choice(user_id, user_input)
        await safe_reply(update, response)
        return

    # ── 5. Role-play: active ──────────────────────────────────────────────────
    if is_in_roleplay(user_id):
        scenario_prompt = get_active_scenario_prompt(user_id)
        count = increment_exchange(user_id)
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

        xp_got, new_xp, lu, ln = add_xp(user_id, "roleplay_exchange", name)

        if is_session_ending(user_id):
            ending_prompt = (
                scenario_prompt
                + "\n\nThis is the final exchange. Wrap up naturally (1-2 sentences), "
                "then give a short paragraph in Indonesian about the user's English "
                "(grammar, vocabulary, fluency). Be encouraging! Suggest /roleplay to try another."
            )
            response = call_ai("gemini", ending_prompt, user_input)
            cancel_roleplay(user_id)
            increment_weekly_stat(user_id, "roleplay_sessions")
            response += xp_notification(xp_got, new_xp, lu, ln)
        else:
            response = call_ai("gemini", scenario_prompt, user_input)

        await safe_reply(update, response, parse_mode=None)
        return

    # ── 6. Grammar: choosing topic ────────────────────────────────────────────
    if is_choosing_grammar(user_id):
        response, ok = handle_grammar_choice(user_id, user_input)
        await safe_reply(update, response)
        return

    # ── 7. Grammar: exercise ──────────────────────────────────────────────────
    if is_in_grammar(user_id):
        result = handle_grammar_answer(user_id, user_input)
        if result:
            response, is_correct = result
            if is_correct:
                xp_got, new_xp, lu, ln = add_xp(user_id, "grammar_correct", name)
                response += xp_notification(xp_got, new_xp, lu, ln)
                increment_weekly_stat(user_id, "grammar_done")
            else:
                remaining = lose_heart(user_id)
                heart_warn = ""
                if remaining <= 1 and not is_premium(user_id):
                    refill = refill_time_str(user_id)
                    if remaining == 0:
                        heart_warn = f"\n\n🖤 Hati habis! Refill dalam ~{refill}. Ketik /premium untuk hati tak terbatas."
                    else:
                        heart_warn = f"\n\n❤️ Hati tersisa: {remaining}. Tetap semangat!"
                response += heart_warn
            await safe_reply(update, response)
            return

    # ── 8. Vocab: choosing category ───────────────────────────────────────────
    if is_waiting_category(user_id):
        response, ok = handle_category_choice(user_id, user_input)
        await safe_reply(update, response)
        return

    # ── 9. Vocab: answering flashcard ─────────────────────────────────────────
    if is_in_vocab_session(user_id):
        response, is_correct = handle_vocab_answer(user_id, user_input)
        if response:
            if is_correct:
                xp_got, new_xp, lu, ln = add_xp(user_id, "vocab_correct", name)
                response += xp_notification(xp_got, new_xp, lu, ln)
                increment_weekly_stat(user_id, "vocab_answers")
            else:
                lose_heart(user_id)
                increment_weekly_stat(user_id, "vocab_answers")
            await safe_reply(update, response)
            return

    # ── 10. Normal conversation ───────────────────────────────────────────────
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

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        response = generate_ai_response(
            user_input, ctx["state"], ctx["history"], user_level=level
        )
    except Exception as e:
        response = "Duh, servernya lagi error nih. Coba sebentar lagi ya."
        logger.error(f"AI error: {e}")

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
        BotCommand("grammar", "Grammar Coach — 10 topik tata bahasa"),
        BotCommand("latihan", "Mulai soal latihan grammar"),
        BotCommand("story", "Cerita interaktif + soal pemahaman"),
        BotCommand("vocab", "Flashcard kosakata per topik"),
        BotCommand("profil", "Lihat XP, level, streak, dan hati"),
        BotCommand("leaderboard", "Papan peringkat top learners"),
        BotCommand("premium", "Info fitur premium"),
        BotCommand("menu", "Panduan lengkap semua fitur"),
        BotCommand("stop", "Hentikan sesi aktif"),
        BotCommand("reset", "Reset semua sesi dan profil"),
    ]
    await application.bot.set_my_commands(commands)
    logger.info("Bot commands registered.")


def main() -> None:
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logger.error("TELEGRAM_TOKEN tidak ditemukan.")
        return

    keep_alive()

    application = (
        Application.builder().token(token).post_init(post_init).build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("profil", profil_command))
    application.add_handler(CommandHandler("profile", profil_command))
    application.add_handler(CommandHandler("leaderboard", leaderboard_command))
    application.add_handler(CommandHandler("premium", premium_command))
    application.add_handler(CommandHandler("assessment", assessment_command))
    application.add_handler(CommandHandler("roleplay", roleplay_command))
    application.add_handler(CommandHandler("grammar", grammar_command))
    application.add_handler(CommandHandler("latihan", latihan_command))
    application.add_handler(CommandHandler("story", story_command))
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
