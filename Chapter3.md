# 模板

视图函数的作用：生成请求的响应

业务逻辑、表现逻辑
把表现逻辑移到模板中能够提升程序的可维护性。

模板是一个包含响应文本的文件，包含用占位变量表示的动态部分，具体指爱请求的上下文才知道。
使用真实值替代变量，再返回最终得到的响应字符串，这一过程称为 __渲染__

## Jinja2模板引擎
Flask在程序文件夹的templates子文件夹中寻找模板，
render_template函数把Jinja2模板引擎集成到了程序中,第一个参数为模板文件名，随后参数都是键对值，表示模板中变量对应的真实值。

Jinja2能识别所有类型的变量，可以使用过滤器修改变量,下面模板以首字母大写形式显示变量name的值

    Hello, {{ name|capitalize }}
safe    渲染值时不转义  <br>
capitalize   首字母大写  <br>
lower  小写  <br>
upper  大写  <br>
title  每个单词首字母大写  <br>
trim  首尾空格去掉  <br>
striptags  渲染之前把值中所有的HTML标签都删掉。<br><br>
__出于安全考虑，Jinja2会转义所有变量。千万别在不可信的值上使用safe过滤器，例如用户在表单中输入的文本__

条件控制语句:

    {% if user %}
        Hello, {{ user }}!
    {% else %}
        Hello, Stranger!
    {% endif %}
渲染一组元素:

    <ul>
        {% for comment in comments %}
            <li>{{ comment }}</li>
        {% endfor %}
    </ul>
Jinja2还支持宏:

    {% macro render_comment(comment) %}
        <li>{{ comment }}</li>
    {% endmacro %}

    <ul>
        {% for comment in comments %}
            {{ render_comment(comment) }}
        {% endfor %}
    </ul>
需要在多处重复使用的模板代码片段可以写入单独的文件，再包含在所有模板中，以避免重复。

    {% include 'comment.html' %}
另一种重复使用代码的方式是 __模板继承__
block标签定义的元素可在衍生模板中修改。

## Bootstrap
Boostrap是一个 __Twitter__ 开发的一个开源框架，它提供的用户界面组件可用于创建整洁且具有吸引力的网页。<br>
它是客户端框架，不会涉及到服务器。服务器要做的是提供引用了Bootstrap层叠样式表和JavaScript文件的HTML响应，并在HTML、CSS和JavaScript代码中实例化所需组件。这些操作最理想的执行场所就是模板。
Flask-Bootstrap,简化集成的过程。
Flask扩展一般都在创建程序实例时初始化。

如果程序需要向已经有内容的块中添加新内容，必须使用Jinja2的super()函数。

    {% block scripts %}
    {{ super() }}
    <script type="text/javascript" src="my-script.js"></script>
    {% endblock %}

### 链接
任何具有多个路由的程序都需要可以连接不同页面的链接，例如导航条。
Flask提供了url_for()辅助函数，它可以使用程序URL映射中保存的信息生成URL。
url_for()函数最简单的用法是以视图函数名作为参数，返回对应的URL。<br>
使用url_for()生成动态地址时，将动态部分作为关键字参数传入。

### 静态文件
默认设置下，Flask在程序跟目录中名为static的自目录中寻找静态文件。


## Flask-Moment本地化日期和时间
服务器需要统一时间单位，这和用户所在的地理位置无关，所以一般使用协调时间时(Coordinated Universal Time, UTC)。<br>
要想在服务器上只使用UTC时间，把时间单位发送给Web浏览器，转换成当地时间，然后渲染。<br>
有一个使用JavaScript开发的优秀客户端开源代码库，名为 __moment.js__，它 可以在浏览器中渲染日期和时间。 __Flask-Moment__ 可以把moment.js集成到Jinja2模板中。
Flask-Moment还依赖jquery.js.
