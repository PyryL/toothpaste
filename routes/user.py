from app import app
from flask import render_template, redirect, request, session
from repositories import UserRepository
from utilities.session import set_logged_in_user_id, is_user_logged_in
from utilities.validation import InputValidation

@app.route("/log-in", methods=["GET"])
def getLogIn():
    if is_user_logged_in():
        return redirect("/")
    return render_template("login.html")

@app.route("/log-in", methods=["POST"])
def postLogIn():
    userId = UserRepository.validate_credentials(request.form["username"], request.form["password"])
    if userId is None:
        return redirect("/log-in")
    set_logged_in_user_id(userId)
    return redirect("/")

@app.route("/sign-up", methods=["GET"])
def getSignUp():
    if is_user_logged_in():
        return redirect("/")
    return render_template("signup.html")

@app.route("/sign-up", methods=["POST"])
def postSignUp():
    # check that given credentials meet requirements
    username, password = request.form["username"], request.form["password1"]
    if request.form["password1"] != request.form["password2"] or \
        not InputValidation.is_valid_password(password) or \
        not InputValidation.is_valid_username(username):
        return "username and/or password criteria not met"

    # add user to database
    userid = UserRepository.add_new_user(username, password)
    if userid is None:
        return redirect("/sign-up?status=username-exists")
    set_logged_in_user_id(userid)
    return redirect("/")
