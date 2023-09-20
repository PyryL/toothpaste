from app import app, db
from flask import render_template
from sqlalchemy.sql import text
from utilities.session import is_user_logged_in, get_logged_in_user_id
from repositories import PasteRepository

@app.route("/")
def index():
    logged_in_user_id = get_logged_in_user_id()
    return render_template("frontpage.html",
        isLoggedIn=is_user_logged_in(),
        latestPastes=PasteRepository.get_latest_frontpage_pastes(logged_in_user_id),
        myPastes=PasteRepository.get_pastes_of_user(logged_in_user_id) if is_user_logged_in() else [])
