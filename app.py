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


# @app.route("/results.html")
# def results():
#     return render_template('/results.html')

@app.route("/results_chart.html")
def results():
    return render_template('/results_chart.html')

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


@app.route('/post_results', methods=['POST'])
def post_results():
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


@app.route('/get_stats', methods=['GET','POST'])
def get_stats():
    # Parse JSON to get logged in user
    # Create new connection to SQLite3 db
    # Pull level data for logged in user
    data = request.json
    user = data['User']
    con = sql.connect('users.db')
    cur = con.cursor()
    cur.execute("SELECT lv1_correct, lv1_total, lv2_correct, lv2_total, lv3_correct, lv3_total FROM users WHERE username=?", (user,))
    user_info = cur.fetchall()
    print(user_info)

    # Get users average for level 1
    lv1_correct = user_info[0][0]
    print(lv1_correct)
    lv1_total = user_info[0][1]
    if lv1_total == 0:
        lv1_average = 0
    else:
        lv1_average = int(lv1_correct)/int(lv1_total)
    print(lv1_average)

    # Get global average for level 1
    cur.execute("SELECT lv1_correct FROM users")
    get_all_lv1_correct = cur.fetchall()
    print(get_all_lv1_correct)
    lv1_total_correct = 0
    for i in range(len(get_all_lv1_correct)):
        lv1_total_correct += get_all_lv1_correct[i][0]
    print(lv1_total_correct)
    cur.execute("SELECT lv1_total FROM users")
    get_all_lv1_total = cur.fetchall()
    lv1_total_total = 0
    for i in range(len(get_all_lv1_total)):
        lv1_total_total += get_all_lv1_total[i][0]
    print("Printing total for level 1")
    print(lv1_total_total)
    if lv1_total_total == 0:
        lv1_total_average = 0
    else:
        lv1_total_average = int(lv1_total_correct)/int(lv1_total_total)
    print(lv1_total_average)

    # Get user average for level 2
    lv2_correct = user_info[0][2]
    lv2_total = user_info[0][3]
    if lv2_total == 0:
        lv2_average = 0
    else:
        lv2_average = int(lv2_correct) / int(lv2_total)

    # Get global average for level 2
    cur.execute("SELECT lv2_correct FROM users")
    get_all_lv2_correct = cur.fetchall()
    print(get_all_lv2_correct)
    lv2_total_correct = 0
    for i in range(len(get_all_lv2_correct)):
        lv2_total_correct += get_all_lv2_correct[i][0]
    print(lv2_total_correct)
    cur.execute("SELECT lv2_total FROM users")
    get_all_lv2_total = cur.fetchall()
    lv2_total_total = 0
    for i in range(len(get_all_lv2_total)):
        lv2_total_total += get_all_lv2_total[i][0]
    if lv2_total_total == 0:
        lv2_total_average = 0
    else:
        lv2_total_average = int(lv2_total_correct)/int(lv2_total_total)
    print(lv2_total_average)

    # Get user average for level 3
    lv3_correct = user_info[0][4]
    lv3_total = user_info[0][5]
    if lv3_total == 0:
        lv3_average = 0
    else:
        lv3_average = int(lv3_correct) / int(lv3_total)

    # Get global average for level 3
    cur.execute("SELECT lv3_correct FROM users")
    get_all_lv3_correct = cur.fetchall()
    print(get_all_lv3_correct)
    lv3_total_correct = 0
    for i in range(len(get_all_lv3_correct)):
        lv3_total_correct += get_all_lv3_correct[i][0]
    print(lv3_total_correct)
    cur.execute("SELECT lv3_total FROM users")
    get_all_lv3_total = cur.fetchall()
    lv3_total_total = 0
    for i in range(len(get_all_lv3_total)):
        lv3_total_total += get_all_lv3_total[i][0]
    if lv3_total_total == 0:
        lv3_total_average = 0
    else:
        lv3_total_average = int(lv3_total_correct)/int(lv3_total_total)
    print(lv3_total_average)

    # Close connections
    cur.close()
    con.close()

    # Return JSON data
    return jsonify({
        'user_level_1_average': lv1_average,
        'user_level_2_average': lv2_average,
        'user_level_3_average': lv3_average,
        'all_level_1_average': lv1_total_average,
        'all_level_2_average': lv2_total_average,
        'all_level_3_average': lv3_total_average
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
