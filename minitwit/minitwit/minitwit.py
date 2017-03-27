#coding=utf-8
import time
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash
import sys
reload(sys)
sys.setdefaultencoding('utf8')


#config
DATABASE = '/tmp/minitwit.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'

#小应用，实例化Flask类，绑定到app上，从环境变量和name中引入相应的项
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)


def get_db():  #数据库连接
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db

@app.teardown_appcontext
def close_databse(exception):   #数据库关闭
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()

def init_db():   #初始化数据库，导入schema.sql文件，进行建表工作，创建了user,follower,message
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.cli.command('initdb')
def initdb_command():   #方便调用,将initdb引入命令行
    init_db()
    print ('Initialized the databse.')

def query_db(query, args=(), one=False):   #定义数据库查询操作
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

def get_user_id(username):   # 获取用户id，根据用户username向数据库里进行查询
    rv = query_db('select user_id from user where username = ?', [username], one=True)
    return rv[0] if rv else None

def format_datetime(timestamp):  #将时间戳转化成可读的时间表示格式
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')

def gravatar_url(email, size=80):  #根据email，生成在Gravater上对应头像链接，大小80*80
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)

@app.before_request
def before_request():    #在request之前先清空全局变量g的user，再向session查询是否有user_id,如果有的话返回相应的用户信息
    g.user = None        #因为提供了cookie登陆的方法，不必要求每次都手动输入信息登陆
    if 'user_id' in session:
        g.user = query_db('select * from user where user_id = ?',[session['user_id']], one=True)

@app.route('/')
def timeline():  #若用户之前没有进行登陆操作，而且本地没有cookie，将其重定向到公共的时间线页面，例如微博
    if not g.user:   #若登陆，则渲染成用户定制的时间线页面，按时间逆序显示用户本人和关注人所发的推文，和微博类似
        return redirect(url_for('public_timeline'))
    return render_template('timeline.html', messages=query_db('''
        select message.*, user.* from message, user
        where message.author_id = user.user_id and (
            user.user_id = ? or
            user.user_id in (select whom_id from follower
                                     where who_id = ?))
        order by message.pub_data desc limit?''',
        [session['user_id'], session['user_id'], PER_PAGE]))

@app.route('/public')
def public_timeline():   #为游客定制的首页，显示最近来自所有用户的推文
    return render_template('timeline.html', messages=query_db('''
    select message.*, user.* from message, user
    where message.author_id = user.user_id
    order by message.pub_data desc limit ?''', [PER_PAGE]))


@app.route('/<username>')  #动态路由，也可这样写: /<string:username>
def user_timeline(username):   #用户个人资料页面，若不存在，返回404,
    profile_user = query_db('select * from user where username = ?',
                            [username], one=True)
    if profile_user is None:
        abort(404)
    followed = False
    if g.user:
        followed = query_db('''select 1 from follower where
            follower.who_id = ? and follower.whom_id  = ?''',
            [session['user_id'], profile_user['user_id']],
            one=True) is not None
    return render_template('timeline.html', messages=query_db('''
            select message.*, user.* from message, user where
            user.user_id = message.author_id and user.user_id = ?
            order by message.pub_data desc limit ?''',
            [profile_user['user_id'], PER_PAGE]), followed=followed,
            profile_user=profile_user)


@app.route('/<username>/follow')
def follow_user(username): #用户的关注列表,提供了用户关注人的添加方法，如果没有用户，或者用户名不合法，则返回
    if not g.user:    #401和404异常
        abort(401)
    whom_id = get_user_id(username)
    if whom_id is None:
        abort(404)
    db = get_db()
    db.execute('insert into follower (who_id, whom_id) values (?, ?)',
               [session['user_id'], whom_id])
    db.commit()
    flash('已关注"%s"' % username)
    return redirect(url_for('user_timeline', username=username))

@app.route('/<username>/unfollow')
def unfollow_user(username):  #取消关注
    if not g.user:
        abort(401)
    whom_id = get_user_id(username)
    if whom_id is None:
        abort(404)
    db = get_db()
    db.execute('delete from follower where who_id=? and whom_id=?',
               [session['user_id'], whom_id])
    db.commit()
    flash('你将不再关注 "%s"' % username)
    return redirect(url_for('user_timeline', username=username))



@app.route('/add_message', methods=['POST'])
def add_message():     #发送文章，检验是否登录，只有登录过才能发送推文，否则抛出401异常
    if 'user_id' not in session:   #从表单中获取text内容，将这部分内容插入message表后重定向
        abort(401)                 #到时间线页面，显示提阿难捱过推文信息后的新页面
    if request.form['text']:
        db = get_db()
        db.execute('''insert into message (author_id, text, pub_data)
          values (?, ?, ?)''', (session['user_id'], request.form['text'],
                                int(time.time())))
        db.commit()
        flash('发送成功')
    return redirect(url_for('timeline'))

@app.route('/login', methods=['GET', 'POST'])
def login():  #登录
    if g.user:
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        user = query_db('''select * from user where
            username = ?''', [request.form['username']], one=True)
        if user is None:
            error = '无效的用户名'
        elif not check_password_hash(user['pw_hash'],
                                      request.form['password']):
            error = '密码错误'
        else:
            flash('你已登录')
            session['user_id'] = user['user_id']
            return redirect(url_for('timeline'))
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():  #注册，当用户已经合法登录，直接重定向到时间线页面
    if g.user:   #当收到get请求时，将注册页面和错误信息展示出来
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = '请输入用户名'
        elif not request.form['email'] or '@' not in request.form['email']:
            error = '请输入有效的电子邮箱'
        elif not request.form['password']:
            error = '请输入密码'
        elif request.form['password'] != request.form['password2']:
            error = '两次输入的密码不一致'
        elif get_user_id(request.form['username']) is not None:
            error = '用户名已被占用,请换一个'
        else:
            db = get_db()
            db.execute('''insert into user (
              username, email, pw_hash) values (?, ?, ?)''',
              [request.form['username'], request.form['email'],
               generate_password_hash(request.form['password'])])
            db.commit()
            flash('你已成功注册，现在可以登录')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():   #退出登录，从session查询对应的应用信息，并将该用户的相关信息从session
    flash('你已退出登录')   #弹出，显示弹出信息，重定向到公共时间线页面
    session.pop('user_id', None)
    return redirect(url_for('public_timeline'))

app.jinja_env.filters['datetimeformat'] = format_datetime
app.jinja_env.filters['gravatar'] = gravatar_url

if __name__ == "__main__":   #执行此文件
    init_db()  #初始化数据库
    app.run(debug=True)