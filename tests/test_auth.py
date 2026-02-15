import unittest
import os
import json
from app.models import UserManager, System

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.user_file = "test_users.json"
        if os.path.exists(self.user_file):
            os.remove(self.user_file)
        self.um = UserManager(data_file=self.user_file)

    def tearDown(self):
        if os.path.exists(self.user_file):
            os.remove(self.user_file)

    def test_default_admin(self):
        # Should create default admin
        admin = self.um.verify_login("admin", "admin")
        self.assertIsNotNone(admin)
        self.assertEqual(admin.role, "admin")

    def test_create_users(self):
        # Create Ref
        ref = self.um.create_user("ref1", "pass", "referee")
        self.assertEqual(ref.role, "referee")
        
        # Create Rep
        rep = self.um.create_user("rep1", "pass", "rep", team_id=10)
        self.assertEqual(rep.role, "rep")
        self.assertEqual(rep.team_id, 10)
        
        # Verify persistence
        self.um.save_data()
        new_um = UserManager(data_file=self.user_file)
        loaded_rep = new_um.verify_login("rep1", "pass")
        self.assertEqual(loaded_rep.team_id, 10)

    def test_login_fail(self):
        user = self.um.verify_login("admin", "wrongpass")
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()
