# 博客文章

本章实现主要功能，允许用户阅读、撰写博客文章。
重用模板，分页显示长列表、处理富文本。

current_user由Flask-Login提供，和所有上下文变量一样，也是通过
线程内的代理对象实现。这个对象的表现类似用户对象，但实际上却是一个轻度包装，包含真正的用户对象。
数据库需要真正的用户对象，因此要调用_get_current_obect()方法。<br>

维护两个完全相同的HTML片段可不是一个好主意，Jinja2提供的include()指令就很有用

    {% include 'xxx.html' %}
## 分页显示长博客文章列表
要实现博客文章分页，我们需要一个包含大量数据的测试数据库。
有多个Python包可用于生成虚拟信息，其中ForgerPy功能比较完善<br>
__ForgerPy__并不是这个程序的依赖，因为它只在开发过程中使用。为了区分生产环境的依赖和开发环境的依赖，换成requirements文件夹。

虚拟对象属性由ForegeryPy的随机信息生成器生成。有时会有重复的，提交数据库会话会抛出IntegerityError异常，处理方式为：在继续操作之前回滚会话，在循环中生成重复内容是不会把用户写入数据库，。
offset()查询过滤器，这个过滤器会跳过参数中指定的记录数量，通过设定一个随机的偏移值，再调用first()方法，就能每次获得一个不同的随机用户。

paginate()，页数是第一个参数，也是唯一必需的参数。另外可选参数为per_page和error_out
error_out，设置为True，如果超出范围，返回404，设置为false，超出范围返回空列表。
per_page参数用来指定每页显示的记录数量，如果没有指定，默认为20个记录<br>
paginate()方法返回一个Pagination类对象，这个类在Flask-SQLAlchemy中定义。包含很多属性，用于
在模板中生成分页链接，因此将其作为参数传入了模板。

## 使用Markdown和Flask-PageDown支持富文本文章
PageDown: 使用JavaScript实现的客户端Markdown到HTML的转换程序
Flask-PageDown： 把PageDown集成到Flask-WTF表单中
Markdown: 使用Python实现的服务器端Markdown到HTML的转换程序。
Bleach： 使用Python实现的HTML清理器

Flask-PageDown使用前，要初始化<br>
Markdown使用PageDown库生成，因此要在模板中修改。Flask-PageDown简化了这个过程，提供一个模板宏，从CDN中加载所需文件。

__在创建博客文章时候做一次性转换，文章的Markdown原文本还要保存在数据库中，以防需要编辑。__

真正的转换分3步：
1. markdown()函数初步把Markdown文本转化成HTML
2. 把得到的结果和允许使用的HTML标签列表传给clean()函数。clean()函数删除所有不在白名单的标签
3. 最后一步由linkify()完成，这个函数由Bleach提供，把纯文本中的URL转换成适当的<a>链接。


渲染HTML格式内容使用| safe后缀，其目的是告诉Jinja2不要转义HTML元素。
出于安全考虑，默认情况下Jin2会转义所有模板变量。