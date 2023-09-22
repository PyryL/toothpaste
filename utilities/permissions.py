
class Permissions:
    @classmethod
    def can_view_paste(
        cls, paste_publicity: str, paste_owner_id: int, logged_in_user_id: int
    ) -> bool:
        if paste_publicity in ["listed", "unlisted"]:
            return True
        return paste_owner_id == logged_in_user_id and logged_in_user_id is not None

    @classmethod
    def can_modify_paste(
        cls, token_level: str, paste_publicity: str, paste_owner_id: int, logged_in_user_id: int
    ) -> bool:
        return token_level == "modify" and \
            Permissions.can_view_paste(paste_publicity, paste_owner_id, logged_in_user_id)

    @classmethod
    def can_delete_paste(
        cls, token_level: str, paste_owner_id: int, logged_in_user_id: int
    ) -> bool:
        # modify-level token is always required
        # in addition, user must be paste owner if the paste was not created anonymously
        return token_level == "modify" and paste_owner_id == logged_in_user_id

    @classmethod
    def can_delete_chat_message(
        cls, token_level: str, paste_owner_id: int, logged_in_user_id: int
    ) -> bool:
        # modify-level token is always required
        # if paste was not created anonymously, user is also required to be the owner
        return token_level == "modify" and \
            (paste_owner_id is None or paste_owner_id == logged_in_user_id)

    @classmethod
    def can_regenerate_tokens(
        cls, token_level: str, paste_owner_id: int, logged_in_user_id: int
    ) -> bool:
        # modify-level token is always required
        # in addition, user must be paste owner if the paste was not created anonymously
        return token_level == "modify" and \
            (paste_owner_id is None or paste_owner_id == logged_in_user_id)

    @classmethod
    def can_vote(cls, paste_publicity: str, paste_owner_id: int, logged_in_user_id: int) -> bool:
        # require that user has permission to view the paste and is logged in
        return Permissions.can_view_paste(paste_publicity, paste_owner_id, logged_in_user_id) and \
            logged_in_user_id is not None
