import psycopg2

try:
    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='password'")
    cur = conn.cursor()

    cur.execute("""SELECT * FROM users""")
    rows = cur.fetchall()

    print("\nThe table contains:")
    for line in rows:
    	print(line)

except:
    print ("I am unable to connect to the database")
