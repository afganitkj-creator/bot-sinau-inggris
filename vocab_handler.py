"""
Handles flashcard/flipchart vocabulary learning sessions.
State per user stored in vocab_sessions dict.
"""

import difflib
from vocab_data import get_words_for_category, get_category_by_number, get_category_list, CATEGORY_COUNT, VOCAB_CATEGORIES

# vocab_sessions[user_id] = {
#   "active": bool,
#   "words": list of word dicts,
#   "index": int,          # current card index (0-based)
#   "score": int,          # correct answers
#   "waiting_answer": bool # True when we're waiting for user answer
# }
vocab_sessions = {}

def is_in_vocab_session(user_id):
    s = vocab_sessions.get(user_id)
    return s is not None and s.get("active", False)

def is_waiting_category(user_id):
    s = vocab_sessions.get(user_id)
    return s is not None and s.get("waiting_category", False)

def start_vocab_session(user_id):
    """Initiate vocab session — ask user to pick category."""
    vocab_sessions[user_id] = {"active": False, "waiting_category": True}
    return (
        "📚 *Flashcard Vocab — Pilih Topik!*\n\n"
        + get_category_list()
        + "\n\nBalas dengan *angka* topik yang kamu mau ya!"
    )

def handle_category_choice(user_id, text):
    """Process user's category number selection."""
    try:
        num = int(text.strip())
    except ValueError:
        return "Balasnya pakai *angka* ya, contoh: `1` atau `2` 😊", False

    category_key = get_category_by_number(num)
    if category_key is None:
        return f"Pilihannya antara 1 sampai {CATEGORY_COUNT + 1} aja ya!", False

    words = get_words_for_category(category_key)
    if not words:
        return "Waduh, topiknya kosong nih. Coba pilih yang lain!", False

    if category_key == "random":
        label = "🎲 Random"
    else:
        label = VOCAB_CATEGORIES[category_key]["label"]

    vocab_sessions[user_id] = {
        "active": True,
        "waiting_category": False,
        "words": words,
        "index": 0,
        "score": 0,
        "waiting_answer": True,
        "category_label": label,
    }

    card_text = _build_card(user_id)
    return f"Oke! Mulai sesi *{label}*!\n\n" + card_text, True

def handle_vocab_answer(user_id, user_answer):
    """Evaluate user answer and advance to next card or finish session."""
    s = vocab_sessions.get(user_id)
    if not s or not s["active"]:
        return None, False

    current_word = s["words"][s["index"]]
    correct_id = current_word["id"].lower()
    given = user_answer.strip().lower()

    # Accept answer if it's close enough (difflib ratio > 0.75)
    # Also accept exact match or partial match for compound answers (e.g. "nasi/beras")
    accepted_answers = [a.strip() for a in correct_id.replace("/", "|").split("|")]
    is_correct = False
    for accepted in accepted_answers:
        ratio = difflib.SequenceMatcher(None, given, accepted).ratio()
        if ratio >= 0.80 or given == accepted:
            is_correct = True
            break

    if is_correct:
        s["score"] += 1
        feedback = (
            f"✅ *Betul!*\n"
            f"*{current_word['en'].upper()}* = *{current_word['id']}*\n"
            f"_{current_word['example']}_"
        )
    else:
        feedback = (
            f"❌ *Belum tepat.*\n"
            f"*{current_word['en'].upper()}* = *{current_word['id']}*\n"
            f"_{current_word['example']}_"
        )

    s["index"] += 1
    total = len(s["words"])

    if s["index"] >= total:
        # Session finished
        score = s["score"]
        s["active"] = False
        del vocab_sessions[user_id]

        if score == total:
            emoji = "🏆"
            comment = "Sempurna! Kamu luar biasa!"
        elif score >= total * 0.7:
            emoji = "🎉"
            comment = "Bagus banget! Terus semangat!"
        elif score >= total * 0.4:
            emoji = "💪"
            comment = "Lumayan! Latihan lagi yuk!"
        else:
            emoji = "📖"
            comment = "Santai, belajar itu proses. Coba lagi ya!"

        result_text = (
            f"{feedback}\n\n"
            f"{'─'*25}\n"
            f"{emoji} *Sesi selesai!*\n"
            f"Skor kamu: *{score}/{total}*\n"
            f"{comment}\n\n"
            f"Ketik /vocab untuk main lagi, atau lanjut ngobrol belajar biasa aja!"
        )
        return result_text, True
    else:
        next_card = _build_card(user_id)
        return f"{feedback}\n\n{'─'*25}\n\n{next_card}", True

def _build_card(user_id):
    s = vocab_sessions[user_id]
    idx = s["index"]
    total = len(s["words"])
    word = s["words"][idx]

    return (
        f"🃏 *Kartu {idx+1} dari {total}*\n\n"
        f"🇬🇧  *{word['en'].upper()}*\n\n"
        f"Apa artinya dalam bahasa Indonesia?"
    )

def cancel_vocab_session(user_id):
    """Cancel an active session."""
    if user_id in vocab_sessions:
        del vocab_sessions[user_id]
    return "Sesi flashcard dihentikan. Kapan-kapan lanjut lagi ya! 😊"
