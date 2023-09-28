from flask import session

def set_logged_in_user_id(user_id: int):
    session["user_id"] = user_id

def delete_session_user_id():
    if "user_id" in session:
        session.pop("user_id")

def get_logged_in_user_id() -> int:
    return session["user_id"] if "user_id" in session else None

def is_user_logged_in() -> bool:
    return "user_id" in session
