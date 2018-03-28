# Doing the same thing that db-test.py does, but using SQLite3
# This is a work in progress

import sqlite3

conn = sqlite3.connect("test.db")

cur = conn.cursor()
try:
	cur.execute('''CREATE TABLE users
	             (id INTEGER PRIMARY KEY,
	             user_id TEXT UNIQUE NOT NULL, 
	             user_pw TEXT NOT NULL, 
	             fname TEXT, 
	             lname TEXT, 
	             lv1_correct INTEGER DEFAULT 0,
	             lv1_total INTEGER DEFAULT 0,
	             lv2_correct INTEGER DEFAULT 0,
	             lv2_total INTEGER DEFAULT 0,
	             lv3_correct INTEGER DEFAULT 0,
	             lv3_total INTEGER DEFAULT 0)''')
except sqlite3.OperationalError as e:
	print(e)
	pass

cur.execute('''SELECT * FROM users''')
all_rows = cur.fetchall()
print(all_rows)

uid = "BobUser"
pw = "password"
first = "Bob"
last = "smith"

try:
	cur.execute('''INSERT INTO users (user_id, user_pw, fname, lname) VALUES (
			?,
			?,
			?,
			?)
			''', (uid, pw, first, last))
except sqlite3.IntegrityError as e:
	print(e)

conn.commit()

cur.close()
conn.close()