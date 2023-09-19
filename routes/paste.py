from app import app, db
from flask import render_template, redirect, request
from sqlalchemy import text
from repositories.pastes import get_paste, update_paste, add_new_paste, delete_paste
from repositories.chat import get_messages_of_paste, delete_messages_of_paste
from repositories.votes import get_votes_of_paste, delete_votes_of_paste
from repositories.tokens import add_new_token, delete_tokens_of_paste, get_token_data, get_tokens_of_paste
from utilities.session import get_logged_in_user_id
from utilities.encryption import encrypt, decrypt
from utilities.permissions import Permissions

@app.route("/paste/<string:token>", methods=["GET", "POST"])
def readPaste(token):
    logged_in_user_id = get_logged_in_user_id()
    token_info = get_token_data(token)
    if token_info is None:
        return "404 paste not found"
    paste = get_paste(token_info["pasteId"])
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
        content = decrypt(bytes.fromhex(paste.content), request.form["decryption-key"])
        if content is None:
            return redirect(f"/ask-key/{token}?status=incorrect")
        content = content.decode("utf-8")
    else:
        content = paste.content

    votes = get_votes_of_paste(token)
    tokens = get_tokens_of_paste(token_info["pasteId"])
    view_token = next((t["token"] for t in tokens if t["level"] == "view"), None)
    modify_token = next((t["token"] for t in tokens if t["level"] == "modify"), None)

    return render_template("paste.html",
        header="Read paste",
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
        chatMessages=get_messages_of_paste(token),
        chatRemoveAvailable=can_delete_chat_messages)

@app.route("/paste", methods=["POST"])
def pastePost():
    if request.form["encryption-key"] == "":
        content = request.form["content"]
    else:
        content = encrypt(request.form["content"].encode("utf-8"), request.form["encryption-key"]).hex()
    try:
        if request.form["modifyToken"] != "":
            update_paste(
                request.form["modifyToken"],
                request.form["title"],
                content,
                request.form["publicity"],
                request.form["encryption-key"] != "",
                get_logged_in_user_id()
            )
            pasteToken = request.form["modifyToken"]
        else:
            pasteToken = add_new_paste(
                request.form["title"],
                content,
                request.form["publicity"],
                request.form["encryption-key"] != "",
                get_logged_in_user_id()
            )
    except Exception as e:
        return f"{e.args[0]} {e.args[1]}"
    return redirect(f"/paste/{pasteToken}")

@app.route("/new-paste")
def newPaste():
    return render_template("paste.html",
        header="New paste",
        fieldsDisabled="",
        pasteTitle="",
        pasteContent="",)

@app.route("/ask-key/<string:token>")
def askKey(token: str):
    is_incorrect = "status" in request.args and request.args["status"] == "incorrect"
    return render_template("ask-key.html",
        token=token,
        is_incorrect=is_incorrect)

@app.route("/paste/delete/<string:token>", methods=["POST"])
def deletePaste(token: str):
    logged_in_user_id = get_logged_in_user_id()
    token_info = get_token_data(token)
    if token_info is None:
        return "404 paste not found"
    paste = get_paste(token_info["pasteId"])
    if paste is None:
        return "404 paste not found"

    if not Permissions.can_delete_paste(token_info["level"], paste.owner, logged_in_user_id):
        return "403 forbidden"

    delete_tokens_of_paste(token_info["pasteId"])
    delete_votes_of_paste(token_info["pasteId"])
    delete_messages_of_paste(token_info["pasteId"])
    delete_paste(token_info["pasteId"])
    
    return redirect("/")

@app.route("/paste/regenerate-tokens/<string:token>", methods=["POST"])
def regenerateTokens(token: str):
    logged_in_user_id = get_logged_in_user_id()
    token_info = get_token_data(token)
    if token_info is None:
        return "404 paste not found"
    paste = get_paste(token_info["pasteId"])
    if paste is None:
        return "404 paste not found"

    if not Permissions.can_regenerate_tokens(token_info["level"], paste.owner, logged_in_user_id):
        return "403 forbidden"

    # delete existing and generate new
    delete_tokens_of_paste(token_info["pasteId"])
    modifyLevelToken = add_new_token(token_info["pasteId"], "modify")
    add_new_token(token_info["pasteId"], "view")

    return redirect(f"/paste/{modifyLevelToken}")
