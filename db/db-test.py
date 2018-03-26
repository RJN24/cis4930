import psycopg2

conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='password'")
cur = conn.cursor()

cur.execute("SELECT * FROM users")
table = cur.fetchall()

print("\nThe users table contains:")
for row in table:
	print(row)

print("\nLet's pretend Bob completed level 1 with 8/10 correct")
print("Changing data in table...")
cur.execute("SELECT lv1_correct FROM users WHERE user_id = 'DrPython2018'")
user_correct = int(cur.fetchone()[0])
cur.execute("SELECT lv1_total FROM users WHERE user_id = 'DrPython2018'")
user_total = int(cur.fetchone()[0])


user_correct += 8
user_total += 10

cur.execute("UPDATE users SET lv1_correct = (%s) WHERE user_id = 'DrPython2018'", [user_correct])
conn.commit()
cur.execute("UPDATE users SET lv1_total = (%s) WHERE user_id = 'DrPython2018'", [user_total])
conn.commit()

print("Table updated.")
cur.execute("SELECT * FROM users")
table = cur.fetchall()

print("\nThe users table contains:")
for row in table:
	print(row)

result = user_correct/user_total * 10
print("Bob's average score for level 1 is: {result}/10\n".format(result = result))

cur.execute("UPDATE users SET lv1_correct = 0 WHERE user_id = 'DrPython2018'")
conn.commit()
cur.execute("UPDATE users SET lv1_total = 0 WHERE user_id = 'DrPython2018'")
conn.commit()

cur.close()
conn.close()


