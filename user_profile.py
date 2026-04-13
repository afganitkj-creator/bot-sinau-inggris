from datetime import datetime, timedelta

user_profiles = {}

LEVEL_LABELS = {
    "beginner": "Pemula",
    "intermediate": "Menengah",
    "advanced": "Lanjutan",
}


def get_profile(user_id):
    if user_id not in user_profiles:
        user_profiles[user_id] = {
            # English level (from assessment)
            "level": "beginner",
            "goals": [],
            "assessment_done": False,
            "sessions_count": 0,
            "lessons_completed": [],
            # Gamification
            "xp": 0,
            "streak": 0,
            "last_activity_date": "",
            "wrong_times": [],     # timestamps for heart refill tracking
            "premium": False,
            "premium_until": "",
            "weekly_stats": {},    # {week_key: {stat: count}}
        }
    return user_profiles[user_id]


def save_profile(user_id, profile):
    user_profiles[user_id] = profile


def get_level(user_id):
    return get_profile(user_id).get("level", "beginner")


def set_level(user_id, level):
    p = get_profile(user_id)
    p["level"] = level
    p["assessment_done"] = True


def is_assessment_done(user_id):
    return get_profile(user_id).get("assessment_done", False)


def get_level_label(user_id):
    level = get_level(user_id)
    return LEVEL_LABELS.get(level, "Pemula")


def add_score(user_id, points):
    get_profile(user_id)["xp"] = get_profile(user_id).get("xp", 0) + points


def is_premium(user_id):
    return not check_premium_expired(user_id)


def set_premium(user_id, value=True):
    profile = get_profile(user_id)
    profile["premium"] = value
    if not value:
        profile["premium_until"] = ""


def set_premium_duration(user_id, days):
    """Set premium duration untuk user."""
    profile = get_profile(user_id)
    profile["premium"] = True
    profile["premium_until"] = (datetime.now() + timedelta(days=days)).isoformat()
    save_profile(user_id, profile)


def get_premium_remaining_days(user_id):
    """Ambil sisa hari premium."""
    profile = get_profile(user_id)
    if not profile.get("premium"):
        return 0

    try:
        until = datetime.fromisoformat(profile.get("premium_until", ""))
        remaining = (until - datetime.now()).days
        return max(0, remaining)
    except Exception:
        return 0


def check_premium_expired(user_id):
    """Cek apakah premium sudah expired."""
    profile = get_profile(user_id)
    if not profile.get("premium"):
        return True

    try:
        until = datetime.fromisoformat(profile.get("premium_until", ""))
        if datetime.now() > until:
            profile["premium"] = False
            profile["premium_until"] = ""
            save_profile(user_id, profile)
            return True
        return False
    except Exception:
        return True


def get_premium_status_text(user_id):
    remaining_days = get_premium_remaining_days(user_id)
    if remaining_days <= 0:
        return "Standar (ketik /support untuk upgrade Premium)"
    return f"💎 PREMIUM aktif ({remaining_days} hari tersisa)"


def reset_profile(user_id):
    if user_id in user_profiles:
        del user_profiles[user_id]
