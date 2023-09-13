from app import db
from sqlalchemy import text

def add_new_message(pasteId: int, content: str, logged_in_user_id: int):
    sql = "INSERT INTO chatmessages (paste, creator, content) VALUES (:paste, :creator, :content)"
    values = {
        "paste": pasteId,
        "creator": logged_in_user_id,
        "content": content
    }
    db.session.execute(text(sql), values)
    db.session.commit()
