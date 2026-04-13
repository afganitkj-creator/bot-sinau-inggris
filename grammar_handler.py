
# Note: exercise blanks use ＿＿＿ (fullwidth underscore U+FF3F) to avoid
# Telegram Markdown parsing issues caused by regular underscores.

BLANK = "＿＿＿"

GRAMMAR_TOPICS = [
    {
        "id": 1,
        "title": "Present Simple — Kebiasaan Sehari-hari",
        "emoji": "⏰",
        "explanation": (
            "*Present Simple* dipakai untuk kebiasaan, fakta, atau rutinitas.\n\n"
            "Rumus:\n"
            "• I/You/We/They + *kata kerja dasar*\n"
            "• He/She/It + *kata kerja + s/es*\n\n"
            "Contoh:\n"
            "• I *eat* rice every day. (Saya makan nasi setiap hari)\n"
            "• She *goes* to the market on Sunday.\n"
            "• Water *boils* at 100°C. (Air mendidih di 100°C)"
        ),
        "exercise": "Lengkapi: 'My brother ＿＿＿ (work) at a bank.'",
        "answer": "works",
        "hint": "Subjek 'My brother' = He → kata kerja + s → works",
    },
    {
        "id": 2,
        "title": "Past Simple — Cerita Masa Lalu",
        "emoji": "📖",
        "explanation": (
            "*Past Simple* dipakai untuk kejadian yang sudah selesai di masa lalu.\n\n"
            "Rumus:\n"
            "• Regular verb: + *ed* (work→worked, play→played)\n"
            "• Irregular verb: bentuk khusus (go→went, eat→ate, buy→bought)\n\n"
            "Contoh:\n"
            "• I *watched* a movie last night.\n"
            "• She *went* to Bali last month.\n"
            "• They *bought* a new car yesterday."
        ),
        "exercise": "Ubah ke past tense: 'I ＿＿＿ (go) to school by bus this morning.'",
        "answer": "went",
        "hint": "'go' adalah irregular verb → bentuk past-nya 'went'",
    },
    {
        "id": 3,
        "title": "Future Tense — Rencana & Prediksi",
        "emoji": "🔮",
        "explanation": (
            "Ada dua cara utama menyatakan masa depan:\n\n"
            "1. *Will* → prediksi / keputusan spontan\n"
            "   • It *will* rain tomorrow.\n"
            "   • I *will* help you!\n\n"
            "2. *Going to* → rencana yang sudah dipikirkan\n"
            "   • I *am going to* visit Jakarta next week.\n"
            "   • She *is going to* study medicine."
        ),
        "exercise": "Pilih yang tepat: 'Watch out! You ＿＿＿ fall!' (will / going to)",
        "answer": "are going to",
        "hint": "Bahaya sudah terlihat → 'going to' untuk prediksi berdasarkan bukti nyata.",
    },
    {
        "id": 4,
        "title": "Articles — a, an, the",
        "emoji": "📌",
        "explanation": (
            "*a* / *an* → benda yang belum spesifik / pertama kali disebut\n"
            "• *a* + konsonan: a book, a cat\n"
            "• *an* + bunyi vokal: an apple, an hour\n\n"
            "*the* → benda yang sudah spesifik / diketahui\n\n"
            "Contoh:\n"
            "• I saw *a* dog. *The* dog was cute.\n"
            "• *The* sun rises in the east.\n"
            "• She is *an* honest person. (honest bunyi 'o')"
        ),
        "exercise": "Isi artikel: 'I want to be ＿＿＿ engineer someday.'",
        "answer": "an",
        "hint": "'engineer' dimulai bunyi vokal 'e' → pakai 'an'",
    },
    {
        "id": 5,
        "title": "Modal Verbs — can, should, must",
        "emoji": "🔑",
        "explanation": (
            "Modal verbs menambahkan *makna tambahan* pada kata kerja:\n\n"
            "• *can* → kemampuan / izin → _I can swim._\n"
            "• *should* → saran → _You should drink more water._\n"
            "• *must* → kewajiban kuat → _You must wear a seatbelt._\n"
            "• *could* → permintaan sopan → _Could you help me?_\n\n"
            "Setelah modal → *kata kerja dasar* (tanpa s/to)"
        ),
        "exercise": "Pilih yang tepat: 'You ＿＿＿ see a doctor. You look sick.'",
        "answer": "should",
        "hint": "Saran = should. Must lebih kuat (kewajiban wajib).",
    },
    {
        "id": 6,
        "title": "Prepositions of Time — in, on, at",
        "emoji": "🕐",
        "explanation": (
            "Tiga preposisi waktu yang paling sering salah:\n\n"
            "• *at* → waktu spesifik: _at 7 PM, at midnight_\n"
            "• *on* → hari & tanggal: _on Monday, on July 4th_\n"
            "• *in* → bulan, tahun, periode: _in January, in 2024, in the morning_\n\n"
            "Trik: *A-O-I* (At → On → In) = makin spesifik → makin umum"
        ),
        "exercise": "Isi preposisi: 'The meeting is ＿＿＿ Monday ＿＿＿ 9 AM.'",
        "answer": "on / at",
        "hint": "Hari = on Monday. Waktu spesifik = at 9 AM.",
    },
    {
        "id": 7,
        "title": "Passive Voice — Kalimat Pasif",
        "emoji": "🔄",
        "explanation": (
            "Passive voice: objek lebih penting dari pelaku.\n\n"
            "Rumus: *Subject + to be + V3 (past participle)*\n\n"
            "Contoh:\n"
            "• Active: *The chef cooks* the food.\n"
            "• Passive: *The food is cooked* by the chef.\n\n"
            "• Active: *Someone stole* my phone.\n"
            "• Passive: *My phone was stolen.*\n\n"
            "Common V3: eaten, written, made, broken, sold, built"
        ),
        "exercise": "Ubah ke passive: 'The teacher explains the lesson.'\n→ 'The lesson ＿＿＿ by the teacher.'",
        "answer": "is explained",
        "hint": "Subjek baru (the lesson) + is + explained (V3 dari explain)",
    },
    {
        "id": 8,
        "title": "Conditional Sentences — Kalimat Pengandaian",
        "emoji": "🤔",
        "explanation": (
            "3 tipe conditional:\n\n"
            "• *Type 1* (mungkin terjadi):\n"
            "  If + present → will + infinitive\n"
            "  _If it rains, I will stay home._\n\n"
            "• *Type 2* (khayalan):\n"
            "  If + past → would + infinitive\n"
            "  _If I were rich, I would travel._\n\n"
            "• *Type 3* (penyesalan masa lalu):\n"
            "  If + had + V3 → would have + V3\n"
            "  _If I had studied, I would have passed._"
        ),
        "exercise": "Lengkapi (Type 1): 'If she ＿＿＿ (study) hard, she will pass.'",
        "answer": "studies",
        "hint": "Type 1: If + present simple. she → studies (he/she/it + s)",
    },
    {
        "id": 9,
        "title": "Reported Speech — Kalimat Tidak Langsung",
        "emoji": "💬",
        "explanation": (
            "Reported speech: menceritakan ulang ucapan orang lain.\n\n"
            "Perubahan tense (backshift):\n"
            "• am/is/are → was/were\n"
            "• will → would\n"
            "• can → could\n\n"
            "Contoh:\n"
            "• Direct: He said, 'I *am* hungry.'\n"
            "• Reported: He said that he *was* hungry.\n\n"
            "• Direct: She said, 'I *will* call you.'\n"
            "• Reported: She said that she *would* call me."
        ),
        "exercise": "Ubah: 'She said, I can help you.' → She said that she ＿＿＿ help me.",
        "answer": "could",
        "hint": "'can' dalam reported speech berubah menjadi 'could'",
    },
    {
        "id": 10,
        "title": "Phrasal Verbs — Kata Kerja Majemuk",
        "emoji": "💡",
        "explanation": (
            "Phrasal verbs = kata kerja + preposisi yang artinya berbeda.\n\n"
            "Yang paling sering dipakai:\n"
            "• *give up* = menyerah → _Don't give up!_\n"
            "• *look up* = mencari → _Look it up on Google._\n"
            "• *turn on/off* = nyalakan/matikan → _Turn off the light._\n"
            "• *put off* = menunda → _Don't put off your homework._\n"
            "• *get along* = rukun → _We get along well._\n"
            "• *run out of* = kehabisan → _I ran out of money._"
        ),
        "exercise": "Isi phrasal verb: 'I ＿＿＿ trying. I will do it!' (tidak menyerah)",
        "answer": "won't give up",
        "hint": "'give up' = menyerah. 'won't give up' = tidak akan menyerah.",
    },
]

