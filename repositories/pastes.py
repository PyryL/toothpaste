from app import db
from sqlalchemy import text

def get_paste(id: int, logged_in_user_id: int) -> dict:
    """Load paste with given ID from the database.
    Returns dictionary containing paste data if available.
    Raises an exception with data (status_code, description) if unavailable.
    """

    sql = "SELECT title, content, owner, publicity FROM pastes WHERE id=:id"
    result = db.session.execute(text(sql), { "id": id })

    if result.rowcount != 1:
        raise Exception(404, "paste not found")
    paste = result.fetchone()

    if paste.publicity == "private" and logged_in_user_id != paste.owner:
        raise Exception(403, "not allowed to view this paste")

    return {
        "title": paste.title,
        "content": paste.content,
        "publicity": paste.publicity,
        "has_edit_permissions": logged_in_user_id is not None and logged_in_user_id == paste.owner
    }

def update_paste(id: int, title: str, content: str, publicity: str, logged_in_user_id: int):
    """Updates paste data in database."""

    # check permission
    if logged_in_user_id is None:
        raise Exception(401, "not logged in")
    sql = "SELECT owner FROM pastes WHERE id=:pasteId"
    result = db.session.execute(text(sql), { "pasteId": id })
    if result.rowcount != 1:
        raise Exception(404, "invalid paste id")
    if result.fetchone().owner != logged_in_user_id:
        raise Exception(403, "you are not the owner")

    sql = """
        UPDATE pastes
        SET title=:title, content=:content, publicity=:publicity
        WHERE id=:pasteid
        RETURNING id
    """
    values = {
        "title": title,
        "content": content,
        "publicity": publicity,
        "pasteid": id
    }
    db.session.execute(text(sql), values)
    db.session.commit()

def add_new_paste(title: str, content: str, publicity: str, logged_in_user_id: int) -> int:
    """Add new paste into database and return its ID"""

    sql = """
        INSERT INTO pastes (title, content, owner, publicity)
        VALUES (:title, :content, :owner, :publicity)
        RETURNING id
    """
    values = {
        "title": title,
        "content": content,
        "owner": logged_in_user_id,
        "publicity": publicity
    }
    result = db.session.execute(text(sql), values)
    db.session.commit()
    return result.fetchone().id
