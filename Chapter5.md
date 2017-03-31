# 数据库
数据库按照一定的规则保存程序数据，程序再发起查询取回所需的数据。Web程序最常用基于关系模型的
数据库，这种数据库也称为SQL数据库。因为它们使用结构化查询语言。近几年流行 __文档数据库__
和 __键值对数据库__成了最流行戴尔替代选择，这两种数据库合称NoSQL数据库。

## NoSQL数据库
NoSQL数据库一般使用集合代替表，使用文档代替记录。
NoSQL数据库采用的设计方式使联结变得困难，所以大多数数据库不支持这种操作。<br>
NoSQL好处: 数据重复可以提升查询速度。


SQL数据库擅于用高校且紧凑的形式存储结构化数据，需要花费大量精力保证数据的一致性
NoSQL放宽了对一致性的要求，获得了性能上的优势。

## ORM
数据库抽象层，也称为对象关系映射(Object-Relational Mapper, ORM)或对象文档映射(Object-Document Mapper, ODM)
,在用户不知觉的情况下把高层的面向对象操作转换成底层的数据库指令。

## Flask-SQLAlchemy
Flask-SQLAlchemy是一个Flask扩展，简化了Flask程序中使用SQLAlchemy的操作。

### 模型
模型表示程序使用的持久化实体，在ORM中，模型一般是一个Python类，类中的属性对应数据库表中的列
__repr()__ 方法，返回一个具有可读性的字符串表示模型，可在调试和测试时使用。

    class Role(db.Model):
        # ...
        users = db.relationship('User', backref='role')


    class User(db.Model):
        # ...
        role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

添加到User模型中的role_id列被定义为外键。
传给db.ForeignKey()的参数'role.id'表明这列是roles表中行的id值。<br>

添加到Role模型中的user属性代表这个关系的面向对象视角。对于一个Role类的实例，其users属性将返回与角色相关联的用户组成的列表。

### 数据库操作
创建数据库，使用db.create_all()，更新现有数据库表的粗暴方式是先删除再重新出创建。
db.drop_all()
db.create_all()

构造对象，准备把对象写入数据库之前，先要将其添加到会话中，然后调用commit()提交会话，
__数据库会话也称为事务__<br>
数据库会话能保证数据库的一致性。提交操作把会话中的对象全部写入数据库。
<br>会话也可以回滚。db.session.rollback()

删除与插入和更新一样，提交数据库会话后才会执行。<br>
Flask-SQLAlchemy为每个模型类都提供了query对象。

使用过滤器可以配置query对象进行更精准的数据库查询。<br>
filter_by()等过滤器在query对象上调用。返回一个更精确的query对象。<br>
all()以列表形式返回查询的所有结果。

### 集成Python shell
想把对象添加到导入列表中，我们要为shell命令注册一个make_context回调函数。
make_shell_context()函数注册了程序、数据库实例以及模型，因此这些对象能直接导入shell。

### 使用Flask-Migrate实现数据库迁移
更新表的更好方法是使用数据库迁移框架，源码版本控制工具可以跟踪源码文件的变化。
SQLAlchemy主力开发人员编写了一个迁移框架，称为Alembic，Flask程序还可使用Flask-Migrate扩展。
这个扩展对Alembic做了轻量级包装，并集成到Flask-Script中，所有操作都通过Flask-Script命令完成。

数据库迁移仓库中的文件要和程序的其他文件一起纳入版本控制。

Alembic中，数据库迁移用迁移脚本表示，脚本中有两个函数，分别是upgrade()和downgrade()。
upgrade()把迁移中的改动应用到数据库中，downgrade()则将改动删除


