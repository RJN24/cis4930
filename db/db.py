import sqlite3
import sys
from cryptography.fernet import Fernet

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
		cipher_suite = Fernet(key)
		encode_string = str.encode(password)
		upw = cipher_suite.encrypt(encode_string)
		cur.execute("INSERT INTO users (user_id, user_pw) VALUES (?, ?)", (uid, upw))
		conn.commit()
	except sqlite3.IntegrityError:
		print(e)

def verifyLogin(uid, pw):
	cur.execute("SELECT * FROM users WHERE user_id = ?", (uid,))
	present = cur.fetchone()
	if present is None:
		return False
	cur.execute("SELECT user_pw FROM users WHERE user_id = ?", (uid,))
	one = cur.fetchone()
	decrypted = Fernet(key)
	realpw = decrypted.decrypt(one[0])
	pwstrip = str(realpw).replace("'", "")
	upw = pwstrip[1:]
	if pw == upw:
		return True
	else:
		return False

def closeDb():
	cur.execute("DROP TABLE IF EXISTS users")
	conn.commit()
	cur.close()
	conn.close()

# def updateUserScore(uid, lvl, correct):

# I may not need this sutff below
conn = createDbConnection("users.db")
if (conn is None):
	print("Error connecting to db")
	sys.exit()

cur = conn.cursor()
key = Fernet.generate_key()