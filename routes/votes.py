from flask import redirect
from app import app
from utilities.session import get_logged_in_user_id
from utilities.permissions import Permissions
from repositories import PasteRepository, VoteRepository    # TokenRepository

@app.route("/vote/<string:direction>/<string:token>", methods=["POST"])
def vote(direction: str, token: str):
    logged_in_user_id = get_logged_in_user_id()
    token_info, paste = PasteRepository.get_paste_by_token(token)
    if token_info is None or paste is None:
        return "404 paste not found"
    # token_info = TokenRepository.get_token_data(token)
    # if token_info is None:
    #     return "404 paste not found"
    # paste = PasteRepository.get_paste(token_info["pasteId"])
    # if paste is None:
    #     return "404 paste not found"

    if not Permissions.can_vote(paste.publicity, paste.owner, logged_in_user_id):
        return "403 forbidden"

    VoteRepository.register_vote(token, logged_in_user_id, direction == "up")
    return redirect(f"/paste/{token}")
