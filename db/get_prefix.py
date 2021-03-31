import db


def get_prefix(user):
    prefix = db.cr.execute("SELECT prefix FROM users WHERE user_id = ?", (user.id,))
    return prefix.fetchone()[0]
