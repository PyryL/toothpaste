import re

class InputValidation:
    @classmethod
    def is_valid_username(cls, username: str) -> bool:
        return re.compile(r"^[a-zA-Z0-9_]{3,12}$").fullmatch(username) is not None

    @classmethod
    def is_valid_password(cls, password: str) -> bool:
        if len(password) < 8 or len(password) > 72 or \
            re.compile(r"[0-9]").search(password) is None or \
            re.compile(r"[a-z]").search(password) is None or \
            re.compile(r"[A-Z]").search(password) is None or \
            re.compile(r"[^a-zA-Z0-9]").search(password) is None:
            return False
        return True
