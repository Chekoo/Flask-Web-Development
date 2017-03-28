# Flask
Flask是一个小型框架

Flask两个依赖:  路由、调试和Web服务器网关接口(Web Server GateWay Interface, WSGI)

子系统由Werkzeug提供，模板系统由Jinja2提供。Werkzeug和Jinja2都由核心开发者开发而成。

## 虚拟环境:
python解释器的一个私有副本,在这个环境中你可以安装私有包,不会影响系统中安装的全局python解释器.

git checkout 1a   把程序文件夹切换到'1a'版本,即程序的初始版本

## virtualenv venv  创建python虚拟环境
文件夹中有一个名为venv的子文件夹,它保存一个全新的虚拟环境,其中有一个私有的python解释器.

使用虚拟环境之前,必须要将其激活
source venv/bin/activate   Linux
venv\Sripts\activate       Windows

激活后,python解释器的路徑就被添加进PATH中,但这种改变不是永久性的,它只会影响到当前的命令行会话.

which python可以查看当前使用的环境

退出虚拟环境,回到全局Python解释器中:  deactivate

