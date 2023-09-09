from app import app, db
from flask import render_template, redirect, request
from sqlalchemy import text
from repositories.pastes import get_paste, update_paste, add_new_paste
from utilities.session import get_logged_in_user_id

@app.route("/paste/<string:id>", methods=["GET"])
def readPaste(id):
    try:
        paste = get_paste(id, get_logged_in_user_id())
    except Exception as e:
        return f"{e.args[0]} {e.args[1]}"

    return render_template("paste.html",
        header="Read paste",
        existingId=id,
        fieldsDisabled="" if paste["has_edit_permissions"] else "disabled",
        pastePublicity=paste["publicity"],
        pasteTitle=paste["title"],
        pasteContent=paste["content"])

@app.route("/paste", methods=["POST"])
def pastePost():
    try:
        if request.form["existingId"] != "":
            update_paste(
                request.form["existingId"],
                request.form["title"],
                request.form["content"],
                request.form["publicity"],
                get_logged_in_user_id()
            )
            pasteId = request.form["existingId"]
        else:
            pasteId = add_new_paste(
                request.form["title"],
                request.form["content"],
                request.form["publicity"],
                get_logged_in_user_id()
            )
    except Exception as e:
        return f"{e.args[0]} {e.args[1]}"
    return redirect(f"/paste/{pasteId}")

@app.route("/new-paste")
def newPaste():
    return render_template("paste.html",
        header="New paste",
        fieldsDisabled="",
        pasteTitle="",
        pasteContent="",)
