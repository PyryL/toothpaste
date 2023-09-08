from app import app, db
from flask import render_template, redirect, request, session
from sqlalchemy import text

@app.route("/paste/<string:id>", methods=["GET"])
def readPaste(id):
    sql = "SELECT title, content, owner, publicity FROM pastes WHERE id=:id"
    result = db.session.execute(text(sql), { "id": id })
    if result.rowcount != 1:
        return "404 paste not found"
    paste = result.fetchone()
    has_edit_permission = "userid" in session and session["userid"] == paste.owner

    return render_template("paste.html",
        header="Read paste",
        existingId=id,
        fieldsDisabled="" if has_edit_permission else "disabled",
        pastePublicity=paste.publicity,
        pasteTitle=paste.title,
        pasteContent=paste.content,)

@app.route("/paste", methods=["POST"])
def pastePost():
    # if this is editing, check that user has edit permissions
    if request.form["existingId"] != "":
        if "userid" not in session:
            return "401 not logged in"
        sql = "SELECT owner FROM pastes WHERE id=:pasteId"
        result = db.session.execute(text(sql), { "pasteId": request.form["existingId"] })
        if result.rowcount != 1:
            return "404 invalid paste id"
        if result.fetchone().owner != session["userid"]:
            return "403 you are not the owner"
        
        sql = """
            UPDATE pastes SET title=:title, content=:content, publicity=:publicity
            WHERE id=:pasteid
            RETURNING id
        """
        values = {
            "title": request.form["title"],
            "content": request.form["content"],
            "publicity": request.form["publicity"],
            "pasteid": request.form["existingId"]
        }
    else:
        sql = """
            INSERT INTO pastes (title, content, owner, publicity)
            VALUES (:title, :content, :owner, :publicity)
            RETURNING id
        """
        values = {
            "title": request.form["title"],
            "content": request.form["content"],
            "owner": session["userid"] if "userid" in session else None,
            "publicity": request.form["publicity"]
        }
    result = db.session.execute(text(sql), values)
    db.session.commit()
    pasteId = result.fetchone().id
    return redirect(f"/paste/{pasteId}")

@app.route("/new-paste")
def newPaste():
    return render_template("paste.html",
        header="New paste",
        fieldsDisabled="",
        pasteTitle="",
        pasteContent="",)
