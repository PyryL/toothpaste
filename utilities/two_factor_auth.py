import pyotp
from flask_qrcode import QRcode
from app import app

# `qrcode` function can now be used in template files
QRcode(app)

class TwoFactorAuthentication:
    @classmethod
    def generate_new(cls, username: str) -> dict:
        secret = pyotp.random_base32()
        issuer_name = "ToothPaste"
        provisioning_uri = pyotp.totp.TOTP(secret).provisioning_uri(username, issuer_name)
        return {
            "secret": secret,
            "provisioning_uri": provisioning_uri
        }

    @classmethod
    def validate_2fa_code(cls, totp_secret: str, code: str) -> bool:
        totp = pyotp.TOTP(totp_secret)
        return totp.verify(code)
