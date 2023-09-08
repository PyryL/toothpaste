from app import app, db
from flask import render_template, redirect, request, session
from sqlalchemy import text

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
