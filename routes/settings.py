from app import app
from flask import render_template, redirect, request
from repositories.users import UserRepository
from utilities.session import is_user_logged_in, get_logged_in_user_id
from utilities.two_factor_auth import TwoFactorAuthentication

@app.route("/settings")
def settings():
    if not is_user_logged_in():
        return redirect("/log-in")

    user_details = UserRepository.get_user_details(get_logged_in_user_id())

    if not user_details.has_2fa_enabled:
        totp = TwoFactorAuthentication.generate_new(user_details.username)

    return render_template("settings.html",
        username=user_details.username,
        has2FAEnabled=user_details.has_2fa_enabled,
        TwoFAUri="" if user_details.has_2fa_enabled else totp["provisioning_uri"],
        totpSecret="" if user_details.has_2fa_enabled else totp["secret"]
    )

@app.route("/settings/setup-2fa", methods=["POST"])
def setup2FA():
    if not is_user_logged_in():
        return "401 not logged in"

    totp_secret, verification_code = request.form["totp-secret"], request.form["totp-code"]

    # check that user gave valid 2FA code
    if not TwoFactorAuthentication.validate_2FA_code(totp_secret, verification_code):
        return redirect("/settings?status=invalid-2fa-code")

    # save secret to database
    UserRepository.add_2fa_secret_to_user(get_logged_in_user_id(), totp_secret)

    return redirect("/settings")
