from sqlalchemy import text
from app import db

class PasteRepository:
    @classmethod
    def get_paste(cls, paste_id: int) -> dict:
        """Load paste with given token from the database.
        Returns dictionary containing paste data if available.
        Raises an exception with data (status_code, description) if unavailable.
        """

        sql = "SELECT title, content, owner, publicity, is_encrypted FROM pastes WHERE id=:id"
        result = db.session.execute(text(sql), { "id": paste_id })
        if result.rowcount != 1:
            return None
        return result.fetchone()

    @classmethod
    def update_paste(
        cls, paste_id: int, title: str, content: str, publicity: str, is_encrypted: bool
    ):
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
            "pasteid": paste_id
        }
        db.session.execute(text(sql), values)
        db.session.commit()

    @classmethod
    def add_new_paste(
        cls, title: str, content: str, publicity: str, is_encrypted: bool, logged_in_user_id: int
    ) -> str:
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
    def delete_paste(cls, paste_id: int):
        sql = "DELETE FROM pastes WHERE id=:pasteId"
        db.session.execute(text(sql), { "pasteId": paste_id })
        db.session.commit()

    @classmethod
    def get_latest_frontpage_pastes(cls, exclude_owner: int):
        """Returns database result of ten latest pastes whose owner is not the given user."""
        sql = """
            SELECT p.title AS title, t.token AS token
            FROM pastes AS p, tokens AS t
            WHERE t.paste=p.id AND t.level='view' AND p.publicity='listed' AND
                p.is_encrypted=FALSE AND (p.owner IS NULL OR p.owner != :excludeOwner)
            ORDER BY modification_date DESC
            LIMIT 10
        """
        values = { "excludeOwner": -1 if exclude_owner is None else exclude_owner }
        result = db.session.execute(text(sql), values)
        return result.fetchall()

    @classmethod
    def get_pastes_of_user(cls, user_id: int):
        """Returns database result containing title and modify-level token
        of all pastes owned by given user."""

        sql = """
            SELECT p.title AS title, t.token AS token
            FROM pastes AS p, tokens AS t
            WHERE t.paste=p.id AND t.level='modify' AND p.owner=:owner
            ORDER BY modification_date DESC
        """
        return db.session.execute(text(sql), { "owner": user_id }).fetchall()
