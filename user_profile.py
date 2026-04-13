
user_profiles = {}

LEVEL_LABELS = {
    "beginner": "Pemula",
    "intermediate": "Menengah",
    "advanced": "Lanjutan",
}

def get_profile(user_id):
    if user_id not in user_profiles:
        user_profiles[user_id] = {
            "level": "beginner",
            "goals": [],
            "assessment_done": False,
            "total_score": 0,
            "sessions_count": 0,
            "lessons_completed": [],
        }
    return user_profiles[user_id]

def get_level(user_id):
    return get_profile(user_id).get("level", "beginner")

def set_level(user_id, level):
    p = get_profile(user_id)
    p["level"] = level
    p["assessment_done"] = True

def is_assessment_done(user_id):
    return get_profile(user_id).get("assessment_done", False)

def add_score(user_id, points):
    get_profile(user_id)["total_score"] += points

def reset_profile(user_id):
    if user_id in user_profiles:
        del user_profiles[user_id]

def get_level_label(user_id):
    level = get_level(user_id)
    return LEVEL_LABELS.get(level, "Pemula")
