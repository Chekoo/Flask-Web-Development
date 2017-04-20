#coding=utf-8
from flask import jsonify
from ..exceptions import ValidationError
from . import api


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


# API中ValidationError异常的处理程序, 只要抛出指定类的异常，就会调用被修饰的函数。
@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
