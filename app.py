from turtle import position
from flask import Flask, abort, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import positions
import users
import secrets
# test
app = Flask(__name__)
app.secret_key = config.secret_key


def require_login():
    if "user_id" not in session:
        abort(403)



def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if "csrf_token" not in session:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)



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
    comments = positions.list_comments(db, position_id)
    return render_template("show_position.html", position=position, classes=classes, comments=comments)



@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    positions = users.get_positions_by_user(user_id)
    return render_template("show_user.html", user=user, positions=positions)



@app.route("/new_position")
def new_position():
    classes = positions.get_all_classes()
    return render_template("new_position.html", classes=classes)



@app.route("/edit_position/<int:position_id>")
def edit_position(position_id):
    require_login()
    position = positions.get_position(position_id)
    if session.get("user_id") != position["user_id"]:
        abort(403)
    classes = positions.get_classes(position_id)
    all_classes = positions.get_all_classes()
    return render_template("edit_position.html", position=position, classes=classes , all_classes=all_classes)




@app.route("/edit_comment/<int:comment_id>", methods=["GET"])
def edit_comment(comment_id):
    require_login()
    comment = positions.get_comment(comment_id)
    if session.get("user_id") != comment["user_id"]:
        return "Ei oikeuksia", 403
    return render_template("edit_comment.html", comment=comment)



@app.route("/register")
def register():
    return render_template("register.html")



@app.route("/update_comment/<int:comment_id>", methods=["POST"])
def update_comment(comment_id):
    require_login()
    check_csrf()
    content = request.form["content"]
    comment = positions.get_comment(comment_id)
    if session.get("user_id") != comment["user_id"]:
        return "Ei oikeuksia", 403
    positions.update_comment(comment_id, content)
    return redirect(f"/positions/{comment['position_id']}")



@app.route("/create_comment/<int:position_id>", methods=["POST"])
def create_comment(position_id):
    require_login()
    check_csrf()
    content = request.form["content"]
    positions.add_comment(position_id, session["user_id"], content)
    return redirect(f"/positions/{position_id}")




@app.route("/create_position", methods=["POST"])
def create_position():
    require_login()
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    check_csrf()

    stock_name = request.form["stock_name"]
    if len(stock_name) > 100:
        return "Osakkee nimi on liian pitkä (max 100 merkkiä)."
    
    ex_dividend_date = request.form["ex_dividend_date"]
    record_date = request.form["record_date"]
    payment_date = request.form["payment_date"]
    if ex_dividend_date > record_date:
        return "Täsmäytyspäivä ei voi olla ennen osingon irtoamispäivää."
    if ex_dividend_date > payment_date:
        return "Maksupäivä ei voi olla ennen osingon irtoamispäivää."
    if record_date > payment_date:
        return "Maksupäivä ei voi olla ennen täsmäytyspäivää."
    
    description = request.form["description"]
    if len(description.split()) > 200:
        return "Kuvaus liian pitkä (max 200 sanaa)."
    
    user_id = session["user_id"]
    classes = []
    for entry in request.form.getlist("classes"):
        if entry and ":" in entry:
            parts = entry.split(":", 1)
            if len(parts) == 2:
                classes.append((parts[0], parts[1]))
    positions.add_position(user_id, stock_name, ex_dividend_date, record_date, payment_date, description, classes)
    return redirect("/")



@app.route("/update_position", methods=["POST"])
def update_position():
    require_login()
    check_csrf()
    position_id = request.form["position_id"]
    position = positions.get_position(position_id)
    if session.get("user_id") != position["user_id"]:
        abort(403)
    
    stock_name = request.form["stock_name"]
    if len(stock_name) > 100:
        return "Osakkeen nimi on liian pitkä (max 100 merkkiä)."

    ex_dividend_date = request.form["ex_dividend_date"]
    record_date = request.form["record_date"]
    payment_date = request.form["payment_date"]
    if ex_dividend_date > record_date:
        return "Täsmäytyspäivä ei voi olla ennen osingon irtoamispäivää."
    if ex_dividend_date > payment_date:
        return "Maksupäivä ei voi olla ennen osingon irtoamispäivää."
    if record_date > payment_date:
        return "Maksupäivä ei voi olla ennen täsmäytyspäivää."

    description = request.form["description"]
    if len(description.split()) > 200:
        return "Kuvaus liian pitkä (max 200 sanaa)."

    classes = []
    for entry in request.form.getlist("classes"):
        if entry and ":" in entry:
            type, value = entry.split(":", 1)
            classes.append((type, value))

    positions.update_position(position_id, stock_name, ex_dividend_date, record_date, payment_date, description, classes)
    return redirect("/positions/" + str(position_id))



@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    result = users.create_user(username, password1, password2)
    return result



@app.route("/delete_comment/<int:comment_id>", methods=["POST"])
def delete_comment(comment_id):
    require_login()
    check_csrf()
    comment = positions.get_comment(comment_id)
    if session.get("user_id") != comment["user_id"]:
        return "Ei oikeuksia", 403
    positions.delete_comment(comment_id)
    return redirect(f"/positions/{comment['position_id']}")


@app.route("/delete_position/<int:position_id>", methods=["GET", "POST"])
def delete_position(position_id):
    require_login()
    position = positions.get_position(position_id)
    if session.get("user_id") != position["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("delete_position.html", position=position)
    if request.method == "POST":
        check_csrf()
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
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")

    return "VIRHE: väärä tunnus tai salasana"


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("csrf_token", None)
    return redirect("/")