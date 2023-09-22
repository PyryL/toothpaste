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

    @classmethod
    def get_latest_frontpage_pastes(cls, excludeOwner: int):
        """Returns database result of ten latest pastes whose owner is not the given user."""
        sql = """
            SELECT p.title AS title, t.token AS token
            FROM pastes AS p, tokens AS t
            WHERE t.paste=p.id AND t.level='view' AND p.publicity='listed' AND
                p.is_encrypted=FALSE AND (p.owner IS NULL OR p.owner != :excludeOwner)
            ORDER BY modification_date DESC
            LIMIT 10
        """
        result = db.session.execute(text(sql), { "excludeOwner": -1 if excludeOwner is None else excludeOwner })
        return result.fetchall()

    @classmethod
    def get_pastes_of_user(cls, userId: int):
        """Returns database result containing title and modify-level token of all pastes owned by given user."""
        sql = """
            SELECT p.title AS title, t.token AS token
            FROM pastes AS p, tokens AS t
            WHERE t.paste=p.id AND t.level='modify' AND p.owner=:owner
            ORDER BY modification_date DESC
        """
        return db.session.execute(text(sql), { "owner": userId }).fetchall()
