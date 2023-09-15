from app import app, db
from flask import render_template, redirect, request
from sqlalchemy import text
from repositories.pastes import get_paste, update_paste, add_new_paste
from repositories.chat import get_messages_of_paste
from repositories.votes import get_votes_of_paste
from utilities.session import get_logged_in_user_id
from utilities.encryption import encrypt, decrypt

@app.route("/paste/<string:token>", methods=["GET", "POST"])
def readPaste(token):
    try:
        paste = get_paste(token, get_logged_in_user_id())
    except Exception as e:
        return f"{e.args[0]} {e.args[1]}"

    if paste["is_encrypted"] and "decryption-key" not in request.form:
        return redirect(f"/ask-key/{token}")

    if paste["is_encrypted"]:
        content = decrypt(bytes.fromhex(paste["content"]), request.form["decryption-key"])
        if content is None:
            return redirect(f"/ask-key/{token}?status=incorrect")
        content = content.decode("utf-8")
    else:
        content = paste["content"]

    votes = get_votes_of_paste(token)
    return render_template("paste.html",
        header="Read paste",
        share_view_token=paste["view_token"] if paste["has_edit_permissions"] else "",
        share_modify_token=paste["modify_token"] if paste["has_edit_permissions"] else "",
        modifyToken=token if paste["has_edit_permissions"] else "",
        fieldsDisabled="" if paste["has_edit_permissions"] else "disabled",
        pastePublicity=paste["publicity"],
        encryption_key=request.form["decryption-key"] if paste["is_encrypted"] else "",
        pasteTitle=paste["title"],
        pasteContent=content,
        votingAvailable=True,
        upVotes=votes["upvotes"],
        downVotes=votes["downvotes"],
        chatToken=token,
        chatMessages=get_messages_of_paste(token),
        chatRemoveAvailable=paste["is_owner"])
    
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
