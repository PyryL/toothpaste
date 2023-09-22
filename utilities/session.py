from flask import session

def set_logged_in_user_id(user_id: int):
    session["userid"] = user_id

def delete_session_user_id():
    if "userid" in session:
        session.pop("userid")

def get_logged_in_user_id() -> int:
    return session["userid"] if "userid" in session else None

def is_user_logged_in() -> bool:
    return "userid" in session
