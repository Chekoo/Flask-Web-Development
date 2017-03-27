#coding=utf-8
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)