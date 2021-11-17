import os
from string import ascii_uppercase
import itertools
import csv

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Limits the size of input
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = '.csv'


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///sheets.db")

@app.route("/")
@login_required
def index():
    # Get user table data
    data = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    rows = data[0]["rows"]
    cols = data[0]["cols"]
    user = data[0]["username"]
    location = data[0]["location"]
    new_thing = {}

    # Gets saved data from sql database
    if location == "exists":
        things = db.execute("SELECT * FROM ? ", user)
        for thing in things:
            if thing["cell_data"] != "":
                new_thing[thing["cell"]] = thing["cell_data"]

    # Gets row numbers
    rows = list(range(rows))
    

    # Gets all the column headings
    index = 0
    cols_list = []

    def iter_all_strings():
        for size in itertools.count(1):
            for s in itertools.product(ascii_uppercase, repeat=size):
                yield "".join(s)

    for s in iter_all_strings():
        cols_list.append(s)
        index += 1
        if index == cols:
            break

    page = True

    return render_template("index.html", rows=rows, cols=cols_list, page=page, things=new_thing, user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash("Welcome,")
        flash(request.form.get("username"))
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        user = request.form.get("username")
        row = request.form.get("row")
        column = request.form.get("column")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not row:
            row = 100
        elif int(row) > 1000:
            row = 1000
        if not column:
            column = 26
        elif int(column) > 1000:
            column = 1000
        if not user:
            return apology("Username cannot be empty")
        if not password:
            return apology("Password cannot be empty")
        if not confirmation:
            return apology("Please re-enter password")

        data = db.execute("SELECT username FROM users;")
        for name in data:
            if name["username"] == user:
                return apology("Username already taken")

        if password != confirmation:
            return apology("Passwords do not match")
        password_hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash, rows, cols) VALUES(?, ?, ?, ?)", user, password_hash, row, column)
        rows = db.execute("SELECT * FROM users WHERE username = ?", user)
        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:

        return render_template("register.html")

@app.route("/password", methods=["GET", "POST"])
@login_required
def password():

    if request.method == "POST":

        current = request.form.get("current")

        if not current:
            return apology("Try again")

        password = request.form.get("password")
        if not password:
            return apology("New password cannot be empty")

        confirmation = request.form.get("confirmation")
        if not confirmation:
            return apology("Please re-enter password")

        if password != confirmation:
            return apology("Passwords do not match")

        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], current):
            return apology("Current password is invalid", 403)
        password_hash = generate_password_hash(password)
        db.execute("UPDATE users set hash=? WHERE id=?", password_hash, session["user_id"])
        return redirect("/logout")

    else:

        return render_template("password.html")


@app.route("/save", methods=["GET", "POST"])
@login_required
def save():
    if request.method == "POST":

        data = request.form.get("output")
        print("get save data = ", data)
        data = data.split(",")
        new_data = []
        a = 0
        while a < len(data) and data[0] != "":
            new_data.append([data[a], data[a + 1]])
            a += 2
        user = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])
        user = user[0]["username"]
        location = "exists"
        db.execute("CREATE TABLE IF NOT EXISTS ? (cell TEXT NOT NULL PRIMARY KEY, cell_data TEXT NOT NULL)", user)
        db.execute("UPDATE users SET location = ? WHERE id = ?", location, session["user_id"])
        for item in new_data:
            check = db.execute("SELECT COUNT(*) FROM ? WHERE cell=?;", user, item[0])
            if check[0]['COUNT(*)'] == 0:
                db.execute("INSERT INTO ? (cell, cell_data) VALUES (?, ?)", user, item[0], item[1])
            else:
                db.execute("UPDATE ? SET cell_data=? WHERE cell=?", user, item[1], item[0])

        return redirect("/")

    else:

        return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        data = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        new_rows = request.form.get("rows")
        new_cols = request.form.get("cols")


        if not new_rows:
            new_rows = data[0]["rows"]
        else:
            new_rows = int(new_rows) + data[0]["rows"]
        if new_rows > 1000:
            new_rows = 1000
            flash("Table cannot exceed 1000 rows.")

        if not new_cols:
            new_cols = data[0]["cols"]
        else:
            new_cols = int(new_cols) + data[0]["cols"]
        if new_cols > 1000:
            new_cols = 1000
            flash("Table cannot exceed 1000 columns.")

        db.execute("UPDATE users SET rows = ?, cols = ? WHERE id = ?", new_rows, new_cols, session["user_id"])

        return redirect("/")

    else:
        return redirect("/")

