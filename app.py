from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>ToothPaste</h1>"

@app.route("/paste/<string:id>")
def readPaste(id):
    return render_template("paste.html",
        fieldsDisabled="disabled",
        pasteTitle=f"Paste called {id}",
        pasteContent=f"This is the content of paste with ID {id}.",)
