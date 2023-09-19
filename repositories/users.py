from app import db
from sqlalchemy import text

class UserRepository:
    @classmethod
    def validate_credentials(cls, username: str, password: str) -> int:
        """Check if given credentials are correct.
        Returns user ID if correct, None otherwise.
        """

        sql = """
            SELECT id AS userid FROM users
            WHERE username=:username AND password_hash=crypt(:password, password_hash)
        """
        parameters = {
            "username": username,
            "password": password
        }
        result = db.session.execute(text(sql), parameters)

        if result.rowcount != 1:
            return None
        return result.fetchone().userid

    @classmethod
    def add_new_user(cls, username: str, password: str) -> int:
        """Add a new user to the database.
        Does not check given credentials for any requirements.
        Returns the user ID of the created account, or None is username already exists.
        """

        # check for duplicate username
        sql = "SELECT COUNT(username) AS count FROM users WHERE username=:username"
        result = db.session.execute(text(sql), { "username": username })
        if int(result.fetchone().count) != 0:
            return None

        sql = """
            INSERT INTO users (username, password_hash)
            VALUES (:username, crypt(:password, gen_salt('bf')))
            RETURNING id
        """
        values = {
            "username": username,
            "password": password
        }
        result = db.session.execute(text(sql), values)
        db.session.commit()
        return result.fetchone().id
