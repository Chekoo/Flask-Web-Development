#coding=utf-8
# all the imports
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
import os

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create out little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():   #连接数据库
    return sqlite3.connect(app.config['DATABASE'])

def init_db():                  #当我们连接到数据库是，我们得到一个提供指针的连接对象db
    with closing(connect_db()) as db:   #帮助函数允许我们在with代码块保持数据库连接
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():   #这个视图把条目作为字典传递给show_entries.html模板，返回渲染结果
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods = ['POST'])
def add_entry():   #检查用户是否已经登录(检查会话中是否有logged_in键，对应值是否True
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():  #登录函数 如果通过验证，键值为True并重定向到show_entries页面,闪现一个信息，告诉用户登录成功
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():   #使用字典pop方法并传递第二个参数（键的缺省），当字典有这个键就会删除这个键，否则什么也不做
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()

























