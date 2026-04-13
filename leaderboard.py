
leaderboard_data = {}  # {user_id: {"name": str, "xp": int}}


def update_leaderboard(user_id, xp, display_name):
    leaderboard_data[user_id] = {"name": display_name, "xp": xp}


def get_top(limit=10):
    return sorted(leaderboard_data.items(), key=lambda x: x[1]["xp"], reverse=True)[:limit]


def get_user_rank(user_id):
    ranked = sorted(leaderboard_data.items(), key=lambda x: x[1]["xp"], reverse=True)
    for i, (uid, _) in enumerate(ranked):
        if uid == user_id:
            return i + 1
    return None


def format_leaderboard(user_id=None):
    top = get_top()
    if not top:
        return (
            "🏆 *Leaderboard*\n\n"
            "Belum ada pemain. Jadilah yang pertama!\n"
            "Kumpulkan XP dengan belajar setiap hari!"
        )

    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    lines = ["🏆 *Top Learners — English Mas/Mbak*\n"]
    for i, (uid, data) in enumerate(top, 1):
        medal = medals.get(i, f"{i}.")
        marker = " ◀ *kamu*" if uid == user_id else ""
        lines.append(f"{medal} {data['name']} — *{data['xp']} XP*{marker}")

    if user_id:
        rank = get_user_rank(user_id)
        if rank and rank > 10:
            xp = leaderboard_data.get(user_id, {}).get("xp", 0)
            lines.append(f"\n_Posisi kamu: #{rank} — {xp} XP_")

    lines.append("\n_Update setiap sesi belajar_ 🔄")
    return "\n".join(lines)
