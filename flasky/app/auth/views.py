#coding=utf-8

from flask import render_template
from . import auth

# 蓝本中的路由和视图函数
@auth.route('/login')
def login():
    return render_template('auth/login.html')