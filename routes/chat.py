from app import app
from flask import request, redirect
from utilities.session import get_logged_in_user_id
from repositories.tokens import get_token_data
from repositories.chat import add_new_message, get_paste_owner_of_message, delete_message as delete_message_from_database

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
    # check that logged-in user is the owner of the paste of this chat message
    logged_in_user_id = get_logged_in_user_id()
    if logged_in_user_id is None:
        return f"401 not logged in"
    if logged_in_user_id != get_paste_owner_of_message(id):
        return f"403 you are not the owner"

    delete_message_from_database(id)
    return redirect(f"/paste/{request.form['token']}")
