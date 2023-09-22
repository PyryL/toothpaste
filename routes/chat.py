from flask import request, redirect
from app import app
from utilities.session import get_logged_in_user_id
from utilities.permissions import Permissions
from repositories import TokenRepository, ChatRepository, PasteRepository

@app.route("/chat", methods=["POST"])
def new_chat_message():
    token_info = TokenRepository.get_token_data(request.form["token"])
    if token_info is None:
        return "404 paste not found"

    ChatRepository.add_new_message(
        token_info["pasteId"],
        request.form["content"],
        get_logged_in_user_id()
    )

    return redirect(f"/paste/{request.form['token']}")

@app.route("/chat/delete/<int:message_id>", methods=["POST"])
def delete_message(message_id: int):
    logged_in_user_id = get_logged_in_user_id()
    token = request.form["token"]
    token_info = TokenRepository.get_token_data(token)
    if token_info is None:
        return "404 paste not found"
    paste = PasteRepository.get_paste(token_info["pasteId"])
    if paste is None:
        return "404 paste not found"

    if not Permissions.can_delete_chat_message(token_info["level"], paste.owner, logged_in_user_id):
        return "403 forbidden"
    # make sure that token is related to the same paste with chat message
    if ChatRepository.get_paste_id_of_message(message_id) != token_info["pasteId"]:
        return "400 bad request"

    ChatRepository.delete_message(message_id)
    return redirect(f"/paste/{token}")
