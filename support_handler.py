"""Support Developer Handler - QRIS Payment Integration.
Untuk mendukung pengembangan bot dan memberikan akses Premium.
"""

QRIS_CONFIG = {
    "name": "brosnigan",
    "nmid": "ID1026501497097",
    "code": "A01",
    "url": "www.aspi-qris.id",
    "donation_tiers": [
        {"amount": 5000, "label": "Kopi", "days": 1, "description": "Support segelas kopi ☕"},
        {"amount": 10000, "label": "Makan Siang", "days": 3, "description": "Support makan siang 🍜"},
        {"amount": 25000, "label": "Mingguan", "days": 7, "description": "Support Premium 1 minggu 📅"},
        {"amount": 50000, "label": "Bulanan", "days": 30, "description": "Support Premium 1 bulan 💎"},
    ],
}

# Support session tracking
support_sessions = {}


def get_support_menu():
    """Menu utama Support Developer."""
    return (
        "💖 *Support Developer*\n\n"
        "Bantu kami mengembangkan bot dan dapatkan akses Premium sementara!\n\n"
        "*Dengan Support kamu akan mendapat:*\n"
        "✅ Akses Premium selama durasi support\n"
        "✅ Hati unlimited untuk belajar tanpa batas salah\n"
        "✅ Fitur baru setiap hari (ganti pertanyaan/tambah fitur)\n"
        "✅ Priority access ke fitur terbaru\n"
        "✅ Badge khusus di profil & leaderboard\n\n"
        "*Pilihan donasi:*\n"
        "1️⃣ Rp 5.000 — Support segelas kopi (1 hari) ☕\n"
        "2️⃣ Rp 10.000 — Support makan siang (3 hari) 🍜\n"
        "3️⃣ Rp 25.000 — Support mingguan (7 hari) 📅\n"
        "4️⃣ Rp 50.000 — Support bulanan (30 hari) 💎\n\n"
        "Balas dengan angka 1-4 untuk pilih jumlah donasi.\n"
        "_Terimakasih sudah support pengembangan bot ini!_ 🙏"
    )


def get_qris_payment_info(tier_index):
    """Dapatkan informasi pembayaran QRIS untuk tier tertentu."""
    if tier_index < 0 or tier_index >= len(QRIS_CONFIG["donation_tiers"]):
        return None, None

    tier = QRIS_CONFIG["donation_tiers"][tier_index]

    qris_text = (
        f"💖 *Terima kasih sudah Support!*\n\n"
        f"*Paket Donasi:* {tier['label']}\n"
        f"*Jumlah:* Rp {tier['amount']:,}\n"
        f"*Durasi Premium:* {tier['days']} hari\n"
        f"*Deskripsi:* {tier['description']}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"*📱 Silakan scan QR Code ini untuk pembayaran QRIS:*\n\n"
        f"*Nama Penerima:* {QRIS_CONFIG['name']}\n"
        f"*NMID:* {QRIS_CONFIG['nmid']}\n"
        f"*Kode:* {QRIS_CONFIG['code']}\n\n"
        f"_Cek aplikasi penyelenggara di: {QRIS_CONFIG['url']}_\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"*Petunjuk Pembayaran:*\n"
        f"1. 📲 Buka aplikasi e-wallet atau banking\n"
        f"2. 📷 Scan QR Code di atas\n"
        f"3. ✅ Konfirmasi pembayaran Rp {tier['amount']:,}\n"
        f"4. 💬 Balas dengan SS bukti pembayaran\n\n"
        f"Setelah verifikasi, akun kamu akan langsung jadi Premium! 🎉"
    )

    return tier, qris_text


def get_premium_benefits_text(tier_index):
    """Daftar manfaat premium yang akan diterima."""
    if tier_index < 0 or tier_index >= len(QRIS_CONFIG["donation_tiers"]):
        return None

    tier = QRIS_CONFIG["donation_tiers"][tier_index]

    return (
        f"💎 *Manfaat Premium {tier['label']} ({tier['days']} hari):*\n\n"
        f"✨ *Pembelajaran Tanpa Batas:*\n"
        f"❤️ Hati unlimited — Salah sebanyak yang kamu mau\n"
        f"🔄 Reset daily challenge setiap hari\n"
        f"📚 Akses semua fitur pembelajaran\n\n"
        f"🎯 *Fitur Eksklusif:*\n"
        f"⚡ Akses prioritas fitur baru\n"
        f"🎨 Personalisasi kurikulum lebih dalam\n"
        f"📊 Statistik pembelajaran detail\n"
        f"🏅 Badge Premium di leaderboard\n\n"
        f"🤖 *Fitur AI:*\n"
        f"💬 Role-play unlimited tanpa batasan\n"
        f"🎤 Analisis suara unlimited\n"
        f"📖 Cerita unlimited tanpa batasan\n"
        f"🃏 Flashcard unlimited\n\n"
        f"🎁 *Bonus Mingguan:*\n"
        f"🎰 Spin wheel bonus XP 2x sehari\n"
        f"🎯 Weekly challenge dengan hadiah ekstra\n"
        f"🌟 Monthly tier bonus\n\n"
        f"_Premium berlaku selama {tier['days']} hari!_ ⏰"
    )


def format_support_confirmation(tier_index, user_name):
    """Format pesan konfirmasi support."""
    if tier_index < 0 or tier_index >= len(QRIS_CONFIG["donation_tiers"]):
        return None

    tier = QRIS_CONFIG["donation_tiers"][tier_index]

    return (
        f"🎉 *Terima Kasih {user_name}!* 🎉\n\n"
        f"Kamu memilih: *{tier['label']}* (Rp {tier['amount']:,})\n"
        f"Durasi Premium: *{tier['days']} hari*\n\n"
        f"Silakan lanjutkan dengan pembayaran QRIS seperti yang sudah ditampilkan.\n\n"
        f"Setelah pembayaran berhasil, reply dengan screenshot bukti pembayaran untuk verifikasi cepat.\n\n"
        f"Pertanyaan? Hubungi admin! 👨‍💻"
    )


def start_support_session(user_id):
    """Mulai sesi support."""
    support_sessions[user_id] = {"state": "viewing_menu"}
    return get_support_menu()


def is_in_support_session(user_id):
    return user_id in support_sessions


def get_support_session_state(user_id):
    return support_sessions.get(user_id, {}).get("state")


def handle_support_choice(user_id, choice):
    """Handle pilihan tier donasi."""
    try:
        tier_index = int(choice) - 1
        if tier_index < 0 or tier_index >= len(QRIS_CONFIG["donation_tiers"]):
            return get_support_menu(), False

        support_sessions[user_id] = {
            "state": "awaiting_payment",
            "tier_index": tier_index,
        }

        _, qris_text = get_qris_payment_info(tier_index)
        return qris_text, True
    except (ValueError, TypeError):
        return get_support_menu(), False


def confirm_support(user_id, display_name):
    """Konfirmasi pilihan support."""
    if user_id not in support_sessions:
        return None

    session = support_sessions[user_id]
    if session.get("state") != "awaiting_payment":
        return None

    tier_index = session.get("tier_index", 0)
    return format_support_confirmation(tier_index, display_name)


def get_tier_info(user_id):
    """Ambil info tier yang dipilih."""
    if user_id not in support_sessions:
        return None

    tier_index = support_sessions[user_id].get("tier_index", 0)
    if tier_index < 0 or tier_index >= len(QRIS_CONFIG["donation_tiers"]):
        return None

    return QRIS_CONFIG["donation_tiers"][tier_index]


def end_support_session(user_id):
    """Akhiri sesi support."""
    support_sessions.pop(user_id, None)
