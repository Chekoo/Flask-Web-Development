#coding=utf-8

import unittest
from flask import current_app
from ..app import create_app, db


class BasicsTestCase(unittest.TestCase):
    def setUp(self):  # 创建测试环境，激活上下文，确保能在测试中使用current_app
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])