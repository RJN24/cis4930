# SQLite3 stores a db on disk that persists through sessions
# This program demonstrates creating a table, inserting a user, querying/updating, and dropping a table

import sqlite3

# Connect to db, this creates a new db if it does not already exist
conn = sqlite3.connect("test.db")
cur = conn.cursor()

#------------------------------------------ CREATE TABLE ---------------------------------------------------------
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



#------------------------------------------ INSERT INTO TABLE ---------------------------------------------------------
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


##------------------------------------------ QUERY/UPDATE ---------------------------------------------------------
cur.execute("SELECT * FROM users")
print(cur.fetchall())

print("\nBob completed level 1 and scored 8/10... updating table")
cur.execute("SELECT lv1_correct FROM users WHERE user_id = ?", (uid,))
correct = cur.fetchone()
cur.execute("SELECT lv1_total FROM users WHERE user_id = ?", (uid,))
total = cur.fetchone()

cur.execute("UPDATE users SET lv1_correct = {amt} WHERE {idf} = ?".format(amt = correct[0]+8, idf = "user_id"), (uid,))
conn.commit()

cur.execute("UPDATE users SET lv1_total = {amt} WHERE {idf} = ?".format(amt = total[0]+10, idf = "user_id"), (uid,))
conn.commit()

cur.execute("SELECT * FROM users")
print(cur.fetchall())

cur.execute("SELECT lv1_correct, lv1_total FROM users WHERE user_id = ?", (uid,))
res = cur.fetchall()
av = round(res[0][0]/res[0][1], 2)
print("\nBob's average after scoring 8/10 is {}%".format(av*100))

print("\nHe completed level 1 again and this time scored a perfect score 10/10")
cur.execute("SELECT lv1_correct FROM users WHERE user_id = ?", (uid,))
correct = cur.fetchone()
cur.execute("SELECT lv1_total FROM users WHERE user_id = ?", (uid,))
total = cur.fetchone()

cur.execute("UPDATE users SET lv1_correct = {amt} WHERE {idf} = ?".format(amt = correct[0]+10, idf = "user_id"), (uid,))
conn.commit()

cur.execute("UPDATE users SET lv1_total = {amt} WHERE {idf} = ?".format(amt = total[0]+10, idf = "user_id"), (uid,))
conn.commit()

cur.execute("SELECT * FROM users")
print(cur.fetchall())

cur.execute("SELECT lv1_correct, lv1_total FROM users WHERE user_id = ?", (uid,))
res = cur.fetchall()
av = round(res[0][0]/res[0][1], 2)
print("\nBob's average after scoring 10/10 is {}%".format(av*100))

print("\nHe completed level 1 one last time and this time scored 3/10... oops!")
cur.execute("SELECT lv1_correct FROM users WHERE user_id = ?", (uid,))
correct = cur.fetchone()
cur.execute("SELECT lv1_total FROM users WHERE user_id = ?", (uid,))
total = cur.fetchone()

cur.execute("UPDATE users SET lv1_correct = {amt} WHERE {idf} = ?".format(amt = correct[0]+3, idf = "user_id"), (uid,))
conn.commit()

cur.execute("UPDATE users SET lv1_total = {amt} WHERE {idf} = ?".format(amt = total[0]+10, idf = "user_id"), (uid,))
conn.commit()

cur.execute("SELECT * FROM users")
print(cur.fetchall())

cur.execute("SELECT lv1_correct, lv1_total FROM users WHERE user_id = ?", (uid,))
res = cur.fetchall()
av = round(res[0][0]/res[0][1], 2)
print("\nBob's average after scoring 3/10 is {}%".format(av*100))


#------------------------------------------ DROP TABLE ---------------------------------------------------------
cur.execute("DROP TABLE users")

cur.close()
conn.close()
