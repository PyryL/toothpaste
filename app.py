from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///toothpaste"
db = SQLAlchemy(app)

@app.route("/")
def index():
    return "<h1>ToothPaste</h1>"

@app.route("/paste/<string:id>")
def readPaste(id):
    sql = "SELECT title, content FROM pastes WHERE id=:id"
    result = db.session.execute(text(sql), { "id": id })
    if result.rowcount != 1:
        return "404 paste not found"
    paste = result.fetchone()

    return render_template("paste.html",
        fieldsDisabled="disabled",
        pasteTitle=paste.title,
        pasteContent=paste.content,)