grammar_sessions = {}


def get_grammar_menu():
    lines = ["📚 *Grammar Coach — Pilih Topik:*\n"]
    for t in GRAMMAR_TOPICS:
        lines.append(f"*{t['id']}.* {t['emoji']} {t['title']}")
    lines.append(f"\nKetik angka *1–{len(GRAMMAR_TOPICS)}* untuk mulai!")
    return "\n".join(lines)


def start_grammar(user_id, topic_num=None):
    if topic_num:
        idx = topic_num - 1
    else:
        existing = grammar_sessions.get(user_id, {})
        idx = existing.get("topic_idx", 0)

    grammar_sessions[user_id] = {"state": "learning", "topic_idx": idx}
    return _format_lesson(idx)


def start_grammar_menu(user_id):
    """Show topic list and set state to choosing."""
    grammar_sessions[user_id] = {"state": "choosing", "topic_idx": 0}
    return get_grammar_menu()


def is_in_grammar(user_id):
    s = grammar_sessions.get(user_id)
    return s and s["state"] == "exercise"


def is_choosing_grammar(user_id):
    s = grammar_sessions.get(user_id)
    return s and s["state"] == "choosing"


def handle_grammar_choice(user_id, text):
    try:
        num = int(text.strip())
        if 1 <= num <= len(GRAMMAR_TOPICS):
            return start_grammar(user_id, num), True
    except ValueError:
        pass
    return f"Ketik angka *1* sampai *{len(GRAMMAR_TOPICS)}* ya!", False


