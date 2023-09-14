from app import app
from flask import redirect
from utilities.session import get_logged_in_user_id
from repositories.pastes import has_user_view_permission
from repositories.votes import register_vote

@app.route("/vote/<string:direction>/<string:token>", methods=["POST"])
def vote(direction: str, token: str):
    # require user to be logged in
    logged_in_user_id = get_logged_in_user_id()
    if logged_in_user_id is None:
        return "401 not logged in"
    if not has_user_view_permission(token, logged_in_user_id):
        return "403 not allowed to vote"

    register_vote(token, logged_in_user_id, direction == "up")
    return redirect(f"/paste/{token}")
