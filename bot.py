# Updated bot.py to add support developer feature

# 1. Importing support_handler functions
from support_handler import (
    start_support_session, handle_support_choice,
    confirm_support, get_tier_info, end_support_session, 
    get_premium_benefits_text, is_in_support_session, get_support_session_state
)

# ... existing imports here

# 2. Updating user_profile import
from user_profile import (
    get_level, set_level, get_level_label,
    is_assessment_done, reset_profile, is_premium, set_premium,
    set_premium_duration, get_premium_remaining_days, check_premium_expired, get_premium_status_text,
)

# ... existing code here 

# 3. Adding the support command
async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    text = start_support_session(user_id)
    await safe_reply(update, text)

# ... existing code here

# 4. Updating the menu command
# "💎 /premium — Fitur premium\n"
# "💖 /support — Support developer dengan QRIS!\n\n"

# ... existing code here

# 5. Adding support handler in handle_message function
    # ── 10. Support Developer (Donasi/Premium) ────────────────────────────────
    if is_in_support_session(user_id):
        from support_handler import support_sessions
        session = support_sessions.get(user_id, {})
        state = get_support_session_state(user_id)
        
        if state == "viewing_menu":
            response, ok = handle_support_choice(user_id, user_input)
            if ok:
                tier = get_tier_info(user_id)
                response += "\n\n" + get_premium_benefits_text(session.get("tier_index", 0))
            await safe_reply(update, response)
            return
        
        elif state == "awaiting_payment":
            if user_input.lower() in ["batal", "cancel", "tidak", "tidak jadi"]:
                end_support_session(user_id)
                await safe_reply(update, 
                    "Support dibatalkan. Ketik /support untuk coba lagi atau /menu untuk kembali ke menu utama."
                )
            else:
                await safe_reply(update,
                    "Silakan lanjutkan pembayaran QRIS seperti yang ditampilkan di atas.\n\n"
                    "Setelah selesai, kirim screenshot bukti pembayaran untuk verifikasi.\n\n"
                    "Ketik 'batal' untuk membatalkan."
                )
            return

# 6. Adding support command to post_init function
BotCommand("support", "Support developer dengan QRIS - dapatkan Premium!"),

# 7. Adding handler in main() function
application.add_handler(CommandHandler("support", support_command))