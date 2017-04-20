#coding=utf-8
from flask_httpauth import HTTPBasicAuth
from flask import g, jsonify
from . import api
from ..models import User, AnonymousUser
from .errors import unauthorized, forbidden

auth = HTTPBasicAuth()


# 初始化Flask-HTTPAuth
# 支持令牌的改进验证回调
@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


# Flask-HTTPAuth错误处理程序
@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


# 在before_request处理程序中进行认证
@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden('Unconfirmed accounnt')

# 生成认证令牌
@api.route('/token')
def get_token():
    if g.current_user.is_anonymous() or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(expiration=3600), 'expiration': 3600})