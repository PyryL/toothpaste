from app import db
from sqlalchemy import text

def get_token_data(token: str) -> dict:
    """Returns token information dictionary, or None if not found."""

    sql = "SELECT paste, level FROM tokens WHERE token=:token"
    result = db.session.execute(text(sql), { "token": token })
    if result.rowcount != 1:
        return None
    token_info = result.fetchone()
    return {
        "pasteId": token_info.paste,
        "level": token_info.level
    }

def get_tokens_of_paste(pasteId: int) -> list[dict]:
    """Returns a list of all tokens related to the given paste."""

    sql = "SELECT token, level FROM tokens WHERE paste=:pasteId"
    result = db.session.execute(text(sql), { "pasteId": pasteId })
    return [{ "token": row.token, "level": row.level } for row in result.fetchall()]
