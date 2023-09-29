import re

class InputValidation:
    @classmethod
    def is_valid_username(cls, username: str) -> bool:
        return re.compile(r"^[a-zA-Z0-9_]{3,12}$").fullmatch(username) is not None

    @classmethod
    def is_valid_password(cls, password: str) -> bool:
        # list item is True, if password meets that exact criteria
        criteria = [
            len(password) >= 8,
            len(password) <= 72,
            re.compile(r"[0-9]").search(password) is not None,
            re.compile(r"[A-Z]").search(password) is not None,
            re.compile(r"[a-z]").search(password) is not None,
            re.compile(r"[^a-zA-Z0-9]").search(password) is not None,
        ]
        return False not in criteria
