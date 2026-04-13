
import time
from datetime import date, timedelta

LEVELS = [
    (0,    "🥚 Newbie"),
    (100,  "🐣 Beginner"),
    (300,  "🌱 Explorer"),
    (600,  "📖 Learner"),
    (1000, "⭐ Intermediate"),
    (1800, "🏆 Advanced"),
    (3000, "💎 Expert"),
    (5000, "👑 Master"),
]

MAX_HEARTS = 5
HEART_REFILL_SECS = 7200  # 1 heart every 2 hours

XP_REWARDS = {
    "vocab_correct":       10,
    "grammar_correct":     15,
    "assessment_complete": 50,
    "story_correct":       20,
    "story_complete":      30,
    "roleplay_exchange":    5,
    "daily_streak":        25,
}

WEEKLY_CHALLENGES = [
    ("📝 Jawab 20 flashcard kosakata", "vocab_answers", 20),
    ("📚 Selesaikan 5 topik Grammar Coach", "grammar_done", 5),
    ("💬 Latihan roleplay 3 kali sesi", "roleplay_sessions", 3),
    ("📖 Baca 2 cerita English Stories", "stories_read", 2),
    ("🔥 Capai streak 5 hari berturut-turut", "streak_peak", 5),
    ("🎯 Raih 200 XP minggu ini", "weekly_xp", 200),
]


# ─── Level helpers ────────────────────────────────────────────────────────────

def get_level_info(xp):
    level_num, level_name = 0, LEVELS[0][1]
    next_xp = LEVELS[1][0]
    for i, (min_xp, name) in enumerate(LEVELS):
        if xp >= min_xp:
            level_num = i + 1
            level_name = name
            next_xp = LEVELS[i + 1][0] if i + 1 < len(LEVELS) else None
    return level_num, level_name, next_xp


def get_xp_bar(xp):
    level_num, level_name, next_xp = get_level_info(xp)
    if next_xp is None:
        return f"{level_name} _(MAX LEVEL!)_ 🎉"
    prev_xp = LEVELS[level_num - 1][0] if level_num > 1 else 0
    progress = xp - prev_xp
    needed = next_xp - prev_xp
    filled = int((progress / needed) * 10) if needed > 0 else 10
    bar = "🟦" * filled + "⬜" * (10 - filled)
    return f"{level_name}\n{bar} _{xp}/{next_xp} XP_"


# ─── XP system ────────────────────────────────────────────────────────────────

def add_xp(user_id, reward_key, display_name=None):
    """Add XP. Returns (xp_gained, new_total, leveled_up, new_level_name)."""
    from user_profile import get_profile
    from leaderboard import update_leaderboard

    points = XP_REWARDS.get(reward_key, 0)
    if points == 0:
        return 0, 0, False, None

    profile = get_profile(user_id)
    old_xp = profile.get("xp", 0)
    old_level, _, _ = get_level_info(old_xp)

    new_xp = old_xp + points
    profile["xp"] = new_xp

    # Weekly XP tracker
    _add_weekly_xp(profile, points)

    new_level, new_name, _ = get_level_info(new_xp)
    leveled_up = new_level > old_level

    if display_name:
        update_leaderboard(user_id, new_xp, display_name)

    return points, new_xp, leveled_up, (new_name if leveled_up else None)


def _add_weekly_xp(profile, points):
    week_key = _current_week_key()
    stats = profile.setdefault("weekly_stats", {})
    week = stats.setdefault(week_key, {})
    week["weekly_xp"] = week.get("weekly_xp", 0) + points


def xp_notification(xp_gained, new_xp, leveled_up, level_name):
    """Return a short XP notification string to append to messages."""
    if xp_gained <= 0:
        return ""
    msg = f"\n\n✨ *+{xp_gained} XP!* (Total: {new_xp} XP)"
    if leveled_up:
        msg += f"\n🎉 *Level Up! → {level_name}*"
    return msg


# ─── Daily streak ─────────────────────────────────────────────────────────────

