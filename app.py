import sqlite3 as sql
from flask import Flask, request, jsonify, render_template
import uuid
import re
from fractions import Fraction

app = Flask(__name__, template_folder='static')
app.config["DEBUG"] = True

if __name__ == "__main__":
    app.run(port=3000)

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


# Route for reduction practice
@app.route("/reduction_practice.html")
def reduction_practice():
    return render_template('/reduction_practice.html')


# Route for fraction practice
@app.route("/fraction_practice.html")
def fraction_practice():
    return render_template('/fraction_practice.html')

# Route for Home Page
@app.route("/home.html")
def myHome():
    return render_template('/home.html')

# Make SQL cursor return dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Post request method for /login
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
    print(temp)
    if temp is None:
        return jsonify({
            'auth': False
        })
    elif user_id == temp["username"] and password == temp["password"]:
        return jsonify({
            'auth': True,
            'user': {
                "uid": user_id
            }
        })
    else:
        return jsonify({
            'auth': False
        })


# Post request method for /register
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

# Returns user's events
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


@app.route('/results', methods=['POST'])
def results():
    print('hello from results')
    data = request.json

    # print(data)
    for key, value in data.items():
        print(key, '\t', value)

    con = sql.connect("users.db")
    cur = con.cursor()

    if data["Level"] == "easy":
        cur.execute("SELECT lv1_correct FROM users WHERE username = ?", (data["User"],))
        correct = cur.fetchone()
        cur.execute("SELECT lv1_total FROM users WHERE username = ?", (data["User"],))
        total = cur.fetchone()
        cur.execute(
            "UPDATE users SET lv1_correct = {amt} WHERE {idf} = ?".format(amt=correct[0] + int(data["Correct"]), idf="username"),
            (data["User"],))
        con.commit()
        cur.execute("UPDATE users SET lv1_total = {amt} WHERE {idf} = ?".format(amt=total[0] + 10, idf="username"),
                    (data["User"],))
        con.commit()

    elif data["Level"] == "medium":
        cur.execute("SELECT lv2_correct FROM users WHERE username = ?", (data["User"],))
        correct = cur.fetchone()
        cur.execute("SELECT lv2_total FROM users WHERE username = ?", (data["User"],))
        total = cur.fetchone()
        cur.execute(
            "UPDATE users SET lv2_correct = {amt} WHERE {idf} = ?".format(amt=correct[0] + int(data["Correct"]), idf="username"),
            (data["User"],))
        con.commit()
        cur.execute("UPDATE users SET lv2_total = {amt} WHERE {idf} = ?".format(amt=total[0] + 10, idf="username"),
                    (data["User"],))
        con.commit()

    elif data["Level"] == "hard":
        cur.execute("SELECT lv3_correct FROM users WHERE username = ?", (data["User"],))
        correct = cur.fetchone()
        cur.execute("SELECT lv3_total FROM users WHERE username = ?", (data["User"],))
        total = cur.fetchone()
        cur.execute(
            "UPDATE users SET lv3_correct = {amt} WHERE {idf} = ?".format(amt=correct[0] + int(data["Correct"]), idf="username"),
            (data["User"],))
        con.commit()
        cur.execute("UPDATE users SET lv3_total = {amt} WHERE {idf} = ?".format(amt=total[0] + 10, idf="username"),
                    (data["User"],))
        con.commit()

    else:
        print("Unable to store results in database.")
        cur.close()
        con.close()
        return jsonify({
            'registered': False
        })


    print("Adding {amt} to user {usr} for level {lvl}".format(amt = data["Correct"], usr = data["User"], lvl = data["Level"]))

    cur.close()
    con.close()

    
    return jsonify({
        'registered': True
    })


@app.route('/home.html/fracSolver', methods=['POST'])
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


