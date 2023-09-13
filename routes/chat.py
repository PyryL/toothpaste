from app import app
from flask import request, redirect
from utilities.session import get_logged_in_user_id
from repositories.tokens import get_token_data
from repositories.chat import add_new_message

@app.route("/chat", methods=["POST"])
def new_chat_message():
    token_info = get_token_data(request.form["token"])
    if token_info is None:
        return f"404 paste not found"

    add_new_message(
        token_info["pasteId"],
        request.form["content"],
        get_logged_in_user_id()
    )

    return redirect(f"/paste/{request.form['token']}")
