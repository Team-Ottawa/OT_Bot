import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database='ottawa'
)


cr = db.cursor(buffered=True)


cr.execute("""
CREATE TABLE IF NOT EXISTS users(
id BIGINT(30) PRIMARY KEY,
name VARCHAR(30) DEFAULT NULL,
prefix TEXT,
thanks INT DEFAULT 0,
xp INT(255) DEFAULT 0,
description VARCHAR(101)
)
""")


cr.execute("""
CREATE TABLE IF NOT EXISTS vip(
id BIGINT(30) PRIMARY KEY,
timer BIGINT(255)
)
""")


cr.execute("""
CREATE TABLE IF NOT EXISTS codes(
id VARCHAR(6) PRIMARY KEY,
title VARCHAR(30) NOT NULL,
description VARCHAR(255) NOT NULL,
type TEXT NOT NULL,
author BIGINT(30) NOT NULL,
code LONGTEXT NOT NULL 
)
""")


def get_prefix(user):
    cr.execute("SELECT prefix FROM users WHERE id = %s", (user.id,))
    return cr.fetchone()[0]


def get_thanks(user):
    cr.execute("SELECT thanks FROM users WHERE id = %s", (user.id,))
    return cr.fetchone()[0]


def get_xp(user):
    cr.execute("SELECT xp FROM users WHERE id = %s", (user.id,))
    return cr.fetchone()[0]


def get_description(user):
    cr.execute("SELECT description FROM users WHERE id = %s", (user.id,))
    return cr.fetchone()[0]


def add_thanks(user, thanks_count=1):
    cr.execute('UPDATE users SET xp = %s WHERE id = %s', (get_thanks(user)+thanks_count, user.id))
    db.commit()


def set_description(user, new_title):
    cr.execute('UPDATE users SET description = %s WHERE id = %s', (new_title, user.id))
    db.commit()


def add_xp(user, xp_count=1):
    cr.execute('UPDATE users SET xp = %s WHERE id = %s', (get_xp(user)+xp_count, user.id))
    db.commit()


def set_prefix(user, prefix):
    cr.execute('UPDATE users SET prefix = %s WHERE id = %s', (prefix, user.id))
    db.commit()


def add_user(user):
    try:
        cr.execute('INSERT INTO users(id, name) VALUES(%s, %s)', (user.id, user.name))
        db.commit()
    except mysql.connector.errors.IntegrityError:
        pass


def get_vip(user):
    cr.execute("SELECT timer FROM vip WHERE id = %s", (user.id,))
    return cr.fetchone()[0]


def get_all_vip():
    cr.execute('SELECT * FROM vip')
    return cr.fetchall()


def set_vip(user, time: int):
    try:
        cr.execute('INSERT INTO vip(id, timer) VALUES(%s, %s)', (user.id, time))
        db.commit()
    except mysql.connector.errors.IntegrityError:
        cr.execute('UPDATE vip SET timer = %s WHERE id = %s', (get_vip(user)+time, user.id))


def remove_vip(user_id):
    cr.execute('UPDATE vip SET timer = %s WHERE id = %s', (0, user_id))
    db.commit()


def edit_vip(user, num=1):
    cr.execute('UPDATE vip SET timer = %s WHERE id = %s', (get_vip(user)-num, user.id))
    db.commit()


def add_code(id, title, description, type, author, copyrights, code):
    cr.execute('INSERT INTO codes(id, title, description, type, author, copyrights, code) VALUES(%s, %s, %s, %s, %s, %s, %s)', (
        id, title, description, type, author, copyrights, code
    ))
    db.commit()


def get_code(id):
    cr.execute('SELECT * FROM codes WHERE id = %s', (id,))
    return cr.fetchone()
