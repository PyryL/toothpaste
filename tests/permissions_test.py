import unittest
from utilities.permissions import Permissions

class TestPermissions(unittest.TestCase):
    def test_view_permission_listed_paste(self):
        self.assertTrue(Permissions.can_view_paste("listed", 42, None))
        self.assertTrue(Permissions.can_view_paste("listed", 42, 15))
        self.assertTrue(Permissions.can_view_paste("listed", 42, 42))

    def test_view_permission_unlisted_paste(self):
        self.assertTrue(Permissions.can_view_paste("unlisted", 42, None))
        self.assertTrue(Permissions.can_view_paste("unlisted", 42, 15))
        self.assertTrue(Permissions.can_view_paste("unlisted", 42, 42))

    def test_view_permission_private_paste(self):
        self.assertFalse(Permissions.can_view_paste("private", 42, None))
        self.assertFalse(Permissions.can_view_paste("private", 42, 15))
        self.assertTrue(Permissions.can_view_paste("private", 42, 42))


    def test_modify_permission_view_token(self):
        self.assertFalse(Permissions.can_modify_paste("view", "listed", 42, 42))

    def test_modify_permission_modify_token(self):
        self.assertTrue(Permissions.can_modify_paste("modify", "listed", 42, 15))
        self.assertTrue(Permissions.can_modify_paste("modify", "unlisted", 42, None))
        self.assertFalse(Permissions.can_modify_paste("modify", "private", 42, 15))


    def test_delete_paste_permission_view_token(self):
        self.assertFalse(Permissions.can_delete_paste("view", 42, 42))

    def test_delete_paste_permission_modify_token(self):
        self.assertFalse(Permissions.can_delete_paste("modify", 42, None))
        self.assertFalse(Permissions.can_delete_paste("modify", 42, 15))
        self.assertTrue(Permissions.can_delete_paste("modify", 42, 42))
        self.assertTrue(Permissions.can_delete_paste("modify", None, 42))
        self.assertTrue(Permissions.can_delete_paste("modify", None, None))


    def test_chat_message_delete_permission_view_token(self):
        self.assertFalse(Permissions.can_delete_chat_message("view", 42, 42))

    def test_chat_message_delete_permission_modify_token(self):
        self.assertFalse(Permissions.can_delete_paste("modify", 42, None))
        self.assertFalse(Permissions.can_delete_paste("modify", 42, 15))
        self.assertTrue(Permissions.can_delete_paste("modify", 42, 42))
        self.assertTrue(Permissions.can_delete_paste("modify", None, 42))
        self.assertTrue(Permissions.can_delete_paste("modify", None, None))


    def test_token_regeneration_permission_view_token(self):
        self.assertFalse(Permissions.can_delete_chat_message("view", 42, 42))

    def test_token_regeneration_permission_modify_token(self):
        self.assertFalse(Permissions.can_delete_paste("modify", 42, None))
        self.assertFalse(Permissions.can_delete_paste("modify", 42, 15))
        self.assertTrue(Permissions.can_delete_paste("modify", 42, 42))
        self.assertTrue(Permissions.can_delete_paste("modify", None, 42))
        self.assertTrue(Permissions.can_delete_paste("modify", None, None))


    def test_vote_permission_when_available(self):
        self.assertTrue(Permissions.can_vote("listed", None, 42))

    def test_vote_permission_anonymous_user(self):
        self.assertFalse(Permissions.can_vote("listed", 42, None))
        self.assertFalse(Permissions.can_vote("listed", None, None))

    def test_vote_permission_without_view_permission(self):
        self.assertFalse(Permissions.can_vote("private", 42, 15))
