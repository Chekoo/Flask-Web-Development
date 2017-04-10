# 用户角色

        def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()
通过查找角色名找现有的角色，然后再进行更新。当数据库没有这个角色时创建这个对象。<br>
要想添加新角色，或者修改角色的权限， __修改roles数组，再运行函数__ 即可。

    python manage.py shell
    >>> Role.insert_roles()
    >>> Role.query_all()

## 赋予角色
管理员由保存在设置变量FLASKY_ADMIN中的电子邮件识别，只要这个邮件地址出现在请求注册中，就被赋予正确的角色。


__上下文处理器可以让变量在所有模板中全局可访问__