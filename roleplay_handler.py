
SCENARIOS = {
    "1": {
        "name": "Wawancara Kerja 💼",
        "description": "Simulasi wawancara kerja dalam bahasa Inggris. Aku jadi HRD-nya!",
        "system_role": (
            "You are an HR interviewer at a professional company. "
            "Conduct a job interview in English. Ask common interview questions one at a time. "
            "After each user answer, give brief, friendly feedback in Indonesian (1-2 sentences), "
            "then ask the next interview question. Keep it realistic but supportive. "
            "After 8 exchanges, wrap up with overall feedback in Indonesian about their English."
        ),
        "opening": (
            "Good morning! Please have a seat. My name is Sarah, I'm the HR Manager here.\n\n"
            "_HR: So, could you start by telling me a little about yourself?_"
        ),
    },
    "2": {
        "name": "Di Restoran 🍽️",
        "description": "Latihan pesan makanan di restoran berbahasa Inggris.",
        "system_role": (
            "You are a friendly waiter/waitress at an English-speaking restaurant. "
            "Interact naturally as a restaurant server. Give menu suggestions, take orders, "
            "answer questions about the food. After each user response, give a very brief "
            "Indonesian note about their English (correct or suggest improvement), then continue "
            "the restaurant conversation. After 8 exchanges, give overall feedback in Indonesian."
        ),
        "opening": (
            "Welcome to The Garden Restaurant! 🌿\n\n"
            "_Waiter: Good evening! Table for one? Here's your menu. "
            "Can I get you something to drink while you look it over?_"
        ),
    },
    "3": {
        "name": "Di Bandara ✈️",
        "description": "Simulasi situasi di bandara: check-in, imigrasi, boarding.",
        "system_role": (
            "You play different airport staff roles: check-in counter, immigration officer, "
            "boarding gate. Move naturally through the airport scenario. After each user response, "
            "give a brief Indonesian note about their English, then continue the airport scene. "
            "After 8 exchanges, give overall feedback in Indonesian."
        ),
        "opening": (
            "🛫 Kamu sedang di check-in counter bandara internasional.\n\n"
            "_Staff: Good morning! Welcome to Soekarno-Hatta International Airport. "
            "May I see your passport and ticket, please?_"
        ),
    },
    "4": {
        "name": "Belanja Online/Toko 🛍️",
        "description": "Latihan tawar-menawar dan tanya produk dalam bahasa Inggris.",
        "system_role": (
            "You are a friendly shop assistant at an English-speaking store. "
            "Help the customer find products, answer questions about sizes/prices/availability. "
            "After each user response, give brief Indonesian feedback on their English, "
            "then continue the shopping conversation. After 8 exchanges, give overall feedback in Indonesian."
        ),
        "opening": (
            "🛒 Kamu masuk ke sebuah toko pakaian internasional.\n\n"
            "_Assistant: Hi there! Welcome to StyleHub. Are you looking for anything specific today, "
            "or just browsing?_"
        ),
    },
    "5": {
        "name": "Ke Dokter 🏥",
        "description": "Simulasi konsultasi medis dalam bahasa Inggris.",
        "system_role": (
            "You are a friendly English-speaking doctor. Ask about the patient's symptoms, "
            "give advice and a diagnosis in simple English. After each user response, "
            "give brief Indonesian feedback on their English, then continue the medical consultation. "
            "After 8 exchanges, give overall feedback in Indonesian."
        ),
        "opening": (
            "🏥 Kamu sedang di ruang periksa dokter.\n\n"
            "_Doctor: Hello! Come in, have a seat. I'm Dr. Johnson. "
            "So, what brings you in today? What seems to be the problem?_"
        ),
    },
}

roleplay_sessions = {}


def get_scenarios_menu():
    lines = ["🎭 *Pilih Skenario Role-play:*\n"]
    for key, s in SCENARIOS.items():
        lines.append(f"*{key}.* {s['name']}")
        lines.append(f"   _{s['description']}_\n")
    lines.append("Ketik angka *1–5* untuk mulai!")
    return "\n".join(lines)


def start_roleplay(user_id):
    roleplay_sessions[user_id] = {"state": "choosing", "scenario": None, "exchanges": 0}
    return get_scenarios_menu()


def is_in_roleplay(user_id):
    return user_id in roleplay_sessions


def is_choosing_scenario(user_id):
    s = roleplay_sessions.get(user_id)
    return s and s["state"] == "choosing"


def handle_scenario_choice(user_id, text):
    choice = text.strip()
    if choice not in SCENARIOS:
        return "Pilih angka *1* sampai *5* ya!", False, None

    scenario = SCENARIOS[choice]
    roleplay_sessions[user_id] = {
        "state": "active",
        "scenario_key": choice,
        "scenario": scenario,
        "exchanges": 0,
    }

    opening = (
        f"🎭 *{scenario['name']}*\n\n"
        f"{scenario['opening']}\n\n"
        f"_Balas dalam bahasa Inggris. Ketik /stop untuk keluar._"
    )
    return opening, True, scenario["system_role"]


def get_active_scenario_prompt(user_id):
    s = roleplay_sessions.get(user_id)
    if s and s["state"] == "active":
        return s["scenario"]["system_role"]
    return None


def increment_exchange(user_id):
    s = roleplay_sessions.get(user_id)
    if s:
        s["exchanges"] += 1
        return s["exchanges"]
    return 0


def is_session_ending(user_id):
    s = roleplay_sessions.get(user_id)
    return s and s["exchanges"] >= 8


def cancel_roleplay(user_id):
    if user_id in roleplay_sessions:
        del roleplay_sessions[user_id]
        return "Sesi role-play selesai! Mantap udah latihan tadi 💪"
    return "Tidak ada sesi role-play yang aktif."


def end_roleplay(user_id):
    cancel_roleplay(user_id)
