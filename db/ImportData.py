import sqlite3
import mysql.connector

MySqlDatabase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database='ottawa'
)


SqliteDatabase = sqlite3.connect('db.sqlite')


MySqlCursor = MySqlDatabase.cursor(buffered=True)

SqliteCursor = SqliteDatabase.cursor()


# MySqlCursor.execute("""
# CREATE TABLE IF NOT EXISTS users(
# id BIGINT(30) PRIMARY KEY,
# name VARCHAR(30) DEFAULT NULL,
# prefix TEXT,
# thanks INT DEFAULT 0,
# xp INT(255) DEFAULT 0,
# description VARCHAR(101)
# )
# """)
#
#
# MySqlCursor.execute("""
# CREATE TABLE IF NOT EXISTS vip(
# id BIGINT(30) NOT NULL,
# timer INT(255),
# constraint vip_fk FOREIGN KEY(id) REFERENCES users(id)
# )
# """)
#
#
# MySqlCursor.execute("""
# CREATE TABLE codes(
# id VARCHAR(6) PRIMARY KEY,
# title VARCHAR(30) NOT NULL,
# description VARCHAR(255) NOT NULL,
# type TEXT NOT NULL,
# author BIGINT(30) NOT NULL,
# code LONGTEXT NOT NULL
# )
# """)


def get_users():
    return SqliteCursor.execute('SELECT * FROM users').fetchall()


def get_vip_users():
    return SqliteCursor.execute('SELECT * FROM vip').fetchall()

#
# for i in get_users():
#     MySqlCursor.execute('INSERT INTO users(id, name, prefix, thanks, xp, description) VALUES(%s, %s, %s, %s, %s, %s)',
#                         (i[0], i[1], i[2], i[3], i[4], i[5]))
#     MySqlDatabase.commit()


for i in get_vip_users():
    MySqlCursor.execute('INSERT INTO vip(id, timer) VALUES(%s, %s)', (i[0], i[2]))
    MySqlDatabase.commit()
