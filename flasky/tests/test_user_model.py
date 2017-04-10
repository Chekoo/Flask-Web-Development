#coding=utf-8

import unittest
from ..app.models import User
from ..app.models import Role, Permission, AnonymousUser

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password = 'cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password = 'cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_vertification(self):
        u = User(password = 'cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password != u2.password_hash)

    def test_roles_and_permissioins(self):
        Role.insert_roles()
        u = User(email='admin@163.com', password='admin')
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertTrue(u.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertTrue(u.can(Permission.FOLLOW))
