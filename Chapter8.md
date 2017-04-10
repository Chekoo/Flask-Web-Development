# 用户认证
用户连接程序后会进行身份认证，让程序知道用户身份，提供有针对性的体验。

## 认证扩展
* Flask-Login 管理已登录用户的用户会话
* Werkzeug    计算密码散列值并进行核对
* itsdangerous  生成并核对加密安全令牌
* Flask-Mail    发送与认证相关的电子邮件
* Flask-Bootstrap HTML模板
* Flask-WTF     Web表单

## 密码安全性
存储密码的散列值。计算密码散列值的函数接收密码作为输入，使用一种或多种加密算法转换密码，
得到一个和原始密码没有关系的字符序列，核对密码时，密码散列值可代替原始密码，因为计算散列值的函数是可复现的：
只要输入一样，结果就一样。
## 使用Werkzeug实现密码散列
Werkzeug中的security模快可以方便的实现密码散列值的计算。

     generate_password_hash(password, method=pbkdf2:sha1, salt_length=8):这个函数将原始密码作为输入，
     以字符串形式输出密码的散列值，输出的值可保存在用户数据库中。

     check_password_hash(hash, password)这个函数的参数是从数据库中取回的密码散列值和用户输入的密码，返回值为True表明密码正确


## 认证蓝本
把创建程序的过程移入工厂函数后，可以使用蓝本在全局作用域中定义路由。与用户认证系统相关的路由可在auth蓝本正定义。<br>
对于不同的程序功能，使用不同的蓝本，这是保持代码整齐有序的好方法。

## Flask-Login认证用户
用来管理用户认证系统中的认证状态，且不依赖特定的认证机制。
UserMixin类，其中包含了方法的默认实现，且能满足大多数需求。

## 使用itsdangerous生成确认令牌
把URL中的id换成相同信息安全加密后得到的令牌<br>
itsdangerous提供了多种生成令牌的方法，TimeJSONWebSignatureSerializer类生成具有过期时间的JSON WEB
签名。<br>
dumps()为指定的数据生成一个加密签名，然后再对数据和签名进行序列化。生成令牌字符串。
解码令牌，用loads()。


__如果before_request或before_app_request的回调返回响应或重定向，Flask会直接将其发送到客户端，不会调用请求的视图函数，因此，这些回调可在必要时拦截请求。__