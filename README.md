<div align="center">

# 🤖 English Mas/Mbak Bot

### Tutor Bahasa Inggris AI untuk Pemula Indonesia

*Belajar bahasa Inggris terasa susah? Aku hadir buat nemenin kamu — santai, sabar, dan seru!*

[![Telegram](https://img.shields.io/badge/Telegram-@sinau__inggris__bot-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/sinau_inggris_bot)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Gemini](https://img.shields.io/badge/Gemini_AI-Powered-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![OpenAI](https://img.shields.io/badge/OpenAI-Whisper_+_Fallback-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

</div>

## ✨ Tentang Bot

**English Mas/Mbak** adalah bot Telegram berbasis AI yang dirancang khusus untuk membantu orang Indonesia belajar bahasa Inggris dari nol — dengan pendekatan yang santai, sabar, dan interaktif seperti punya teman tutor pribadi.

---

## 🚀 Fitur Utama

### 🎯 AI Assessment (Tes Penempatan Level)
> `/assessment`

Tes awal **10 soal** yang dirancang untuk menganalisis kemampuan pengguna dari level Pemula hingga Lanjutan. Setelah tes, kurikulum belajar otomatis disesuaikan dengan level kamu.

```
Soal 1 dari 10
🟦⬜⬜⬜⬜⬜⬜⬜⬜⬜

Pilih yang benar: 'I ___ a student.'

A. am
B. is
C. are
D. be

Ketik A, B, C, atau D
```

**Hasil assessment:**
| Skor | Level |
|------|-------|
| 0–3  | Pemula 🌱 |
| 4–7  | Menengah 📈 |
| 8–10 | Lanjutan 🚀 |

---

### 💬 AI Role-play — Simulasi Percakapan Nyata
> `/roleplay`

Latihan percakapan interaktif dengan AI yang berperan sebagai lawan bicara dalam situasi nyata. Tersedia **5 skenario**:

| # | Skenario | Deskripsi |
|---|----------|-----------|
| 1 | 💼 Wawancara Kerja | Simulasi wawancara HRD dalam bahasa Inggris |
| 2 | 🍽️ Di Restoran | Pesan makanan dan berinteraksi dengan waiter |
| 3 | ✈️ Di Bandara | Check-in, imigrasi, hingga boarding |
| 4 | 🛍️ Belanja | Tanya produk, tawar-menawar di toko |
| 5 | 🏥 Ke Dokter | Konsultasi medis dalam bahasa Inggris |

Setelah **8 percakapan**, AI otomatis memberikan feedback lengkap tentang grammar dan vocabulary kamu.

---

### 📚 Grammar Coach — Belajar Tata Bahasa
> `/grammar` → `/latihan`

10 topik grammar yang tersusun dari dasar ke lanjutan, lengkap dengan penjelasan dan soal latihan interaktif:

| # | Topik |
|---|-------|
| 1 | ⏰ Present Simple |
| 2 | 📖 Past Simple |
| 3 | 🔮 Future Tense (will / going to) |
| 4 | 📌 Articles (a, an, the) |
| 5 | 🔑 Modal Verbs (can, should, must) |
| 6 | 🕐 Prepositions of Time (in, on, at) |
| 7 | 🔄 Passive Voice |
| 8 | 🤔 Conditional Sentences |
| 9 | 💬 Reported Speech |
| 10 | 💡 Phrasal Verbs |

---

### 🎤 Analisis Suara (Voice Analyzer)
> Kirim pesan suara langsung ke bot

Kirim pesan suara dalam bahasa Inggris, dan bot akan:
1. **Transkripsi** ucapan kamu otomatis (via OpenAI Whisper)
2. **Koreksi grammar** dan vocabulary
3. **Berikan versi yang lebih natural**
4. **Skor 1–10** sebagai feedback

```
🎤 Yang kamu ucapkan: "I go to school yesterday"
✅ Koreksi grammar: "I went to school yesterday" (past tense)
📝 Versi lebih natural: "I went to school yesterday."
💡 Tips: Gunakan past tense (went) untuk kejadian kemarin
⭐ Skor: 7/10
```

---

### 🃏 Flashcard Kosakata
> `/vocab`

Sesi flashcard interaktif dengan **7 topik kategori** dan **100+ kosakata**:

`makanan` · `warna` · `keluarga` · `hewan` · `tubuh` · `emosi` · `aktivitas` · `🎲 acak`

- **Random mode**: 20 kata dari semua topik (~10 menit)
- **Per kategori**: 15 kata per sesi
- Sistem penilaian dengan fuzzy matching (typo kecil masih dihitung)

---

### 💬 Percakapan Bebas + AI Tutor
Kirim teks apa saja — bot akan merespons sesuai level dan konteksmu:

| Input | Respons Bot |
|-------|-------------|
| Kalimat bahasa Inggris | Dibahas + diajari |
| Kalimat bahasa Indonesia | Diterjemahkan + diajarkan |
| Input bebas | Bot yang buatkan materi |

---

## 🤖 Arsitektur AI

```
Gemini 1.5 Flash (Primary)
       ↓ (jika gagal/quota habis)
Replit AI Integration (OpenAI-compatible)
       ↓ (jika gagal)
OpenAI GPT-3.5 (Fallback)
```

**Transkripsi suara:** OpenAI Whisper-1

---

## 📱 Semua Command

| Command | Fungsi |
|---------|--------|
| `/start` | Mulai / kembali ke menu utama |
| `/assessment` | Tes penempatan level (10 soal) |
| `/roleplay` | Pilih dan mulai sesi role-play |
| `/grammar` | Buka grammar coach |
| `/grammar menu` | Pilih topik grammar |
| `/latihan` | Mulai soal latihan grammar |
| `/vocab` | Mulai flashcard kosakata |
| `/menu` | Lihat panduan lengkap |
| `/stop` | Hentikan semua sesi aktif |
| `/reset` | Reset sesi dan profil |

---

## ⚙️ Cara Deploy Sendiri

### 1. Clone repo

```bash
git clone https://github.com/afganitkj-creator/bot-sinau-inggris.git
cd bot-sinau-inggris
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Buat file `.env`

```env
TELEGRAM_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key   # opsional, untuk voice + fallback
AI_PROVIDER=gemini
BOT_HEALTH_PORT=8000
```

### 4. Jalankan bot

```bash
python bot.py
```

---

## 📡 Setup UptimeRobot (Agar Bot Tidak Mati)

1. Buka [uptimerobot.com](https://uptimerobot.com) → Create Monitor
2. **Monitor Type**: HTTP(s)
3. **URL**: `https://YOUR_REPLIT_DOMAIN/api/healthz`
4. **Interval**: 5 menit

---

## 📁 Struktur File

```
bot-telegram/
├── bot.py                # Orchestrator utama + semua handlers
├── ai_handler.py         # Multi-AI fallback (Gemini → Replit → OpenAI)
├── system_prompt.py      # System prompt level-aware (beginner/intermediate/advanced)
├── assessment_handler.py # Placement test 10 soal
├── roleplay_handler.py   # 5 skenario role-play AI
├── grammar_handler.py    # Grammar Coach 10 topik
├── voice_handler.py      # Voice → Whisper → analisis grammar
├── vocab_handler.py      # Flashcard sesi + scoring
├── vocab_data.py         # 100+ kosakata per 7 topik
├── user_profile.py       # Level & profil pengguna
├── keep_alive.py         # Health check server (UptimeRobot)
├── requirements.txt      # Python dependencies
└── .env.example          # Template konfigurasi
```

---

## 🛠️ Tech Stack

- **Runtime**: Python 3.11
- **Bot Framework**: python-telegram-bot 20.7
- **AI Primary**: Google Gemini 1.5 Flash (`google-genai`)
- **AI Fallback**: OpenAI GPT via Replit AI Integration
- **Voice Transcription**: OpenAI Whisper-1
- **Hosting**: Replit (free tier)
- **Uptime Monitor**: UptimeRobot

---

<div align="center">
<i>Dibuat dengan ❤️ untuk membantu orang Indonesia belajar bahasa Inggris</i>
</div>
