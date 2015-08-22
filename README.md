# Lilium
Someone quetions and Someone Answers

这是一个问答网站，有人可以提问，也可以有人回答的简单知识问答网站。
它的前身是 flask-todo （https://github.com/dodoru/flask_todo）  (用来熟练ORM和SQLAlchemy的例子)
和MyFlask( https://github.com/dodoru/learn_in_python/tree/master/flask/MyFlask）. 用来熟悉sqlite3和简单的逻辑)

这个项目是一边学一边写的。 欢迎各种建议，谢谢。也希望可以和大家一起学习。
前端的页面并没有做很多修饰。只是把基本要展现的网站内容和逻辑呈现出来，所以很轻巧。

---
基本的网站功能：
1.注册
2.登陆
3.主页（登陆者可以看到自己问的问题列表，和自己参与回答的问题列表）
4.找回密码 （哈哈，真的会发送密码给注册邮箱哦，不过只发送“密码”，并没有生成链接之类的。以后再修改吧。）

---
登陆之后网站功能：
1. 题库： 可以看到其他人所提出的问题，也可以自己提问
2. 单个问题页面：可以从题库那里跳转过来，可以添加自己的回答，像是超级简陋版的论坛，（笑）
3. 设置： 目前只有重设密码的功能
4. 退出： 清除session, 会跳转到登陆页面
---
管理员的设置功能：
1 管理员的账号是 admin  (可以考虑在用户角色db_Models.USER 那里加一个角色标签，表示用户是vip,管理员，普通用户等）
2 查看用户列表，可以修改，增加，删除其他用户。建议不要删掉自己。
---
以下是简单的页面截图。
1. 未登录的用户 主页
![image](https://github.com/dodoru/Lilium/blob/master/images/index_unlog.jpg)
---
2. 登陆后的用户 查看题库
![image](https://github.com/dodoru/Lilium/blob/master/images/problems_list.jpg.jpg)
---
3. 登陆后的普通用户-设置-修改密码页面
![image](https://github.com/dodoru/Lilium/blob/master/images/settings.jpg.jpg)
---
4. 登陆后的管理员-设置-比普通用户多一个可以查看用户列表的权限
![image](https://github.com/dodoru/Lilium/blob/master/images/admin_user_list.jpg)
---
5. 登陆后的管理员-设置-用户列表-可以增加删除修改其他用户的信息
![image](https://github.com/dodoru/Lilium/blob/master/images/admin_user_list.jpg)
