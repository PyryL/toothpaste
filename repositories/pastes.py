from app import db
from sqlalchemy import text
from repositories.tokens import get_token_data, get_tokens_of_paste

# TODO
from random import choices
from string import ascii_letters, digits
def generate_token() -> str:
    chars = ascii_letters + digits
    return "".join(choices(chars, k=12))

def get_paste(token: str, logged_in_user_id: int) -> dict:
    """Load paste with given token from the database.
    Returns dictionary containing paste data if available.
    Raises an exception with data (status_code, description) if unavailable.
    """

    token_info = get_token_data(token)
    if token_info is None:
        raise Exception(404, "paste not found")

    sql = "SELECT title, content, owner, publicity FROM pastes WHERE id=:id"
    result = db.session.execute(text(sql), { "id": token_info["pasteId"] })
    if result.rowcount != 1:
        raise Exception(404, "paste not found")
    paste = result.fetchone()

    if paste.publicity == "private" and logged_in_user_id != paste.owner:
        raise Exception(403, "not allowed to view this paste")

    all_tokens = get_tokens_of_paste(token_info["pasteId"])

    return {
        "title": paste.title,
        "content": paste.content,
        "publicity": paste.publicity,
        "has_edit_permissions": token_info["level"] == "modify",
        "view_token": next((t["token"] for t in all_tokens if t["level"] == "view"), None),
        "modify_token": next((t["token"] for t in all_tokens if t["level"] == "modify"), None)
    }

def update_paste(token: str, title: str, content: str, publicity: str, logged_in_user_id: int):
    """Updates paste data in database."""

    token_info = get_token_data(token)
    if token_info is None:
        raise Exception(404, "paste not found")

    # check permission
    if token_info["level"] != "modify":
        raise Exception(403, "you are not allowed to modify this paste")
    sql = "SELECT owner, publicity FROM pastes WHERE id=:pasteId"
    result = db.session.execute(text(sql), { "pasteId": token_info["pasteId"] })
    if result.rowcount != 1:
        raise Exception(404, "paste not found")
    paste = result.fetchone()
    if paste.publicity == "private" and paste.owner != logged_in_user_id:
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
        "pasteid": token_info["pasteId"]
    }
    db.session.execute(text(sql), values)
    db.session.commit()

def add_new_paste(title: str, content: str, publicity: str, logged_in_user_id: int) -> int:
    """Add new paste into database and return its modify-level token."""

    # save the paste
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
    pasteId = result.fetchone().id

    # create view and modify-level tokens
    sql = """
        INSERT INTO tokens (token, paste, level)
        VALUES (:token, :paste, :level)
    """
    modifyLevelToken = generate_token()
    modifyValues = {
        "token": modifyLevelToken,
        "paste": pasteId,
        "level": "modify"
    }
    viewValues = {
        "token": generate_token(),
        "paste": pasteId,
        "level": "view"
    }
    db.session.execute(text(sql), modifyValues)
    db.session.execute(text(sql), viewValues)
    db.session.commit()
    return modifyLevelToken
