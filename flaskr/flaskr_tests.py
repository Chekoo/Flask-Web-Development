#coding=utf-8
import os
import flaskr
import unittest
import tempfile

class FlaskTestCase(unittest.TestCase):

    def setUp(self):   #创建一个新的测试客户端并初始化一个新的数据库，在每个独立的测试函数运行钱都会调用这个方法
        self.db_fb, flaskr.app.config['DATABASE'] = tempfile.mkstemp()   #mkstemp()返回一个低级别的文件和一个随机文件名，这个文件名后面将作为我们数据库名称
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        flaskr.init_db()

    def tearDown(self):  #在测试结束后关闭文件，并在文件系统中删除数据库，设置中TESTING标志开启的，意味着
        os.close(self.db_fb)    #在请求关闭错误捕捉，以便于在执行测试请求时得到更好的错误报告
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')   #使用self.app.get可以向指定URL发送HTTP GET请求，返回值为~flask.Flask.reponse_class对象,
        assert 'No entries here so far' in rv.data    #可以使用data属性来检查应用的返回值

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

    def test_messages(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data


if __name__ == '__main__':
    unittest.main()