def show_grammar_exercise(user_id):
    s = grammar_sessions.get(user_id)
    if not s:
        return None
    idx = s["topic_idx"]
    topic = GRAMMAR_TOPICS[idx]
    s["state"] = "exercise"
    return (
        f"✏️ *Latihan — {topic['emoji']} {topic['title']}*\n\n"
        f"{topic['exercise']}\n\n"
        f"_Ketik jawabanmu!_"
    )


def handle_grammar_answer(user_id, answer_text):
    s = grammar_sessions.get(user_id)
    if not s or s["state"] != "exercise":
        return None

    idx = s["topic_idx"]
    topic = GRAMMAR_TOPICS[idx]
    answer_lower = answer_text.strip().lower()
    correct_lower = topic["answer"].lower()

    is_correct = correct_lower in answer_lower or answer_lower == correct_lower

    if is_correct:
        feedback = f"✅ *Benar!*\nJawaban: _{topic['answer']}_\n\n_{topic['hint']}_"
    else:
        feedback = (
            f"❌ *Hampir!*\n"
            f"Jawabanmu: _{answer_text}_\n"
            f"Yang benar: *{topic['answer']}*\n\n"
            f"_{topic['hint']}_"
        )

    next_idx = (idx + 1) % len(GRAMMAR_TOPICS)
    del grammar_sessions[user_id]

    next_topic = GRAMMAR_TOPICS[next_idx]
    nav = (
        f"\n\n━━━━━━━━━━━━━━━━━━\n"
        f"Topik berikutnya: *{next_topic['emoji']} {next_topic['title']}*\n"
        f"Ketik /grammar untuk lanjut, atau /grammar menu untuk pilih topik lain."
    )
    return feedback + nav, is_correct


def _format_lesson(idx):
    topic = GRAMMAR_TOPICS[idx % len(GRAMMAR_TOPICS)]
    total = len(GRAMMAR_TOPICS)
    return (
        f"📚 *Topik {topic['id']}/{total}: {topic['emoji']} {topic['title']}*\n\n"
        f"{topic['explanation']}\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"Ketik /latihan untuk mulai latihan soal!"
    )


def cancel_grammar(user_id):
    if user_id in grammar_sessions:
        del grammar_sessions[user_id]
