<div align="center">

# 🤖 English Mas/Mbak Bot

### Tutor Bahasa Inggris AI untuk Pemula Indonesia

*Belajar bahasa Inggris terasa susah? Aku hadir buat nemenin kamu — santai, sabar, dan seru!*

[![Telegram](https://img.shields.io/badge/Telegram-@sinau__inggris__bot-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/sinau_inggris_bot)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Gemini](https://img.shields.io/badge/Gemini_AI-Powered-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![OpenAI](https://img.shields.io/badge/OpenAI-Fallback-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

</div>

## ✨ Tentang Bot

**English Mas/Mbak** adalah bot Telegram berbasis AI yang dirancang khusus untuk pemula Indonesia — terutama yang selama ini kesulitan belajar bahasa Inggris dari subtitle atau buku formal.

Bot ini berbicara dalam bahasa Indonesia yang santai dan ramah, layaknya teman yang sabar ngajarin kamu pelan-pelan. Tidak ada gaya guru yang kaku, yang ada hanya teman belajar yang asik!

> *"Belajar Bahasa Inggris sambil santai, tanpa malu, tanpa ribet."*

---

## 🎯 Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 💬 **Tutor Percakapan** | Belajar dari dialog natural gaya *Friends* — kontekstual, bukan hafalan rumus |
| 🃏 **Flashcard Kosakata** | Latihan vocab interaktif dengan sistem flipchart — pilih topik, jawab, cek skor |
| 📊 **Sistem Level** | Mulai dari kalimat dasar hingga slang & percakapan natural |
| 🔄 **State Management** | Bot mengingat percakapan & progress kamu dalam sesi |
| 🤖 **Multi-AI Fallback** | Gemini AI → Replit AI → OpenAI, otomatis pindah jika satu error |
| 🌙 **Always Online** | Keep-alive server untuk UptimeRobot monitoring |

---

## 📚 Topik Flashcard

Kamu bisa latihan vocab dengan 7 kategori:

```
🍽️ Makanan & Minuman    🎨 Warna         👨‍👩‍👧‍👦 Keluarga
🐾 Hewan                🧑 Bagian Tubuh  😊 Emosi & Perasaan
🏃 Aktivitas Sehari-hari          🎲 Random (campuran semua)
```

---

## 🤖 Cara Pakai Bot

### Langkah 1 — Buka bot di Telegram
Cari **[@sinau_inggris_bot](https://t.me/sinau_inggris_bot)** atau klik link di atas.

### Langkah 2 — Mulai sesi
Ketik `/start` untuk memulai. Bot akan menyapa dan siap belajar!

### Langkah 3 — Kirim pesan
Kamu bisa kirim:
- **Kata/kalimat bahasa Inggris** → Bot langsung bahas artinya + contoh
- **Kalimat bahasa Indonesia** → Bot terjemahkan + ajarkan cara pakainya
- **Pesan bebas / sapa** → Bot yang tentuin materi hari ini

### Langkah 4 — Latihan
Setiap sesi materi selalu diakhiri dengan latihan kecil. Jawab saja dengan kalimat biasa!

### Langkah 5 — Pilih menu lanjutan
Setelah dapat feedback, balas:
```
1  →  Ulangi materi
2  →  Latihan lagi (topik sama)
3  →  Naik level / materi baru
```

### Langkah 6 — Coba Flashcard Vocab
Ketik `/vocab` untuk latihan kosakata dengan sistem kartu:
```
Bot  : 🃏 Card 1/10
       🇬🇧 RICE
       Apa artinya dalam bahasa Indonesia?

Kamu : nasi

Bot  : ✅ Betul! RICE = nasi
       "I eat rice every day."
```

---

## 📋 Daftar Perintah

| Perintah | Fungsi |
|----------|--------|
| `/start` | Mulai sesi belajar baru |
| `/menu` | Tampilkan panduan lengkap |
| `/vocab` | Latihan kosakata flashcard |
| `/stop` | Hentikan sesi flashcard |
| `/reset` | Reset sesi dari awal |

---

## 🚀 Deploy Sendiri

### Prasyarat
- Python 3.11+
- Telegram Bot Token (dari [@BotFather](https://t.me/BotFather))
- Google Gemini API Key (dari [Google AI Studio](https://aistudio.google.com))

### Instalasi

```bash
# Clone repo
git clone https://github.com/afganitkj-creator/bot-sinau-inggris.git
cd bot-sinau-inggris

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env dan isi token/API key kamu
```

### Konfigurasi `.env`

```env
TELEGRAM_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key   # opsional, sebagai fallback
AI_PROVIDER=gemini                    # gemini atau openai
BOT_HEALTH_PORT=8000                  # port untuk health check
```

### Jalankan

```bash
python bot.py
```

---

## 🔁 Keep-Alive dengan UptimeRobot

Bot menyertakan server health check internal. Daftarkan URL berikut ke [UptimeRobot](https://uptimerobot.com) agar bot tidak tidur:

```
https://<your-replit-domain>/api/healthz
```

Rekomendasi interval: **setiap 5 menit**.

---

## 🧠 Alur Pembelajaran AI

```
Input User
    │
    ├── Bahasa Inggris  →  Bahas + Terjemah + Contoh + Latihan
    ├── Bahasa Indonesia →  Translate + Ajarkan Konteks + Latihan  
    └── Bebas / Sapa    →  AI buat materi sendiri (Friends-style)
    
Setelah Latihan
    │
    └── Feedback → 1. Ulangi / 2. Latihan lagi / 3. Naik level
```

**Level sistem:**
```
Level 1  →  Kalimat dasar
Level 2  →  Percakapan sehari-hari
Level 3  →  Slang & natural speech
Level 4  →  User buat kalimat sendiri
```

---

## 🛠️ Tech Stack

```
Language  : Python 3.11
Framework : python-telegram-bot 20.7
AI        : Google Gemini 1.5 Flash (primary)
            Replit AI / OpenAI GPT (fallback)
Deploy    : Replit (always-on)
Monitor   : UptimeRobot
```

---

## 📁 Struktur File

```
bot-sinau-inggris/
├── bot.py            # Handler utama & command routing
├── ai_handler.py     # Integrasi AI (Gemini + OpenAI)
├── system_prompt.py  # System prompt tutor AI
├── vocab_handler.py  # Logic flashcard kosakata
├── vocab_data.py     # Database 100+ kosakata (7 topik)
├── keep_alive.py     # Health check server
├── requirements.txt  # Python dependencies
└── .env.example      # Template environment variables
```

---

## 🤝 Kontribusi

Pull request dan issue sangat disambut! Kalau kamu punya ide topik kosakata baru, perbaikan prompt, atau fitur tambahan — langsung aja buka PR.

---

## 📄 Lisensi

MIT License — bebas dipakai, dimodifikasi, dan disebarkan.

---

<div align="center">

Dibuat dengan ❤️ untuk pelajar bahasa Inggris Indonesia

**[⭐ Star repo ini](https://github.com/afganitkj-creator/bot-sinau-inggris)** kalau bermanfaat!

</div>
