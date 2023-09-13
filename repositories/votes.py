from app import db
from sqlalchemy import text

def get_votes_of_paste(token: str) -> dict:
    """Returns the number of upvotes and downvotes of the paste related to the given token."""

    sql = """
        SELECT is_upvote, COUNT(*) AS count
        FROM votes
        WHERE paste=(SELECT paste FROM tokens WHERE token=:token)
        GROUP BY is_upvote
    """
    result = db.session.execute(text(sql), { "token": token }).fetchall()
    return_data = { "upvotes": 0, "downvotes": 0 }
    for row in result:
        if row.is_upvote:
            return_data["upvotes"] = row.count
        else:
            return_data["downvotes"] = row.count
    return return_data
