import os
#from os.path import join, dirname
# from dotenv import load_dotenv
import sqlite3 as sql
from flask import Flask, request, Response, json, jsonify, render_template
import uuid
import re
from fractions import Fraction

#Environment Variables
# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

app = Flask(__name__, template_folder='static')
app.config["DEBUG"] = True


if __name__ == "__main__":
    app.run(port=5000)

#Route for /
@app.route("/")
def hello():
    return render_template('/index.html')

#Make SQL cursor return dictionary 
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#Post request method for /login GETS USER INPUT
@app.route('/login', methods=['POST'])
def login():
    email =  request.form['email'];
    password = request.form['password'];
    con = sql.connect("temp.db")
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    temp = cur.fetchone()
    cur.close()
    print(temp)
    if email == temp["email"] and password == temp["password"]:
        return jsonify({
            'auth': True,
            'user': {
                "email": email,
                "firstName": temp["firstName"],
                "lastName": temp["lastName"]
            }
        })
    else:
        return jsonify({
            'auth': False
        })

#Post request method for /register GETS USER INPUT
@app.route('/register', methods=['POST'])
def register():
    email =  request.form['emailreg'];
    password = request.form['passwordreg'];
    passwordconf = request.form['passwordconfreg'];
    con = sql.connect("temp.db", timeout=10)
    con.row_factory = dict_factory
    cur = con.cursor()
    # Uncomment the following line to create the table then comment it again after the first registration
    # cur.execute("CREATE TABLE users(id INT PRIMARY_KEY, firstName TEXT, lastName TEXT, email TEXT UNIQUE, password TEXT)")
    try:
        cur.execute("SELECT * FROM users WHERE email = " + email + ";")
        temp = cur.fetchone()
        print(temp)
    except:
        print("User not found")
    if password == passwordconf:
        uid = str(uuid.uuid4())
        firstName = 'Fadi'
        lastName = 'Bitar'
        cur.execute("""INSERT INTO Users(id, firstName, lastName, email, password) VALUES (?,?,?,?,?);""", (uid, firstName, lastName, email, password))
        con.commit()
        cur.close()
        con.close()
        return jsonify({
            'registered': True
        })

#Returns user's events RETURNS TO SCREEN
@app.route('/getEvents', methods=['GET'])
def home():
    #Print json from get request
    print(request.args)
    #Save the email to a variable
    email =  request.args.get("temp");
    print(email)
    con = sql.connect("temp.db")
    con.row_factory = dict_factory
    cur = con.cursor()
    # Uncomment the following line to create the table then comment it again after the first registration
    # cur.execute("CREATE TABLE event(id INT PRIMARY_KEY, email TEXT, eventName TEXT, eventTime TEXT, eventUrl TEXT)")
    uid = str(uuid.uuid4())
    # Uncomment to make a test Event
    # cur.execute("""INSERT INTO event(id, email, eventName, eventTime, eventUrl) VALUES(?,?,?,?,?)""",(uid, email, 'Event Name 3', 'Date 3', 'bullsync3.com'))
    cur.execute("SELECT * FROM event WHERE email=?", (email,))
    eventdata = cur.fetchall()
    print(eventdata)
    con.commit()
    cur.close()
    con.close()
    return jsonify({
        'events': eventdata
    });

# GETS USER INPUT
@app.route('/newEvent', methods=['POST'])
def newEvent():
    email = request.form['email']
    eventName =  request.form['eventName'];
    eventTime = request.form['eventTime'];
    eventUrl = request.form['eventUrl'];
    con = sql.connect("temp.db", timeout=10)
    con.row_factory = dict_factory
    cur = con.cursor()
    # Uncomment the following line to create the table then comment it again after the first registration
    # cur.execute("CREATE TABLE event(id INT PRIMARY_KEY, email TEXT, eventName TEXT, eventTime TEXT, eventUrl TEXT)")
    uid = str(uuid.uuid4())
    cur.execute("""INSERT INTO event(id, email, eventName, eventTime, eventUrl) VALUES (?,?,?,?,?);""", (uid, email, eventName, eventTime, eventUrl))
    con.commit()
    cur.close()
    con.close()
    return jsonify({
        'newEventStatus': True
    })

@app.route('/fracSolver', methods=['POST'])
def fractionSolver():
    fraction = request.form['frac']
    patt2 = r'(-?\d+)\/?(-?\d+)?\s+([*\-+/])\s+(-?\d+)\/?(-?\d+)?'
    m = re.search(patt2, fraction)

    try:
        if m.group(2) != None and m.group(5) != None:
            nue1 = int(m.group(1))
            den1 = int(m.group(2))
            nue2 = int(m.group(4))
            den2 = int(m.group(5))

        if m.group(2) == None and m.group(5) == None:
            nue1 = int(m.group(1))
            den1 = 1
            nue2 = int(m.group(4))
            den2 = 1

        if m.group(2) == None and m.group(5) != None:
            nue1 = int(m.group(1))
            den1 = 1
            nue2 = int(m.group(4))
            den2 = int(m.group(5))

        if m.group(5) == None and m.group(2) != None:
            nue1 = int(m.group(1))
            den1 = int(m.group(2))
            nue2 = int(m.group(4))
            den2 = 1

        X = Fraction(nue1, den1)
        Y = Fraction(nue2, den2)

        print(m.group(3))

        if m.group(3) == '+':
            R = X + Y

        if m.group(3) == '-':
            R = X - Y

        if m.group(3) == '*':
            R = X * Y

        if m.group(3) == '/':
            R = X / Y

        print("Soln is: ")
        print(R)

    except ZeroDivisionError:
        R = "Sorry, 0 can not be part of the denominator. Please retry"

    except:
        R = "Sorry, you have entered an incorrect string. Please retry"

    return jsonify({
        'fraction': R.__str__()})