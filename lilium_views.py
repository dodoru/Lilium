# coding:utf-8
import flask
from flask import Flask, request, session, render_template, redirect, url_for, flash, make_response
from flask.ext.bootstrap import Bootstrap
from db_models import User, Problem, Solution, db

app = Flask(__name__)
bootstrap = Bootstrap(app)

DATABASE = 'db_files/db_models.db'
DEBUG = False
SECRET_KEY = 'lilium development key'

app.config.from_object(__name__)


@app.route('/')
def index():
    name = request.cookies.get('username')
    user_id = session.get('user_id')
    # Fixme
    print request.cookies, session
    return render_template('index.html', username=name)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        userdata = request.form.to_dict()
        user = User.query.filter(User.name == userdata['name']).first()
        print user

        if user:
            if user.password == userdata['password']:
                flash("login OK. Jump Jump Jump...")
                response = make_response(redirect(url_for('problems')))
                response.set_cookie('user_id', str(user.id))
                session['user_id'] = user.id
                return response
            else:
                flash("password is not matching, please input again. ")
        else:
            flash('This user dose not exist, please input again.')
    return render_template('login.html')


@app.route('/sign', methods=['POST', 'GET'])
def sign():
    if request.method == 'POST':
        userdata = request.form.to_dict()
        print 'sign - userdata: ', userdata
        if len(userdata['name']) < 3:
            flash(" The length of username should be more than 2 bytes. please input again.")
        elif userdata['password'] != userdata['password1']:
            flash(" Your passwords are different, please input again.")
        else:
            new_user = User(name=userdata['name'], password=userdata['password'], email=userdata['email'])
            db.session.add(new_user)
            try:
                db.session.commit()
            except:
                db.session.rollback()
            flash("Sign Successfully，jump to your home page now.")

            response = make_response(redirect(url_for('problems')))
            response.set_cookie('user_id', str(new_user.id))
            session['user_id'] = new_user.id
            return response
    return render_template('sign.html')


@app.route('/retrieve_password', methods=['POST', 'GET'])
def retrieve_password():
    if request.method == 'POST':
        # user_id=request.cookies.get('user_id')
        user_data = request.form.to_dict()
        print 'retrieve_password , user_data: ', user_data
        # user = alchemy_db.get_user_by_name(user_data['name'])
        user = User.query.filter(User.name == user_data['name'], User.email == user_data['email']).first()
        print user
        if user:
            flash("(●'◡'●),已经将密码发到你注册的邮箱，请查收验证。")
            # fixme
        else:
            flash("咦？ 这个邮箱还没有注册耶~ .../n  (●'◡'●) come on ，baby  ❤ ~ ")
    return render_template('retrieve_password.html')


@app.route('/settings/<name>', methods=['POST', 'GET'])
def settings(name):
    # user_id = request.cookies.get('user_id')
    user_id = session.get('user_id')
    user = User.query.get(int(user_id))
    if user.name == name:
        url = '/settings/' + str(name)
        if request.method == 'POST':
            user_password = request.form.to_dict()
            if user_password['password'] == user_password['password1']:
                user.password = user_password['password']
                db.session.add(user)
                db.session.commit()
                flash('you have reset your password .')
                return '<h2> you have reset your password .</h2> '
        return render_template('settings.html', username=name, action_url=url)
    else:
        return redirect(url_for('login'))
        # 必须是当前用户才可以修改密码,如果不是就要重新登陆


@app.route('/problems', methods=['POST', 'GET'])
def problems():
    user_id = session.get('user_id')
    # user_id = request.cookies.get('user_id')
    if not user_id:
        return flask.redirect(flask.url_for('login'))

    user = User.query.get(int(user_id))
    print "problems_page_log:", user
    if request.method == 'POST':
        problem_data = request.form.to_dict()
        print "problem_data : ", problem_data
        if len(problem_data['title']) <= 2:
            flash("<h1>the title should more than 2 bytes </h1>")
        else:
            new_problem = Problem(title=problem_data['title'], detail=problem_data['detail'], creator_id=user_id)
            db.session.add(new_problem)
            try:
                db.session.commit()
            except:
                db.session.rollback()
    problems_data = Problem.query.all()
    return render_template('problems_list.html', problems=problems_data, username=user.name)


