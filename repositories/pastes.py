from app import db
from sqlalchemy import text
from repositories.tokens import get_token_data, get_tokens_of_paste, generate_token, add_new_token, delete_tokens_of_paste
from repositories.votes import delete_votes_of_paste
from repositories.chat import delete_messages_of_paste

def get_paste(pasteId: int) -> dict:
    """Load paste with given token from the database.
    Returns dictionary containing paste data if available.
    Raises an exception with data (status_code, description) if unavailable.
    """

    sql = "SELECT title, content, owner, publicity, is_encrypted FROM pastes WHERE id=:id"
    result = db.session.execute(text(sql), { "id": pasteId })
    if result.rowcount != 1:
        return None
    paste = result.fetchone()

    return paste

    # return {
    #     "title": paste.title,
    #     "content": paste.content,
    #     "publicity": paste.publicity,
    #     "is_encrypted": paste.is_encrypted,
    #     "has_edit_permissions": token_info["level"] == "modify",
    #     "is_owner": logged_in_user_id == paste.owner and logged_in_user_id is not None,
    #     "has_owner": paste.owner is not None,
    #     "view_token": next((t["token"] for t in all_tokens if t["level"] == "view"), None),
    #     "modify_token": next((t["token"] for t in all_tokens if t["level"] == "modify"), None),

    #     "owner": paste.owner
    # }

def update_paste(token: str, title: str, content: str, publicity: str, is_encrypted: bool, logged_in_user_id: int):
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
        SET title=:title, content=:content, publicity=:publicity, is_encrypted=:is_encrypted
        WHERE id=:pasteid
        RETURNING id
    """
    values = {
        "title": title,
        "content": content,
        "publicity": publicity,
        "is_encrypted": is_encrypted,
        "pasteid": token_info["pasteId"]
    }
    db.session.execute(text(sql), values)
    db.session.commit()

def add_new_paste(title: str, content: str, publicity: str, is_encrypted: bool, logged_in_user_id: int) -> str:
    """Add new paste into database and return its modify-level token."""

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
    pasteId = result.fetchone().id

    # create view and modify-level tokens
    modifyLevelToken = add_new_token(pasteId, "modify")
    add_new_token(pasteId, "view")
    return modifyLevelToken

def delete_paste(pasteId: int):
    sql = "DELETE FROM pastes WHERE id=:pasteId"
    db.session.execute(text(sql), { "pasteId": pasteId })
    db.session.commit()
