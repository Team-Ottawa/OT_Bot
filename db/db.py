import sqlite3

db = sqlite3.connect("db/db.sqlite")

cr = db.cursor()

cr.execute("""
CREATE TABLE IF NOT EXISTS users(
user_id INTEGER PRIMARY KEY,
user_name TEXT DEFAULT NULL, 
prefix TEXT DEFAULT '!', 
thanks INTEGER DEFAULT 0, 
xp INTEGER DEFAULT 0,
vip_time INTEGER DEFAULT 0
)""")


def get_xp(user):
    xp_count = cr.execute("SELECT xp FROM users WHERE user_id = ?", (user.id,))
    return xp_count.fetchone()[0]


def get_description(user):
    description = cr.execute("SELECT description FROM users WHERE user_id = ?", (user.id,))
    return description.fetchone()[0]


def get_vip(user):
    vip_time = cr.execute("SELECT vip_time FROM vip WHERE user_id = ?", (user.id,))
    return vip_time.fetchone()[0]


def get_thx(user):
    thx_count = cr.execute("SELECT thanks FROM users WHERE user_id = ?", (user.id,))
    return thx_count.fetchone()[0]


def get_prefix(user):
    prefix = db.execute("SELECT prefix FROM users WHERE user_id = ?", (user.id,))
    return prefix.fetchone()[0]