@app.route("/export")
@login_required
def export():
    print("Export Begin")
    data = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    rows = data[0]["rows"]
    cols = data[0]["cols"]
    user = data[0]["username"]
    location = data[0]["location"]
    new_thing = {}
    all_col = []
    col_len = 0
    all_row = []
    if location == "exists":
        things = db.execute("SELECT * FROM ? ", user)
        for thing in things:
            if thing["cell_data"] != "":
                new_thing[thing["cell"]] = thing["cell_data"]
                all_col.append(thing["cell"].split("_")[0])
                if len(thing["cell"].split("_")[0]) > col_len:
                    col_len = len(thing["cell"].split("_")[0])
                all_row.append(int(thing["cell"].split("_")[1]))


    for a in all_col:
        if len(a) < col_len:
            all_col.remove(a)

    max_col = max(all_col)
    max_row = max(all_row)
    rows = list(range(rows))
    index = 0
    cols_list = []

    def iter_all_strings():
        for size in itertools.count(1):
            for s in itertools.product(ascii_uppercase, repeat=size):
                yield "".join(s)

    for s in iter_all_strings():
        cols_list.append(s)
        index += 1
        if index == cols:
            break

    csv_list = []
    for row in rows:
        tmp = []
        for col in cols_list:
            cell_id = col + "_" + str(row)
            if cell_id in new_thing:
                tmp.append(new_thing[cell_id])
            else:
                tmp.append("")
            if col == max_col:
                break
        csv_list.append(tmp)
        if row == max_row:
            break

    print(csv_list)
    csv_name = "static/" + user + ".csv"

    with open(csv_name, 'w', newline="") as file:
        writer = csv.writer(file)
        for z in csv_list:
            writer.writerow(z)

    print("Export End")

    return redirect("/")

@app.route("/import", methods=["GET", "POST"])
@login_required
def import_file():

    if request.method == "POST":
        uploaded_file = request.files['import_file']

        file_ext = os.path.splitext(uploaded_file.filename)[1]
        if file_ext != app.config['UPLOAD_EXTENSIONS']:
            return apology("Invalid CSV file", 400)

        user = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])
        user = user[0]["username"]
        location = "exists"
        db.execute("DROP TABLE IF EXISTS ?", user)
        db.execute("CREATE TABLE IF NOT EXISTS ? (cell TEXT NOT NULL PRIMARY KEY, cell_data TEXT NOT NULL)", user)
        db.execute("UPDATE users SET location = ? WHERE id = ?", location, session["user_id"])

        x = uploaded_file.read().decode().splitlines()
        reader = csv.reader(x)
        rows = len(x)
        cols = 0
        for row in reader:
            if len(row) > cols:
                cols = len(row)
        index = 0
        cols_list = []

        def iter_all_strings():
            for size in itertools.count(1):
                for s in itertools.product(ascii_uppercase, repeat=size):
                    yield "".join(s)

        for s in iter_all_strings():
            cols_list.append(s)
            index += 1
            if index == cols:
                break

        reader = csv.reader(x)
        for row_num, row in enumerate(reader):
            for col_num, col in enumerate(row):
                cell_data = col
                cell_id = cols_list[col_num] + "_" + str(row_num)
                check = db.execute("SELECT COUNT(*) FROM ? WHERE cell=?", user, cell_id)
                if check[0]['COUNT(*)'] == 0:
                    db.execute("INSERT INTO ? (cell, cell_data) VALUES (?, ?)", user, cell_id, cell_data)
                else:
                    db.execute("UPDATE ? SET cell_data=? WHERE cell=?", user, cell_data, cell_id)

        if rows < 100:
            rows = 100
        if cols < 26:
            cols = 26
        db.execute("UPDATE users SET rows=?, cols=? WHERE username=?", rows, cols, user)

        return redirect("/")

    else:

        return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)