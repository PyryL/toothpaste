from flask import session

def set_logged_in_user_id(id: int):
    session["userid"] = id

def delete_session_user_id():
    if "userid" in session:
        session.pop("userid")

def get_logged_in_user_id() -> int:
    return session["userid"] if "userid" in session else None

def is_user_logged_in() -> bool:
    return "userid" in session
