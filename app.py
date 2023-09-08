from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///toothpaste"
db = SQLAlchemy(app)

@app.route("/")
def index():
    return "<h1>ToothPaste</h1>"

@app.route("/paste/<string:id>", methods=["GET"])
def readPaste(id):
    sql = "SELECT title, content FROM pastes WHERE id=:id"
    result = db.session.execute(text(sql), { "id": id })
    if result.rowcount != 1:
        return "404 paste not found"
    paste = result.fetchone()

    return render_template("paste.html",
        header="Read paste",
        fieldsDisabled="disabled",
        pasteTitle=paste.title,
        pasteContent=paste.content,)

@app.route("/paste", methods=["POST"])
def pastesPost():
    sql = "INSERT INTO pastes (title, content) VALUES (:title, :content) RETURNING id"
    values = { "title": request.form["title"], "content": request.form["content"] }
    result = db.session.execute(text(sql), values)
    db.session.commit()
    new_id = result.fetchone().id
    return redirect(f"/paste/{new_id}")

@app.route("/new-paste")
def newPaste():
    return render_template("paste.html",
        header="New paste",
        fieldsDisabled="",
        pasteTitle="",
        pasteContent="",)
