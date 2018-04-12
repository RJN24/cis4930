import sqlite3 as sql
from flask import Flask, request, jsonify, render_template
import uuid
import re
from fractions import Fraction

app = Flask(__name__, template_folder='static')
app.config["DEBUG"] = True

if __name__ == "__main__":
    app.run(port=5000)

USERS_TABLE = """ CREATE TABLE IF NOT EXISTS users (
                                id TEXT PRIMARY KEY,
                                username TEXT UNIQUE NOT NULL, 
                                password TEXT NOT NULL,
                                lv1_correct INTEGER DEFAULT 0,
                                lv1_total INTEGER DEFAULT 0,
                                lv2_correct INTEGER DEFAULT 0,
                                lv2_total INTEGER DEFAULT 0,
                                lv3_correct INTEGER DEFAULT 0,
                                lv3_total INTEGER DEFAULT 0); """

EVENT_TABLE = """ CREATE TABLE IF NOT EXISTS event(
                                id TEXT PRIMARY_KEY, 
                                username TEXT, 
                                eventName TEXT, 
                                eventTime TEXT, 
                                eventUrl TEXT); """


# Route for /
@app.route("/")
def hello():
    return render_template('/index.html')


# Make SQL cursor return dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Post request method for /login GETS USER INPUT
@app.route('/login', methods=['POST'])
def login():
    user_id = request.form['username'];
    password = request.form['password'];
    con = sql.connect("users.db")
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(USERS_TABLE)
    cur.execute("SELECT * FROM users WHERE username=?", (user_id,))
    temp = cur.fetchone()
    cur.close()
    print("Trying to login as " + user_id)
    if temp is None:
        return jsonify({
            'auth': False
        })
    elif user_id == temp["username"] and password == temp["password"]:
        return jsonify({
            'auth': True,
            'user': {
                "username": user_id
            }
        })
    else:
        return jsonify({
            'auth': False
        })


# Post request method for /register GETS USER INPUT
@app.route('/register', methods=['POST'])
def register():
    try:
        print(request.form)
        user_id = request.form['usernamereg'];
        password = request.form['passwordreg'];
        passwordconf = request.form['passwordconfreg'];
        con = sql.connect("users.db", timeout=10)
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute(USERS_TABLE)
        cur.execute("SELECT * FROM users WHERE username = ?", (user_id,))
        temp = cur.fetchone()
        print(temp)
        if temp is not None:
            print("Registration failed: {} already taken.".format(user_id))
            cur.close()
            con.close()
            return jsonify({
                'registered': False
            })
        if password == passwordconf:
            uid = str(uuid.uuid4())
            cur.execute("INSERT INTO users(id, username, password) VALUES (?,?,?)", (uid, user_id, password))
            con.commit()
            cur.close()
            con.close()
            return jsonify({
                'registered': True
            })
        else:
            cur.close()
            con.close()
            return jsonify({
                'registered': False
            })
    except KeyError as e:
        print(e)


# Returns user's events RETURNS TO SCREEN
@app.route('/getEvents', methods=['GET'])
def home():
    # Print json from get request
    print(request.args)
    user_id = request.args.get("temp");
    print(user_id)
    con = sql.connect("users.db")
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(EVENT_TABLE)
    cur.execute("SELECT * FROM event WHERE username=?", (user_id,))
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
    user_id = request.form['username']
    eventName = request.form['eventName'];
    eventTime = request.form['eventTime'];
    eventUrl = request.form['eventUrl'];
    con = sql.connect("users.db", timeout=10)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute(EVENT_TABLE)
    uid = str(uuid.uuid4())
    cur.execute("""INSERT INTO event(id, username, eventName, eventTime, eventUrl) VALUES (?,?,?,?,?);""",
                (uid, user_id, eventName, eventTime, eventUrl))
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
        if m.group(2) is not None and m.group(5) is not None:
            nue1 = int(m.group(1))
            den1 = int(m.group(2))
            nue2 = int(m.group(4))
            den2 = int(m.group(5))

        if m.group(2) is None and m.group(5) is None:
            nue1 = int(m.group(1))
            den1 = 1
            nue2 = int(m.group(4))
            den2 = 1

        if m.group(2) is None and m.group(5) is not None:
            nue1 = int(m.group(1))
            den1 = 1
            nue2 = int(m.group(4))
            den2 = int(m.group(5))

        if m.group(5) is None and m.group(2) is not None:
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

        print("Solution is: ")
        print(R)

    except ZeroDivisionError:
        R = "Sorry, cannot divide by 0. Please retry."

    except:
        R = "Sorry, you have entered an incorrect input. Please retry."

    return jsonify({
        'fraction': R.__str__()})

# @app.route('/getAverage', methods=['GET'])
# def getUserAverage
