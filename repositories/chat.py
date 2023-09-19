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

def get_messages_of_paste(token: str) -> list:
    """Get chat messages that relate to the same paste as the given token.
    Return value is a database result. Each item has three values:
    `creator` (username or None), `content` and `creation_date`
    """

    sql = """
        SELECT id, content, creation_date, (SELECT username FROM users WHERE id=creator) AS creator
        FROM chatmessages
        WHERE paste=(SELECT paste FROM tokens WHERE token=:token)
        ORDER BY creation_date ASC
    """
    result = db.session.execute(text(sql), { "token": token })
    return result.fetchall()

def get_paste_owner_of_message(id: int) -> int:
    sql = "SELECT owner FROM pastes WHERE id=(SELECT paste FROM chatmessages WHERE id=:id)"
    result = db.session.execute(text(sql), { "id": id })
    if result.rowcount != 1:
        return None
    return result.fetchone().owner

def delete_message(id: int):
    sql = "DELETE FROM chatmessages WHERE id=:id"
    db.session.execute(text(sql), { "id": id })
    db.session.commit()

def delete_messages_of_paste(pasteId: int):
    sql = "DELETE FROM chatmessages WHERE paste=:pasteId"
    db.session.execute(text(sql), { "pasteId": pasteId })
    db.session.commit()
