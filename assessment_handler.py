
ASSESSMENT_QUESTIONS = [
    {
        "id": 1, "level": "beginner",
        "question": "Pilih yang benar: 'I ___ a student.'",
        "options": {"A": "am", "B": "is", "C": "are", "D": "be"},
        "answer": "A",
        "explanation": "'I' selalu pakai 'am'. Contoh: I am happy, I am here.",
    },
    {
        "id": 2, "level": "beginner",
        "question": "Kata bahasa Inggris untuk 'makan' adalah?",
        "options": {"A": "drink", "B": "sleep", "C": "eat", "D": "walk"},
        "answer": "C",
        "explanation": "Eat = makan. Drink = minum. Sleep = tidur. Walk = jalan kaki.",
    },
    {
        "id": 3, "level": "beginner",
        "question": "Lengkapi: 'She ___ to school every day.'",
        "options": {"A": "go", "B": "goes", "C": "gone", "D": "going"},
        "answer": "B",
        "explanation": "She/He/It + kata kerja + s/es (present simple). Jadi 'goes', bukan 'go'.",
    },
    {
        "id": 4, "level": "beginner",
        "question": "Apa arti 'Where are you from?'",
        "options": {"A": "Kamu mau ke mana?", "B": "Kamu dari mana?", "C": "Kamu siapa?", "D": "Kamu mau apa?"},
        "answer": "B",
        "explanation": "'Where are you from?' artinya menanyakan asal seseorang. 'Kamu dari mana?'",
    },
    {
        "id": 5, "level": "intermediate",
        "question": "Mana yang paling benar untuk cerita masa lalu?",
        "options": {"A": "Yesterday I go to market", "B": "Yesterday I went to market", "C": "Yesterday I going to market", "D": "Yesterday I goes to market"},
        "answer": "B",
        "explanation": "Untuk kejadian masa lalu pakai past tense. 'go' menjadi 'went' (irregular verb).",
    },
    {
        "id": 6, "level": "intermediate",
        "question": "Pilih kalimat yang grammarnya benar:",
        "options": {"A": "He don't like coffee", "B": "He doesn't likes coffee", "C": "He doesn't like coffee", "D": "He not like coffee"},
        "answer": "C",
        "explanation": "He/She/It + doesn't + kata kerja dasar. 'He doesn't like' ✓ (bukan 'doesn't likes').",
    },
    {
        "id": 7, "level": "intermediate",
        "question": "Lengkapi: 'She is ___ honest person.'",
        "options": {"A": "a", "B": "an", "C": "the", "D": "(tanpa artikel)"},
        "answer": "B",
        "explanation": "'an' dipakai sebelum bunyi vokal. 'honest' → bunyi /ɒnɪst/, dimulai bunyi 'o', jadi pakai 'an'.",
    },
    {
        "id": 8, "level": "intermediate",
        "question": "'___ tired, he continued working.' Pilih yang benar:",
        "options": {"A": "Despite be", "B": "Despite being", "C": "Despite been", "D": "Despite was"},
        "answer": "B",
        "explanation": "'Despite' diikuti kata benda atau V+ing. 'Despite being tired' = 'Meskipun lelah'.",
    },
    {
        "id": 9, "level": "advanced",
        "question": "Pilih yang paling formal untuk email profesional:",
        "options": {"A": "I wanna ask something", "B": "I want to ask", "C": "I would like to enquire", "D": "Can I ask?"},
        "answer": "C",
        "explanation": "'I would like to enquire' adalah ekspresi paling formal dan sopan untuk email bisnis.",
    },
    {
        "id": 10, "level": "advanced",
        "question": "'He ___ the answer if he had studied harder.'",
        "options": {"A": "would know", "B": "would have known", "C": "will know", "D": "had known"},
        "answer": "B",
        "explanation": "Conditional Type 3 (unreal past): If + had + V3, would have + V3. Menyatakan penyesalan.",
    },
]

assessment_sessions = {}