def check_and_update_streak(user_id, display_name=None):
    """Returns (streak, is_new_day, bonus_xp, leveled_up, level_name)."""
    from user_profile import get_profile
    from leaderboard import update_leaderboard

    profile = get_profile(user_id)
    today = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    last_date = profile.get("last_activity_date", "")

    if last_date == today:
        return profile.get("streak", 1), False, 0, False, None

    # New day
    if last_date == yesterday:
        profile["streak"] = profile.get("streak", 0) + 1
    else:
        profile["streak"] = 1

    profile["last_activity_date"] = today

    # Track streak peak for weekly challenge
    week_key = _current_week_key()
    stats = profile.setdefault("weekly_stats", {})
    week = stats.setdefault(week_key, {})
    week["streak_peak"] = max(week.get("streak_peak", 0), profile["streak"])

    # Bonus XP
    bonus = XP_REWARDS["daily_streak"]
    old_xp = profile.get("xp", 0)
    _, old_lvl_num, _ = get_level_info(old_xp), *get_level_info(old_xp)  # noqa
    old_level_num, _, _ = get_level_info(old_xp)
    new_xp = old_xp + bonus
    profile["xp"] = new_xp
    new_level_num, new_name, _ = get_level_info(new_xp)
    leveled_up = new_level_num > old_level_num

    if display_name:
        update_leaderboard(user_id, new_xp, display_name)

    return profile["streak"], True, bonus, leveled_up, (new_name if leveled_up else None)


# ─── Hearts ──────────────────────────────────────────────────────────────────

def get_hearts(user_id):
    from user_profile import get_profile
    profile = get_profile(user_id)
    if profile.get("premium", False):
        return MAX_HEARTS

    wrong_times = profile.get("wrong_times", [])
    now = time.time()
    # Keep only wrongs that haven't fully refilled yet
    active_wrongs = [t for t in wrong_times if now - t < HEART_REFILL_SECS]
    profile["wrong_times"] = active_wrongs
    return max(0, MAX_HEARTS - len(active_wrongs))


def lose_heart(user_id):
    from user_profile import get_profile
    profile = get_profile(user_id)
    if profile.get("premium", False):
        return MAX_HEARTS
    wrong_times = profile.get("wrong_times", [])
    wrong_times.append(time.time())
    profile["wrong_times"] = wrong_times
    return get_hearts(user_id)


def hearts_display(user_id):
    from user_profile import get_profile
    if get_profile(user_id).get("premium", False):
        return "💛💛💛💛💛 _(Premium ∞)_"
    h = get_hearts(user_id)
    return "❤️" * h + "🖤" * (MAX_HEARTS - h)


def refill_time_str(user_id):
    from user_profile import get_profile
    wrong_times = get_profile(user_id).get("wrong_times", [])
    if not wrong_times:
        return ""
    oldest = min(wrong_times)
    remaining = HEART_REFILL_SECS - (time.time() - oldest)
    if remaining <= 0:
        return ""
    mins = int(remaining // 60)
    return f"{mins} menit"


# ─── Weekly Challenge ─────────────────────────────────────────────────────────

def _current_week_key():
    iso = date.today().isocalendar()
    return f"{iso[0]}-W{iso[1]:02d}"


def get_weekly_challenge():
    iso = date.today().isocalendar()
    idx = iso[1] % len(WEEKLY_CHALLENGES)
    label, key, target = WEEKLY_CHALLENGES[idx]
    return label, key, target


def get_weekly_progress(user_id):
    from user_profile import get_profile
    profile = get_profile(user_id)
    week_key = _current_week_key()
    stats = profile.get("weekly_stats", {}).get(week_key, {})
    label, key, target = get_weekly_challenge()
    progress = stats.get(key, 0)
    return label, progress, target


def increment_weekly_stat(user_id, stat_key, amount=1):
    from user_profile import get_profile
    profile = get_profile(user_id)
    week_key = _current_week_key()
    stats = profile.setdefault("weekly_stats", {})
    week = stats.setdefault(week_key, {})
    week[stat_key] = week.get(stat_key, 0) + amount


def format_weekly_challenge(user_id):
    label, progress, target = get_weekly_progress(user_id)
    pct = min(progress / target, 1.0)
    filled = int(pct * 10)
    bar = "🟩" * filled + "⬜" * (10 - filled)
    status = "✅ Selesai!" if progress >= target else f"{progress}/{target}"
    return f"{label}\n{bar} {status}"
