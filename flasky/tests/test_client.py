#coding=utf-8

import unittest
import re
from flask import url_for
from ..app import db, create_app
from ..app.models import User, Role


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue('Stranger' in response.get_data(as_text=True))

    def test_register_and_login(self):
        # 注册新用户
        response = self.client.post(url_for('auth.register'), data={
            'email': 'a316296241@gmail.com',
            'username': 'Maple',
            'password': 'admin',
            'password2': 'admin'
        })
        self.assertTrue(response.status_code == 302)

        # 使用新注册的账户登录
        response = self.client.post(url_for('auth.login'), data={
            'email': 'a316296241@gmail.com',
            'password': 'admin'
        }, follow_redirects = True)
        data = response.get_data(as_text=True)
        self.assertTrue(re.search('Hello,\s+Maple!', data))
        self.assertTrue('You have not confirmed your account yet' in data)

        # 发送确认令牌
        user = User.query.filter_by(email='a316296241@gmail.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have confirmed your account' in data)

        # 退出
        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have been logged out' in data)









