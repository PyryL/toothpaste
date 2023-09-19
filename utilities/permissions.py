
class Permissions:
    @classmethod
    def can_delete_paste(cls, token_level: str, paste_owner_id: int, logged_in_user_id: int) -> bool:
        # modify-level token is always required
        # in addition, user must be paste owner if the paste was not created anonymously
        return token_level == "modify" and paste_owner_id == logged_in_user_id

    @classmethod
    def can_regenerate_tokens(cls, token_level: str, paste_owner_id: int, logged_in_user_id: int) -> bool:
        # modify-level token is always required
        # in addition, user must be paste owner if the paste was not created anonymously
        return token_level == "modify" and paste_owner_id == logged_in_user_id
