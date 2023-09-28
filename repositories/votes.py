from sqlalchemy import text
from app import db

class VoteRepository:
    @classmethod
    def get_votes_of_paste(cls, token: str) -> dict:
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

    @classmethod
    def register_vote(cls, token: str, logged_in_user_id: int, is_upvote: bool):
        # check if user has already voted
        sql = """
        SELECT COUNT(*) as count
        FROM votes
        WHERE paste=(SELECT paste FROM tokens WHERE token=:token) AND voter=:userid
        """
        result = db.session.execute(text(sql), { "token": token, "userid": logged_in_user_id })
        has_already_voted = result.fetchone().count != 0

        if has_already_voted:
            sql = """
                UPDATE votes
                SET is_upvote=:isUpvote
                WHERE paste=(SELECT paste FROM tokens WHERE token=:token) AND voter=:userid
            """
            values = { "isUpvote": is_upvote, "token": token, "userid": logged_in_user_id }
            db.session.execute(text(sql), values)
            db.session.commit()
        else:
            sql = """
                INSERT INTO votes (paste, voter, is_upvote)
                VALUES ((SELECT paste FROM tokens WHERE token=:token), :userid, :isUpvote)
            """
            values = { "isUpvote": is_upvote, "token": token, "userid": logged_in_user_id }
            db.session.execute(text(sql), values)
            db.session.commit()

    @classmethod
    def delete_votes_of_paste(cls, paste_id: int):
        sql = "DELETE FROM votes WHERE paste=:pasteId"
        db.session.execute(text(sql), { "pasteId": paste_id })
        db.session.commit()
