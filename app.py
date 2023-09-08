from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SESSION_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    sql = "SELECT id, title FROM pastes ORDER BY modification_date DESC LIMIT 10"
    pastes = db.session.execute(text(sql)).fetchall()
    return render_template("frontpage.html", pastes=pastes)

@app.route("/paste/<string:id>", methods=["GET"])
def readPaste(id):
    sql = "SELECT title, content, owner FROM pastes WHERE id=:id"
    result = db.session.execute(text(sql), { "id": id })
    if result.rowcount != 1:
        return "404 paste not found"
    paste = result.fetchone()
    has_edit_permission = "userid" in session and session["userid"] == paste.owner

    return render_template("paste.html",
        header="Read paste",
        fieldsDisabled="" if has_edit_permission else "disabled",
        pasteTitle=paste.title,
        pasteContent=paste.content,)

@app.route("/paste", methods=["POST"])
def pastesPost():
    sql = "INSERT INTO pastes (title, content, owner) VALUES (:title, :content, :owner) RETURNING id"
    values = {
        "title": request.form["title"],
        "content": request.form["content"],
        "owner": session["userid"] if "userid" in session else None
    }
    result = db.session.execute(text(sql), values)
    db.session.commit()
    new_id = result.fetchone().id
    return redirect(f"/paste/{new_id}")

@app.route("/new-paste")
def newPaste():
    return render_template("paste.html",
        header="New paste",
        fieldsDisabled="",
        pasteTitle="",
        pasteContent="",)

@app.route("/log-in", methods=["GET"])
def getLogIn():
    # if user is already logged in, redirect to the front page
    if "userid" in session:
        return redirect("/")
    return render_template("login.html")

@app.route("/log-in", methods=["POST"])
def postLogIn():
    # check credentials
    sql = "SELECT id AS userid FROM users WHERE username=:username AND password_hash=crypt(:password, password_hash)"
    parameters = { "username": request.form["username"], "password": request.form["password"] }
    result = db.session.execute(text(sql), parameters)

    # incorrect username and/or password
    if result.rowcount != 1:
        return redirect("/log-in")

    session["userid"] = result.fetchone().userid
    return redirect("/")

@app.route("/sign-up", methods=["GET"])
def getSignUp():
    # if user has already logged in, redirect to the front page
    if "userid" in session:
        return redirect("/")
    return render_template("signup.html")

@app.route("/sign-up", methods=["POST"])
def postSignUp():
    # check that given credentials meet requirements
    # TODO: add more criteria for security
    if request.form["password1"] != request.form["password2"] or \
        len(request.form["password1"]) < 1 or len(request.form["password1"]) > 72 or \
        len(request.form["username"]) < 1 or len(request.form["username"]) > 12:
        return "criteria not met"
    
    # add user to database
    sql = "INSERT INTO users (username, password_hash) VALUES (:username, crypt(:password, gen_salt('bf'))) RETURNING id"
    values = { "username": request.form["username"], "password": request.form["password1"] }
    result = db.session.execute(text(sql), values)
    db.session.commit()

    # log user in and redirect to the front page
    session["userid"] = result.fetchone().id
    return redirect("/")
