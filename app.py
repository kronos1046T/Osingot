import sqlite3
from flask import Flask, abort, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import positions
import users
# test
app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_positions = positions.get_positions()
    return render_template("index.html", positions=all_positions)

@app.route("/find_position")
def find_position():
    query = request.args.get("query")
    if query:
        results = positions.find_positions(query)
    else:
        query = ""
        results = []
    return render_template("find_position.html", query=query, results=results)

@app.route("/positions/<int:position_id>")
def show_position(position_id):
    position = positions.get_position(position_id)
    classes = positions.get_classes(position_id)
    return render_template("show_position.html", position=position, classes=classes)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    positions = users.get_positions_by_user(user_id)
    return render_template("show_user.html", user=user, positions=positions)

@app.route("/new_position")
def new_position():
    return render_template("new_position.html")

@app.route("/edit_position/<int:position_id>")
def edit_position(position_id):
    position = positions.get_position(position_id)
    return render_template("edit_position.html", position=position)

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

    classes = []
    field = request.form["field"]
    if field:
        classes.append(("field", field))
    season = request.form["season"]
    if season:
        classes.append(("season", season))

    positions.add_position(user_id, stock_name, ex_dividend_date, record_date, payment_date, description, classes)

    return redirect("/")

@app.route("/update_position", methods=["POST"])
def update_position():
    position_id = request.form["position_id"]
    stock_name = request.form["stock_name"]
    ex_dividend_date = request.form["ex_dividend_date"]
    record_date = request.form["record_date"]
    payment_date = request.form["payment_date"]
    description = request.form["description"]

    positions.update_position(position_id, stock_name, ex_dividend_date, record_date, payment_date, description)

    return redirect("/positions/" + str(position_id))

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    result = users.create_user(username, password1, password2)

    return result

@app.route("/delete_position/<int:position_id>", methods=["GET", "POST"])
def delete_position(position_id):
    if request.method == "GET":
        position = positions.get_position(position_id)
        return render_template("delete_position.html", position=position)
    if request.method == "POST":
        if "delete" in request.form:
            positions.delete_position(position_id)
            return redirect('/')
        else:
            return redirect("/positions/" + str(position_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    user = users.login_user(username, password)

    if user:
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return redirect("/")

    return "VIRHE: väärä tunnus tai salasana"


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect("/")
