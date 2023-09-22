from app import app, db
from flask import render_template, redirect, request
from sqlalchemy import text
from repositories import PasteRepository, ChatRepository, VoteRepository, TokenRepository
from utilities.session import is_user_logged_in, get_logged_in_user_id
from utilities.encryption import Encryption
from utilities.permissions import Permissions

@app.route("/paste/<string:token>", methods=["GET", "POST"])
def readPaste(token):
    logged_in_user_id = get_logged_in_user_id()
    token_info = TokenRepository.get_token_data(token)
    if token_info is None:
        return "404 paste not found"
    paste = PasteRepository.get_paste(token_info["pasteId"])
    if paste is None:
        return "404 paste not found"

    if not Permissions.can_view_paste(paste.publicity, paste.owner, logged_in_user_id):
        return "403 forbidden"
    has_edit_permissions = Permissions.can_modify_paste(token_info["level"], paste.publicity, paste.owner, logged_in_user_id)
    has_delete_permission = Permissions.can_delete_paste(token_info["level"], paste.owner, logged_in_user_id)
    can_delete_chat_messages = Permissions.can_delete_chat_message(token_info["level"], paste.owner, logged_in_user_id)

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
    tokens = TokenRepository.get_tokens_of_paste(token_info["pasteId"])
    view_token = next((t["token"] for t in tokens if t["level"] == "view"), None)
    modify_token = next((t["token"] for t in tokens if t["level"] == "modify"), None)

    return render_template("paste.html",
        isLoggedIn=is_user_logged_in(),
        header="Read paste",
        is_modify=has_edit_permissions,
        share_view_token=view_token if has_edit_permissions else "",
        share_modify_token=modify_token if has_edit_permissions else "",
        modifyToken=token if has_edit_permissions else "",
        fieldsDisabled="" if has_edit_permissions else "disabled",
        pastePublicity=paste.publicity,
        encryption_key=request.form["decryption-key"] if paste.is_encrypted else "",
        pasteTitle=paste.title,
        pasteContent=content,
        pasteDeleteAvailable=has_delete_permission,
        votingAvailable=True,
        upVotes=votes["upvotes"],
        downVotes=votes["downvotes"],
        chatToken=token,
        chatMessages=ChatRepository.get_messages_of_paste(token),
        chatRemoveAvailable=can_delete_chat_messages)

@app.route("/paste", methods=["POST"])
def pastePost():
    # in case of modify, check that user has permission to modify
    is_modify = request.form["modifyToken"] != ""
    logged_in_user_id = get_logged_in_user_id()
    if is_modify:
        token_info = TokenRepository.get_token_data(request.form["modifyToken"])
        if token_info is None:
            return "404 paste not found"
        paste = PasteRepository.get_paste(token_info["pasteId"])
        if paste is None:
            return "404 paste not found"
        if not Permissions.can_modify_paste(token_info["level"], paste.publicity, paste.owner, logged_in_user_id):
            return "403 forbidden"

    # encrypt paste content if encryption key is provided
    is_encrypted = request.form["encryption-key"] != ""
    if is_encrypted:
        content = Encryption.encrypt(request.form["content"].encode("utf-8"), request.form["encryption-key"]).hex()
    else:
        content = request.form["content"]

    # insert or update database
    if is_modify:
        PasteRepository.update_paste(
            token_info["pasteId"],
            request.form["title"],
            content,
            request.form["publicity"],
            is_encrypted,
            logged_in_user_id
        )
        token = request.form["modifyToken"]
    else:
        pasteId = PasteRepository.add_new_paste(
            request.form["title"],
            content,
            request.form["publicity"],
            is_encrypted,
            logged_in_user_id
        )
        token = TokenRepository.add_new_token(pasteId, "modify")
        TokenRepository.add_new_token(pasteId, "view")

    return redirect(f"/paste/{token}")

@app.route("/new-paste")
def newPaste():
    return render_template("paste.html",
        isLoggedIn=is_user_logged_in(),
        header="New paste",
        is_modify=True,
        fieldsDisabled="",
        pasteTitle="",
        pasteContent="",)

@app.route("/ask-key/<string:token>")
def askKey(token: str):
    is_incorrect = "status" in request.args and request.args["status"] == "incorrect"
    return render_template("ask-key.html",
        isLoggedIn=is_user_logged_in(),
        token=token,
        is_incorrect=is_incorrect)

@app.route("/paste/delete/<string:token>", methods=["POST"])
def deletePaste(token: str):
    logged_in_user_id = get_logged_in_user_id()
    token_info = TokenRepository.get_token_data(token)
    if token_info is None:
        return "404 paste not found"
    paste = PasteRepository.get_paste(token_info["pasteId"])
    if paste is None:
        return "404 paste not found"

    if not Permissions.can_delete_paste(token_info["level"], paste.owner, logged_in_user_id):
        return "403 forbidden"

    TokenRepository.delete_tokens_of_paste(token_info["pasteId"])
    VoteRepository.delete_votes_of_paste(token_info["pasteId"])
    ChatRepository.delete_messages_of_paste(token_info["pasteId"])
    PasteRepository.delete_paste(token_info["pasteId"])
    
    return redirect("/?status=paste-deleted")

@app.route("/paste/regenerate-tokens/<string:token>", methods=["POST"])
def regenerateTokens(token: str):
    logged_in_user_id = get_logged_in_user_id()
    token_info = TokenRepository.get_token_data(token)
    if token_info is None:
        return "404 paste not found"
    paste = PasteRepository.get_paste(token_info["pasteId"])
    if paste is None:
        return "404 paste not found"

    if not Permissions.can_regenerate_tokens(token_info["level"], paste.owner, logged_in_user_id):
        return "403 forbidden"

    # delete existing and generate new
    TokenRepository.delete_tokens_of_paste(token_info["pasteId"])
    modifyLevelToken = TokenRepository.add_new_token(token_info["pasteId"], "modify")
    TokenRepository.add_new_token(token_info["pasteId"], "view")

    return redirect(f"/paste/{modifyLevelToken}")
