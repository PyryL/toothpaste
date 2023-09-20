from app import app
from flask import render_template, redirect
from repositories.users import UserRepository
from utilities.session import is_user_logged_in, get_logged_in_user_id
from utilities.two_factor_auth import TwoFactorAuthentication

@app.route("/settings")
def settings():
    if not is_user_logged_in():
        return redirect("/log-in")

    user_details = UserRepository.get_user_details(get_logged_in_user_id())

    has2FAEnabled = False
    if not has2FAEnabled:
        totp = TwoFactorAuthentication.generate_new(user_details.username)

    return render_template("settings.html",
        username=user_details.username,
        has2FAEnabled=has2FAEnabled,
        TwoFAUri="" if has2FAEnabled else totp["provisioning_uri"],
        totpSecret="" if has2FAEnabled else totp["secret"]
    )
