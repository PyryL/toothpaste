from sqlalchemy import text
from app import db

class ChatRepository:
    @classmethod
    def add_new_message(cls, paste_id: int, content: str, logged_in_user_id: int):
        sql = """
            INSERT INTO chatmessages (paste, creator, content)
            VALUES (:paste, :creator, :content)
        """
        values = {
            "paste": paste_id,
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
    def get_paste_id_of_message(cls, message_id: int) -> int:
        sql = "SELECT paste FROM chatmessages WHERE id=:messageId"
        result = db.session.execute(text(sql), { "messageId": message_id })
        if result.rowcount != 1:
            return None
        return result.fetchone().paste

    @classmethod
    def delete_message(cls, message_id: int):
        sql = "DELETE FROM chatmessages WHERE id=:id"
        db.session.execute(text(sql), { "id": message_id })
        db.session.commit()

    @classmethod
    def delete_messages_of_paste(cls, paste_id: int):
        sql = "DELETE FROM chatmessages WHERE paste=:pasteId"
        db.session.execute(text(sql), { "pasteId": paste_id })
        db.session.commit()
