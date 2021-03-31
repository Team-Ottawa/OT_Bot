import db


def get_thx(user):
    thx_count = db.cr.execute("SELECT thanks FROM users WHERE user_id = ?", (user.id,))
    return thx_count.fetchone()[0]
