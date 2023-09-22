from flask import render_template, redirect, request
from app import app
from repositories import UserRepository
from utilities.session import set_logged_in_user_id, is_user_logged_in, delete_session_user_id
from utilities.two_factor_auth import TwoFactorAuthentication
from utilities.validation import InputValidation

@app.route("/log-in", methods=["GET"])
def get_log_in():
    if is_user_logged_in():
        return redirect("/")
    return render_template("login.html", isLoggedIn=False, status=request.args.get("status"))

@app.route("/log-in", methods=["POST"])
def post_log_in():
    username, password = request.form["username"], request.form["password"]
    user_id = UserRepository.validate_credentials(username, password)
    if user_id is None:
        return redirect("/log-in?status=incorrect")

    # check two-factor authentication
    user_details = UserRepository.get_user_details(user_id)
    if request.form["totp-code"] == "" and user_details.has_2fa_enabled:
        return redirect("/log-in?status=2fa-required")
    if user_details.has_2fa_enabled:
        totp_code = request.form["totp-code"]
        totp_secret = user_details.totpsecret
        if not TwoFactorAuthentication.validate_2FA_code(totp_secret, totp_code):
            return redirect("/log-in?status=2fa-incorrect")

    set_logged_in_user_id(user_id)
    return redirect("/?status=welcome")

@app.route("/sign-up", methods=["GET"])
def get_sign_up():
    if is_user_logged_in():
        return redirect("/")
    return render_template("signup.html", isLoggedIn=False, status=request.args.get("status"))

@app.route("/sign-up", methods=["POST"])
def post_sign_up():
    # check that given credentials meet requirements
    username, password = request.form["username"], request.form["password1"]
    if request.form["password1"] != request.form["password2"] or \
        not InputValidation.is_valid_password(password) or \
        not InputValidation.is_valid_username(username):
        return redirect("/sign-up?status=criteria")

    # add user to database
    userid = UserRepository.add_new_user(username, password)
    if userid is None:
        return redirect("/sign-up?status=username-exists")
    set_logged_in_user_id(userid)
    return redirect("/?status=welcome")

@app.route("/log-out")
def log_out():
    delete_session_user_id()
    return redirect("/?status=logged-out")
