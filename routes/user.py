from app import app
from flask import render_template, redirect, request, session
from repositories.users import validate_credentials, add_new_user

@app.route("/log-in", methods=["GET"])
def getLogIn():
    # if user is already logged in, redirect to the front page
    if "userid" in session:
        return redirect("/")
    return render_template("login.html")

@app.route("/log-in", methods=["POST"])
def postLogIn():
    userId = validate_credentials(request.form["username"], request.form["password"])
    if userId is None:
        return redirect("/log-in")
    session["userid"] = userId
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
    userid = add_new_user(request.form["username"], request.form["password1"])
    session["userid"] = userid
    return redirect("/")
