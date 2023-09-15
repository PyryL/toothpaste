from app import app, db
from flask import render_template
from sqlalchemy.sql import text

@app.route("/")
def index():
    sql = """
        SELECT p.title AS title, t.token AS token
        FROM pastes AS p, tokens AS t
        WHERE t.paste=p.id AND t.level='view' AND p.publicity='listed' AND p.is_encrypted=FALSE
        ORDER BY modification_date DESC
        LIMIT 10
    """
    pastes = db.session.execute(text(sql)).fetchall()
    return render_template("frontpage.html", pastes=pastes)
