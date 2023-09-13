from app import app, db
from flask import render_template, redirect, request
from sqlalchemy import text
from repositories.pastes import get_paste, update_paste, add_new_paste
from utilities.session import get_logged_in_user_id

@app.route("/paste/<string:token>", methods=["GET"])
def readPaste(token):
    try:
        paste = get_paste(token, get_logged_in_user_id())
    except Exception as e:
        return f"{e.args[0]} {e.args[1]}"

    return render_template("paste.html",
        header="Read paste",
        share_view_token=paste["view_token"] if paste["has_edit_permissions"] else "",
        share_modify_token=paste["modify_token"] if paste["has_edit_permissions"] else "",
        modifyToken=token if paste["has_edit_permissions"] else "",
        fieldsDisabled="" if paste["has_edit_permissions"] else "disabled",
        pastePublicity=paste["publicity"],
        pasteTitle=paste["title"],
        pasteContent=paste["content"],
        chatToken=token)

@app.route("/paste", methods=["POST"])
def pastePost():
    try:
        if request.form["modifyToken"] != "":
            update_paste(
                request.form["modifyToken"],
                request.form["title"],
                request.form["content"],
                request.form["publicity"],
                get_logged_in_user_id()
            )
            pasteToken = request.form["modifyToken"]
        else:
            pasteToken = add_new_paste(
                request.form["title"],
                request.form["content"],
                request.form["publicity"],
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