def start_assessment(user_id):
    assessment_sessions[user_id] = {"current": 0, "score": 0, "answers": []}
    intro = (
        "🎯 *Assessment Bahasa Inggrismu*\n\n"
        "Tes ini terdiri dari *10 soal* untuk mengetahui level kamu — "
        "Pemula, Menengah, atau Lanjutan.\n"
        "Jawab dengan huruf *A / B / C / D* ya!\n\n"
        "Santai aja, ini bukan ujian sekolah 😊\n\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
    )
    return intro + _format_question(user_id)


def is_in_assessment(user_id):
    return user_id in assessment_sessions


def _format_question(user_id):
    session = assessment_sessions[user_id]
    idx = session["current"]
    if idx >= len(ASSESSMENT_QUESTIONS):
        return None
    q = ASSESSMENT_QUESTIONS[idx]
    total = len(ASSESSMENT_QUESTIONS)
    progress = "🟦" * (idx) + "⬜" * (total - idx)
    lines = [
        f"*Soal {idx + 1} dari {total}*",
        f"{progress}\n",
        q["question"] + "\n",
    ]
    for key, val in q["options"].items():
        lines.append(f"  *{key}.* {val}")
    lines.append("\n_Ketik A, B, C, atau D_")
    return "\n".join(lines)


def handle_assessment_answer(user_id, answer_text):
    session = assessment_sessions.get(user_id)
    if not session:
        return "Kamu belum mulai tes. Ketik /assessment untuk mulai.", False, None

    answer = answer_text.strip().upper()
    if answer not in ["A", "B", "C", "D"]:
        return "Tolong jawab dengan huruf *A*, *B*, *C*, atau *D* ya!", False, None

    idx = session["current"]
    q = ASSESSMENT_QUESTIONS[idx]
    is_correct = answer == q["answer"]

    if is_correct:
        session["score"] += 1
        feedback = f"✅ *Benar!*\n_{q['explanation']}_"
    else:
        correct_val = q["options"][q["answer"]]
        feedback = (
            f"❌ *Kurang tepat.*\n"
            f"Jawaban benar: *{q['answer']}. {correct_val}*\n"
            f"_{q['explanation']}_"
        )

    session["current"] += 1
    session["answers"].append({"q": idx + 1, "correct": is_correct})

    if session["current"] >= len(ASSESSMENT_QUESTIONS):
        result_msg, level = _calculate_result(session)
        del assessment_sessions[user_id]
        return feedback + "\n\n" + result_msg, True, level

    next_q = _format_question(user_id)
    return feedback + "\n\n" + next_q, False, None


def _calculate_result(session):
    score = session["score"]
    total = len(ASSESSMENT_QUESTIONS)

    if score <= 3:
        level = "beginner"
        label = "Pemula 🌱"
        desc = "Santai, semua orang mulai dari sini! Kita belajar dari dasar bareng."
        tip = "Yuk mulai dengan kosakata dasar dan kalimat sederhana sehari-hari!"
    elif score <= 7:
        level = "intermediate"
        label = "Menengah 📈"
        desc = "Bagus! Kamu udah punya fondasi yang oke. Saatnya naik level!"
        tip = "Kamu siap latihan percakapan, grammar lebih kompleks, dan roleplay!"
    else:
        level = "advanced"
        label = "Lanjutan 🚀"
        desc = "Wow, impressive! Level kamu sudah tinggi banget!"
        tip = "Kita bisa latihan percakapan advanced, idiom, dan simulasi nyata!"

    bars = "🟩" * score + "⬜" * (total - score)

    msg = (
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🎯 *Hasil Assessment Kamu*\n\n"
        f"{bars}\n"
        f"Skor: *{score}/{total}*\n"
        f"Level: *{label}*\n\n"
        f"{desc}\n\n"
        f"💡 {tip}\n\n"
        f"Kurikulummu sudah disesuaikan! Ketik /menu untuk lihat semua fitur."
    )
    return msg, level


def cancel_assessment(user_id):
    if user_id in assessment_sessions:
        del assessment_sessions[user_id]
        return "Sesi assessment dibatalkan."
    return "Tidak ada sesi assessment yang aktif."
