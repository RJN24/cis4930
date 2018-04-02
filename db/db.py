# This file contains all functions in relation to our db

import sqlite3

def createDbConnection(db_file):
	try:
		connect = sqlite3.connect(db_file)
		return connect
	except Error as e:
		print(e)
	return None

def createTable():
	try:
		table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        user_id TEXT UNIQUE NOT NULL, 
								        user_pw TEXT NOT NULL,
								        lv1_correct INTEGER DEFAULT 0,
								        lv1_total INTEGER DEFAULT 0,
								        lv2_correct INTEGER DEFAULT 0,
								        lv2_total INTEGER DEFAULT 0,
								        lv3_correct INTEGER DEFAULT 0,
								        lv3_total INTEGER DEFAULT 0
                                    ); """
		cur.execute(table)
		conn.commit()
	except sqlite3.OperationalError as e:
		print(e)

def insertUser(uid, password):
	try:
		cur.execute("SELECT * FROM users WHERE user_id = ?", (uid,))
		present = cur.fetchone()
		if present is not None:
			return False
		cur.execute("INSERT INTO users (user_id, user_pw) VALUES (?, ?)", (uid, password))
		conn.commit()
	except sqlite3.IntegrityError:
		print(e)

def verifyLogin(uid, pw):
	cur.execute("SELECT * FROM users WHERE user_id = ?", (uid,))
	present = cur.fetchone()
	if present is None:
		return False
	cur.execute("SELECT user_pw FROM users WHERE user_id = ?", (uid,))
	upw = cur.fetchone()
	if pw == upw[0]:
		return True
	else:
		return False

def findUser(uid):
	cur.execute("SELECT * FROM users WHERE user_id = ?", (uid,))
	present = cur.fetchone()
	if present is None:
		return False
	return True

def getUserInfo(uid):
	cur.execute("SELECT * FROM users WHERE user_id=?", (uid,))
	show_me = cur.fetchone()
	return show_me

def deleteUsers():
	cur.execute("DROP TABLE IF EXISTS users")
	conn.commit()

def closeDb():
	cur.close()
	conn.close()

def updateUserScore(uid, lvl, result):
	if lvl == 1:
		cur.execute("SELECT lv1_correct FROM users WHERE user_id = ?", (uid,))
		correct = cur.fetchone()
		cur.execute("SELECT lv1_total FROM users WHERE user_id = ?", (uid,))
		total = cur.fetchone()
		cur.execute("UPDATE users SET lv1_correct = {amt} WHERE {idf} = ?".format(amt = correct[0]+result, idf = "user_id"), (uid,))
		conn.commit()
		cur.execute("UPDATE users SET lv1_total = {amt} WHERE {idf} = ?".format(amt = total[0]+10, idf = "user_id"), (uid,))
		conn.commit()

	elif lvl == 2:
		cur.execute("SELECT lv2_correct FROM users WHERE user_id = ?", (uid,))
		correct = cur.fetchone()
		cur.execute("SELECT lv2_total FROM users WHERE user_id = ?", (uid,))
		total = cur.fetchone()
		cur.execute("UPDATE users SET lv2_correct = {amt} WHERE {idf} = ?".format(amt = correct[0]+result, idf = "user_id"), (uid,))
		conn.commit()
		cur.execute("UPDATE users SET lv2_total = {amt} WHERE {idf} = ?".format(amt = total[0]+10, idf = "user_id"), (uid,))
		conn.commit()

	elif lvl == 3:
		cur.execute("SELECT lv3_correct FROM users WHERE user_id = ?", (uid,))
		correct = cur.fetchone()
		cur.execute("SELECT lv3_total FROM users WHERE user_id = ?", (uid,))
		total = cur.fetchone()
		cur.execute("UPDATE users SET lv3_correct = {amt} WHERE {idf} = ?".format(amt = correct[0]+result, idf = "user_id"), (uid,))
		conn.commit()
		cur.execute("UPDATE users SET lv3_total = {amt} WHERE {idf} = ?".format(amt = total[0]+10, idf = "user_id"), (uid,))
		conn.commit()

def getUserAverage(uid, lvl):
	if lvl == 1:
		cur.execute("SELECT lv1_correct FROM users WHERE user_id = ?", (uid,))
		correct = cur.fetchone()
		cur.execute("SELECT lv1_total FROM users WHERE user_id = ?", (uid,))
		total = cur.fetchone()
	elif lvl == 2:
		cur.execute("SELECT lv2_correct FROM users WHERE user_id = ?", (uid,))
		correct = cur.fetchone()
		cur.execute("SELECT lv2_total FROM users WHERE user_id = ?", (uid,))
		total = cur.fetchone()
	elif lvl == 3:
		cur.execute("SELECT lv3_correct FROM users WHERE user_id = ?", (uid,))
		correct = cur.fetchone()
		cur.execute("SELECT lv3_total FROM users WHERE user_id = ?", (uid,))
		total = cur.fetchone()
	return correct[0]/total[0]*100

# I may not need this sutff below
conn = createDbConnection("users.db")
if (conn is None):
	print("Error connecting to db")
	sys.exit()

cur = conn.cursor()