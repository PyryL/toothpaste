from app import db
from sqlalchemy import text

class ChatRepository:
    @classmethod
    def add_new_message(cls, pasteId: int, content: str, logged_in_user_id: int):
        sql = "INSERT INTO chatmessages (paste, creator, content) VALUES (:paste, :creator, :content)"
        values = {
            "paste": pasteId,
            "creator": logged_in_user_id,
            "content": content
        }
        db.session.execute(text(sql), values)
        db.session.commit()

    @classmethod
    def get_messages_of_paste(cls, token: str) -> list:
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

    @classmethod
    def delete_message(cls, id: int):
        sql = "DELETE FROM chatmessages WHERE id=:id"
        db.session.execute(text(sql), { "id": id })
        db.session.commit()

    @classmethod
    def delete_messages_of_paste(cls, pasteId: int):
        sql = "DELETE FROM chatmessages WHERE paste=:pasteId"
        db.session.execute(text(sql), { "pasteId": pasteId })
        db.session.commit()
