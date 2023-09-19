from app import app
from flask import request, redirect
from utilities.session import get_logged_in_user_id
from utilities.permissions import Permissions
from repositories.tokens import get_token_data
from repositories.chat import add_new_message, get_paste_owner_of_message, delete_message as delete_message_from_database
from repositories.pastes import get_paste

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

@app.route("/chat/delete/<int:id>", methods=["POST"])
def delete_message(id: int):
    logged_in_user_id = get_logged_in_user_id()
    token = request.form["token"]
    token_info = get_token_data(token)
    if token_info is None:
        return f"404 paste not found"
    paste = get_paste(token_info["pasteId"])
    if paste is None:
        return f"404 paste not found"

    if not Permissions.can_delete_chat_message(token_info["level"], paste.owner, logged_in_user_id):
        return "403 forbidden"

    delete_message_from_database(id)
    return redirect(f"/paste/{token}")
