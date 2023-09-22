from flask import render_template, request
from app import app
from utilities.session import is_user_logged_in, get_logged_in_user_id
from repositories import PasteRepository, UserRepository

@app.route("/")
def index():
    logged_in_user_id = get_logged_in_user_id()
    if is_user_logged_in():
        username = UserRepository.get_user_details(logged_in_user_id).username
        my_pastes = PasteRepository.get_pastes_of_user(logged_in_user_id)
    else:
        username = ""
        my_pastes = []

    return render_template("frontpage.html",
        isLoggedIn=is_user_logged_in(),
        status=request.args.get("status"),
        username=username,
        latestPastes=PasteRepository.get_latest_frontpage_pastes(logged_in_user_id),
        myPastes=my_pastes)
