from app import app, db
from flask import render_template
from sqlalchemy.sql import text

@app.route("/")
def index():
    sql = "SELECT id, title FROM pastes WHERE publicity='listed' ORDER BY modification_date DESC LIMIT 10"
    pastes = db.session.execute(text(sql)).fetchall()
    return render_template("frontpage.html", pastes=pastes)
