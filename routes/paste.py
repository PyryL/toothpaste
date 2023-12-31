from flask import render_template, redirect, request
from app import app
from repositories import PasteRepository, ChatRepository, VoteRepository, TokenRepository
from utilities.session import is_user_logged_in, get_logged_in_user_id
from utilities.encryption import Encryption
from utilities.permissions import Permissions

@app.route("/paste/<string:token>", methods=["GET", "POST"])
def read_paste(token: str):
    logged_in_user_id = get_logged_in_user_id()
    token_info, paste = PasteRepository.get_paste_by_token(token)
    if token_info is None or paste is None:
        return "404 paste not found"

    if not Permissions.can_view_paste(paste.publicity, paste.owner, logged_in_user_id):
        return "403 forbidden"
    has_edit_permissions = Permissions.can_modify_paste(
        token_info["level"],
        paste.publicity,
        paste.owner,
        logged_in_user_id)
    has_delete_permission = Permissions.can_delete_paste(
        token_info["level"],
        paste.owner,
        logged_in_user_id)
    can_delete_chat_messages = Permissions.can_delete_chat_message(
        token_info["level"],
        paste.owner,
        logged_in_user_id)
    can_regenerate_tokens = Permissions.can_regenerate_tokens(
        token_info["level"],
        paste.owner,
        logged_in_user_id)

    if paste.is_encrypted and "decryption-key" not in request.form:
        return redirect(f"/ask-key/{token}")

    if paste.is_encrypted:
        content = Encryption.decrypt(bytes.fromhex(paste.content), request.form["decryption-key"])
        if content is None:
            return redirect(f"/ask-key/{token}?status=incorrect")
        content = content.decode("utf-8")
    else:
        content = paste.content

    votes = VoteRepository.get_votes_of_paste(token)
    tokens = TokenRepository.get_tokens_of_paste(token_info["paste_id"])
    view_token = next((t["token"] for t in tokens if t["level"] == "view"), None)
    modify_token = next((t["token"] for t in tokens if t["level"] == "modify"), None)

    return render_template("paste.html",
        is_logged_in=is_user_logged_in(),
        header="Read paste",
        is_modify=has_edit_permissions,
        share_view_token=view_token if has_edit_permissions else "",
        share_modify_token=modify_token if has_edit_permissions else "",
        token_regeneration_available=can_regenerate_tokens,
        modify_token=token if has_edit_permissions else "",
        fields_disabled="" if has_edit_permissions else "disabled",
        paste_publicity=paste.publicity,
        private_publicity_disabled="" if is_user_logged_in() else "disabled",
        encryption_key=request.form["decryption-key"] if paste.is_encrypted else "",
        paste_title=paste.title,
        paste_content=content,
        paste_delete_available=has_delete_permission,
        voting_available=Permissions.can_vote(paste.publicity, paste.owner, logged_in_user_id),
        voting_visible=True,
        up_votes=votes["upvotes"],
        down_votes=votes["downvotes"],
        chat_token=token,
        chat_messages=ChatRepository.get_messages_of_paste(token),
        chat_remove_available=can_delete_chat_messages)

@app.route("/paste", methods=["POST"])
def paste_post():
    # in case of modify, check that user has permission to modify
    is_modify = request.form["modifyToken"] != ""
    logged_in_user_id = get_logged_in_user_id()
    if is_modify:
        token_info, paste = PasteRepository.get_paste_by_token(request.form["modifyToken"])
        if token_info is None or paste is None:
            return "404 paste not found"
        if not Permissions.can_modify_paste(token_info["level"], paste.publicity,
            paste.owner, logged_in_user_id):
            return "403 forbidden"

    # validate inputs
    if len(request.form["content"]) == 0 or len(request.form["title"]) == 0 or \
       request.form["publicity"] not in ["listed", "unlisted", "private"]:
        return "400 bad request"

    # encrypt paste content if encryption key is provided
    is_encrypted = request.form["encryption-key"] != ""
    if is_encrypted:
        content = Encryption.encrypt(
            request.form["content"].encode("utf-8"),
            request.form["encryption-key"]).hex()
    else:
        content = request.form["content"]

    # insert or update database
    paste = {
        "title": request.form["title"],
        "content": content,
        "publicity": request.form["publicity"],
        "is_encrypted": is_encrypted
    }
    if is_modify:
        PasteRepository.update_paste(token_info["paste_id"], paste)
        token = request.form["modifyToken"]
    else:
        paste_id = PasteRepository.add_new_paste(paste, logged_in_user_id)
        token = TokenRepository.add_new_token(paste_id, "modify")
        TokenRepository.add_new_token(paste_id, "view")

    return redirect(f"/paste/{token}")

@app.route("/new-paste")
def new_paste():
    return render_template("paste.html",
        is_logged_in=is_user_logged_in(),
        header="New paste",
        is_modify=True,
        fields_disabled="",
        private_publicity_disabled="" if is_user_logged_in() else "disabled",
        paste_title="",
        paste_content="",)

@app.route("/ask-key/<string:token>")
def ask_key(token: str):
    is_incorrect = "status" in request.args and request.args["status"] == "incorrect"
    return render_template("ask-key.html",
        is_logged_in=is_user_logged_in(),
        token=token,
        is_incorrect=is_incorrect)

@app.route("/paste/delete/<string:token>", methods=["POST"])
def delete_paste(token: str):
    logged_in_user_id = get_logged_in_user_id()
    token_info, paste = PasteRepository.get_paste_by_token(token)
    if token_info is None or paste is None:
        return "404 paste not found"

    if not Permissions.can_delete_paste(token_info["level"], paste.owner, logged_in_user_id):
        return "403 forbidden"

    TokenRepository.delete_tokens_of_paste(token_info["paste_id"])
    VoteRepository.delete_votes_of_paste(token_info["paste_id"])
    ChatRepository.delete_messages_of_paste(token_info["paste_id"])
    PasteRepository.delete_paste(token_info["paste_id"])

    return redirect("/?status=paste-deleted")

@app.route("/paste/regenerate-tokens/<string:token>", methods=["POST"])
def regenerate_tokens(token: str):
    logged_in_user_id = get_logged_in_user_id()
    token_info, paste = PasteRepository.get_paste_by_token(token)
    if token_info is None or paste is None:
        return "404 paste not found"

    if not Permissions.can_regenerate_tokens(token_info["level"], paste.owner, logged_in_user_id):
        return "403 forbidden"

    # delete existing and generate new
    TokenRepository.delete_tokens_of_paste(token_info["paste_id"])
    modify_level_token = TokenRepository.add_new_token(token_info["paste_id"], "modify")
    TokenRepository.add_new_token(token_info["paste_id"], "view")

    return redirect(f"/paste/{modify_level_token}")