@app.route('/problems/<problem_id>', methods=['POST', 'GET'])
def problem_id(problem_id):
    user_id = session.get('user_id')
    # user_id = request.cookies.get('user_id')
    problem_data = Problem.query.get(int(problem_id))

    print "problem_data ", problem_data
    if not problem_data:
        return '<h1> 你跑到了海洋的虫洞里了。 <h1>', 404

    if request.method == 'POST':
        solution_data = request.form.to_dict()
        new_solution = Solution(detail=solution_data['detail'], candidate_id=user_id, problem_id=int(problem_id))
        db.session.add(new_solution)
        db.session.commit()

    # solutions_data=Solution.query.filter(Solution.problem==int(problem_id)).all()
    # print solutions_data
    solutions_data = Solution.query.filter(Solution.problem_id == int(problem_id)).all()
    print solutions_data
    return render_template('problem_id.html', problem=problem_data, solutions=solutions_data)


@app.route('/settings/user/list', methods=['POST', 'GET'])
def user_list():
    user_id = session.get('user_id')
    user = User.query.get(int(user_id))
    # username = request.cookies.get('username')
    if user.name == 'admin':
        users = User.query.all()
        return render_template('user_list.html', users=users)
    else:
        return "<h1> 当前用户无权限查看该页面</h1>"


# 添加一个新用户
# only admin can operate other users information
@app.route('/settings/user/add', methods=['POST', 'GET'])
def add_user():
    username = request.cookies.get('username')
    if username == 'admin':
        if request.method == 'POST':
            userdata = request.form.to_dict()
            if userdata['password'] == userdata['password1']:
                del userdata['password1']
                print userdata
                for i in userdata:
                    userdata[i] = userdata[i].encode('utf-8')
                user.save(userdata)
                print "add user OK : ", userdata
                usersdata = user.load()
                return flask.redirect(flask.url_for('settings/user/list'))
                # FIXME 添加成功后，进入 user_list 页面，查看资料
            else:
                return render_template('user_add.html', tips="<h1>输入密码前后不一致，请重新设置</h1>")
        return render_template('user_add.html')
    # return flask.redirect(flask.url_for('login'))
    return "<h1> 当前用户无权限查看该页面</h1>"


# /user/list
# 显示所有用户，以 table 的形式，带有 th 标签（表格头）
# 这个页面每个 条目 的最右边有一个 edit 超链接，点击跳转到 edit 页面



'''
/user/edit/<id>
    编辑这个用户的资料（就是密码和 email 可以编辑）
    这个页面由 list 页面跳转而来，id不存在（如果手动输入一个不存在的id）就404
    成功后跳转到 list 页面
    失败后停留在这个页面
'''


@app.route('/settings/user/edit/<id>', methods=['POST', 'GET'])
def edit_user(id):
    user_id = session.get('user_id')
    user = User.query.get(int(user_id))
    # user_id=request.cookies.get('user_id')
    if user.name == 'admin':
        if request.method == 'POST':
            user_data = request.form.to_dict()
            # user.update(id, user_data) FIXME
            update_user = User()
            users_data = user.load()

            return render_template('user_list.html', user_id=id, users_info=users_data, default_info=default_user)
        return render_template('user_edit.html', user_id=id)
    else:
        return "<h1> 当前用户无权限查看该页面</h1>"


'''
/user/delete/<id>
    删除这个用户
    成功后跳转到 list 页面
    失败后也跳转到 list 页面（一般不会失败，所以先不管）
#  绝对黑魔法
'''


@app.route('/settings/user/delete/<id>', methods=['POST', 'GET'])
def delete_user(id):
    username = request.cookies.get('username')
    if username == 'admin':
        print 'delete user data : ', user.search_id(id)
        user.delete(id)
        return render_template('user_list.html')
    else:
        return "<h1> 当前用户无权限查看该页面</h1>"


'''
@app.errolhandler(404)
def page_not_found():
    return "<h1>page not found</h1>",404
'''

if __name__ == '__main__':
    app.debug = True
    app.run()



