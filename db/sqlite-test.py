# Doing the same thing that db-test.py does, but using SQLite3
# This is a work in progress

import sqlite3

conn = sqlite3.connect("test.db")

cur = conn.cursor()

cur.execute('''CREATE TABLE users
             (user_id VARCHAR(12) UNIQUE NOT NULL, 
             user_pw VARCHAR(30) NOT NULL, 
             fname TEXT, 
             lname TEXT, 
             lv1_correct INT DEFAULT 0,
             lv1_total INT DEFAULT 0,
             lv2_correct INT DEFAULT 0,
             lv2_total INT DEFAULT 0,
             lv3_correct INT DEFAULT 0,
             lv3_total INT DEFAULT 0)''')
cur.execute('''INSERT INTO users (user_id, user_pw, fname, lname) VALUES (
			user_id = 'someUser',
			user_pw = 'password',
			fname = 'Bob',
			lname = 'Smith')
			''')
conn.commit()