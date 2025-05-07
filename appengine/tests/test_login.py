import unittest

from components.login_components import check_user_password, register_user

class TestLoginComponents(unittest.TestCase):
    def setUp(self):
        self.users = {
            'test': 'password123',
            'user': 'mypassword'
        }
    
    def test_check_user_password_valid(self):
        self.assertTrue(check_user_password('test', 'password123', self.users))
        self.assertTrue(check_user_password('user', 'mypassword', self.users))
        self.assertFalse(check_user_password('test', 'wrongpassword', self.users))
    
    def test_register_user(self):
        new_users = register_user('newuser', 'newpassword', self.users)
        self.assertIn('newuser', new_users)
        self.assertEqual(new_users['newuser'], 'newpassword')
        self.assertEqual(len(new_users), 3)
