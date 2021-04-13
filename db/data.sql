USE ottawa;


CREATE TABLE users(
id BIGINT(30) PRIMARY KEY,
name VARCHAR(30) DEFAULT NULL,
prefix TEXT,
thanks INT DEFAULT 0,
xp INT(255) DEFAULT 0,
description VARCHAR(101)
)


CREATE TABLE vip(
id BIGINT(30) NOT NULL,
timer INT(255),
constraint vip_fk FOREIGN KEY(id) REFERENCES users(id)
)


INSERT INTO users(id, name, prefix, thx, xp, description) VALUES()

ALTER TABLE users MODIFY test TEXT DEFAULT 'test';

DESCRIBE


CREATE TABLE codes(
id VARCHAR(6) PRIMARY KEY,
title VARCHAR(30) NOT NULL,
description VARCHAR(255) NOT NULL,
type TEXT NOT NULL,
author BIGINT(30) NOT NULL,
code LONGTEXT NOT NULL
)
