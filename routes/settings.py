from flask import render_template, redirect, request
from app import app
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
        is_logged_in=True,
        status=request.args.get("status"),
        username=user_details.username,
        has_2fa_enabled=user_details.has_2fa_enabled,
        twofa_uri="" if user_details.has_2fa_enabled else totp["provisioning_uri"],
        totp_secret="" if user_details.has_2fa_enabled else totp["secret"]
    )

@app.route("/settings/setup-2fa", methods=["POST"])
def setup_2fa():
    if not is_user_logged_in():
        return "401 not logged in"

    totp_secret, verification_code = request.form["totp-secret"], request.form["totp-code"]
    print(f"totp setup {totp_secret} and {verification_code}")

    # check that user gave valid 2FA code
    if not TwoFactorAuthentication.validate_2fa_code(totp_secret, verification_code):
        return redirect("/settings?status=invalid-2fa-code")

    # save secret to database
    UserRepository.add_2fa_secret_to_user(get_logged_in_user_id(), totp_secret)

    return redirect("/settings")
