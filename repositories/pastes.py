from app import db
from sqlalchemy import text

class PasteRepository:
    @classmethod
    def get_paste(cls, pasteId: int) -> dict:
        """Load paste with given token from the database.
        Returns dictionary containing paste data if available.
        Raises an exception with data (status_code, description) if unavailable.
        """

        sql = "SELECT title, content, owner, publicity, is_encrypted FROM pastes WHERE id=:id"
        result = db.session.execute(text(sql), { "id": pasteId })
        if result.rowcount != 1:
            return None
        return result.fetchone()

    @classmethod
    def update_paste(cls, pasteId: int, title: str, content: str, publicity: str, is_encrypted: bool, logged_in_user_id: int):
        """Updates paste data in database."""

        sql = """
            UPDATE pastes
            SET title=:title, content=:content, publicity=:publicity, is_encrypted=:is_encrypted
            WHERE id=:pasteid
        """
        values = {
            "title": title,
            "content": content,
            "publicity": publicity,
            "is_encrypted": is_encrypted,
            "pasteid": pasteId
        }
        db.session.execute(text(sql), values)
        db.session.commit()

    @classmethod
    def add_new_paste(cls, title: str, content: str, publicity: str, is_encrypted: bool, logged_in_user_id: int) -> str:
        """Add new paste into database and return its id."""

        # save the paste
        sql = """
            INSERT INTO pastes (title, content, owner, publicity, is_encrypted)
            VALUES (:title, :content, :owner, :publicity, :is_encrypted)
            RETURNING id
        """
        values = {
            "title": title,
            "content": content,
            "owner": logged_in_user_id,
            "publicity": publicity,
            "is_encrypted": is_encrypted
        }
        result = db.session.execute(text(sql), values)
        return result.fetchone().id

    @classmethod
    def delete_paste(cls, pasteId: int):
        sql = "DELETE FROM pastes WHERE id=:pasteId"
        db.session.execute(text(sql), { "pasteId": pasteId })
        db.session.commit()
