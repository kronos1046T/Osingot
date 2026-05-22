import sqlite3
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/new_position")
def new_position():
    return render_template("new_position.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create_position", methods=["POST"])
def create_position():
    stock_name = request.form["stock_name"]
    ex_dividend_date = request.form["ex_dividend_date"]
    record_date = request.form["record_date"]
    payment_date = request.form["payment_date"]
    description = request.form["description"]
    user_id = session["user_id"]

    sql = """INSERT INTO positions (user_id, stock_name, 
             ex_dividend_date, record_date, 
             payment_date, description) VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [user_id, stock_name, ex_dividend_date, record_date, payment_date, description])

    return redirect("/")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])

    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])

        if len(result) == 0:
            return "VIRHE: väärä tunnus tai salasana"

        user_id = result[0][0]
        password_hash = result[0][1]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")

        return "VIRHE: väärä tunnus tai salasana"


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect("/")
