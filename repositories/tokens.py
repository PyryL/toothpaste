from string import ascii_letters, digits
from sqlalchemy import text
from Crypto.Random.random import choice
from app import db

class TokenRepository:
    @classmethod
    def _generate_token(cls) -> str:
        chars = ascii_letters + digits
        sql = "SELECT COUNT(*) AS count FROM tokens WHERE token=:token"
        while True:
            token = "".join([choice(chars) for _ in range(12)])
            existing_count = int(db.session.execute(text(sql), { "token": token }).fetchone().count)
            if existing_count == 0:
                return token

    @classmethod
    def add_new_token(cls, paste_id: int, level: str) -> str:
        """Generates a new token and adds it to database. Returns the token."""

        sql = """
            INSERT INTO tokens (token, paste, level)
            VALUES (:token, :paste, :level)
        """
        token = TokenRepository._generate_token()
        values = {
            "token": token,
            "paste": paste_id,
            "level": level
        }
        db.session.execute(text(sql), values)
        db.session.commit()
        return token

    @classmethod
    def get_token_data(cls, token: str) -> dict:
        """Returns token information dictionary, or None if not found."""

        sql = "SELECT paste, level FROM tokens WHERE token=:token"
        result = db.session.execute(text(sql), { "token": token })
        if result.rowcount != 1:
            return None
        token_info = result.fetchone()
        return {
            "paste_id": token_info.paste,
            "level": token_info.level
        }

    @classmethod
    def get_tokens_of_paste(cls, paste_id: int) -> list[dict]:
        """Returns a list of all tokens related to the given paste."""

        sql = "SELECT token, level FROM tokens WHERE paste=:pasteId"
        result = db.session.execute(text(sql), { "pasteId": paste_id })
        return [{ "token": row.token, "level": row.level } for row in result.fetchall()]

    @classmethod
    def delete_tokens_of_paste(cls, paste_id: int):
        sql = "DELETE FROM tokens WHERE paste=:pasteId"
        db.session.execute(text(sql), { "pasteId": paste_id })
        db.session.commit()
