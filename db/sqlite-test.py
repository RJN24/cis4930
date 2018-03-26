# Doing the same thing that db-test.py does, but using SQLite3

import sqlite3

conn = sqlite3.connect("test.db")

cur = conn.cursor()

cur.execute('''CREATE TABLE users
             (user_id VARCHAR(12) UNIQUE NOT NULL, 
             user_pw VARCHAR(30) NOT NULL, 
             symbol text, 
             qty real, 
             price real)''')