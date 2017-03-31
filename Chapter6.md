# 电子邮件

## Flask-Mail
Flask-Mail提供电子邮件支持，Flask-Mail连接到简单邮件传输协议(Simple Mail Transfer Protocol, SMTP)服务器，并
把邮件交给这个服务器发送。如果不配置，它会连接localhost上的端口25，无需验证即可发送电子邮件。

    建议：永远不要将账户证书直接写在你的脚本里面，尤其是如果你打算将你的的工作开源。为了保护你的帐户信息，必须让脚本从你的配置环境中导入敏感信息。

持有email服务器用户名和密码的两个变量需要在环境中定义。如果你是使用Linux或Mac OS X上的bash，你可以设置这些变量如下：

    (venv) $ export MAIL_USERNAME="Gmail username"
    (venv) $ export MAIL_PASSWORD="Gmail password"
对于Windows用户，可以设置环境变量如下：

    (venv) $ set MAIL_USERNAME="Gmail username"
    (venv) $ set MAIL_PASSWORD="Gmail password"

为了测试配置，你可以开启一个shell会话并发送测试email：

    (venv) $ python hello.py shell
    >>> from flask.ext.mail import Message
    >>> from hello import mail
    >>> msg = Message('test subject', sender='you@example.com',
    ... recipients=['you@example.com'])
    >>> msg.body = 'text body'
    >>> msg.html = '<b>HTML</b> body'
    >>> with app.app_context():
    ... mail.send(msg)
    ...
注意，Flask-Mail的send()函数使用current_app，所以它需要执行已激活的应用程序上下文。