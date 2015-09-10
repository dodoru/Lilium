# coding:utf-8
import flask
from flask import Flask, request, session, render_template, redirect, url_for, flash, make_response
from flask.ext.bootstrap import Bootstrap
from db_models import User, Problem, Solution, db
from send_email import send_email

app = Flask(__name__)
bootstrap = Bootstrap(app)

DATABASE = 'db_files/db_models.db'
DEBUG = False
SECRET_KEY = 'lilium development key'

app.config.from_object(__name__)


@app.route('/')
def index():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(int(user_id))
        my_problems = Problem.query.filter(Problem.creator_id == int(user_id)).all()
        my_solutions = Solution.query.filter(Solution.candidate_id == int(user_id)).group_by(Solution.problem_id)
        return render_template('index.html', username=user.name, my_problems=my_problems, my_solutions=my_solutions)
    else:
        return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('user_id'):
        session.__delitem__('user_id')
    if request.method == 'POST':
        userdata = request.form.to_dict()
        user = User.query.filter(User.name == userdata.get('name')).first()
        print user

        if user:
            if user.password == userdata.get('password'):
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
        if len(userdata.get('name')) < 3:
            flash(" The length of username should be more than 2 bytes. please input again.")
        elif userdata.get('password') != userdata.get('password1'):
            flash(" Your passwords are different, please input again.")
        else:
            del userdata['password1']
            # new_user = User(name=userdata['name'], password=userdata['password'], email=userdata['email'])
            new_user = User(**userdata)
            db.session.add(new_user)
            try:
                db.session.commit()
                flash("Sign Successfully，jump to your home page now.")
            except:
                db.session.rollback()
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
        user = User.query.filter(User.name == user_data['name'], User.email == user_data['email']).first()
        print user
        if user:
            send_email(str(user.email), user.password)
            return "<h1>你好，{0} 。已经将密码发到你的邮箱 <b> {1} </b> , 请查收验证。</h1>".format(user.name, user.email)
        else:
            flash("咦？ 这个邮箱还没有注册耶~ .../n  (●'◡'●) come on ，baby  ❤ ~ ")
    return render_template('retrieve_password.html')


@app.route('/settings/<name>', methods=['POST', 'GET'])
def settings(name):
    # user_id = request.cookies.get('user_id')
    user_id = session.get('user_id')
    if user_id:
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
    if not user_id:
        return flask.redirect(flask.url_for('login'))
    else:
        user = User.query.get(int(user_id))
        problem_data = Problem.query.get(int(problem_id))
        if not problem_data:
            return '<h1> 你跑到了海洋的虫洞里了。 <h1>', 404
        else:
            if request.method == 'POST':
                solution_data = request.form.to_dict()
                if solution_data['detail']:
                    new_solution = Solution(detail=solution_data['detail'], candidate_id=user.id,
                                            problem_id=int(problem_id))
                    db.session.add(new_solution)
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()

        solutions_data = Solution.query.filter(Solution.problem_id == int(problem_id)).all()
        return render_template('problem_id.html', problem=problem_data, solutions=solutions_data, username=user.name)


# only admin can check out the information of users
@app.route('/settings/user/list', methods=['POST', 'GET'])
def user_list():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    else:
        user = User.query.get(int(user_id))
        if user.name == 'admin':
            users = User.query.all()
            return render_template('user_list.html', username=user.name, users=users)
        else:
            return "<h1> 当前用户无权限查看该页面</h1>"


# only admin can operate other users information
@app.route('/settings/user/add', methods=['POST', 'GET'])
def add_user():
    # user_id = request.cookies.get('user_id')
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    else:
        user = User.query.get(int(user_id))
        if user.name == 'admin':
            if request.method == 'POST':
                userdata = request.form.to_dict()
                new_user = User(name=userdata['name'], password=userdata['password'], email=userdata['email'])
                db.session.add(new_user)
                try:
                    db.session.commit()
                except:
                    db.session.rollback()

            users = User.query.all()
            response = make_response(redirect(url_for('user_list', username=user.name, users=users)))
            return response
        else:
            return "<h1> 当前用户无权限查看该页面</h1>"


@app.route('/settings/user/edit/<id>', methods=['POST', 'GET'])
def edit_user(id):
    user_id = session.get('user_id')
    # user_id=request.cookies.get('user_id')
    target_user = User.query.get(int(id))

    if user_id:
        user = User.query.get(int(user_id))
        if user.name == 'admin':
            if request.method == 'POST':
                user_data = request.form.to_dict()
                ''' # 按照表格的字典更新用户数据 ,无效更改 Fixme
                for k, v in user_data.items():
                    target_user.k = v
                    print target_user, target_user.k
                '''
                target_user.name = user_data['name']
                target_user.email = user_data['email']
                target_user.password = user_data['password']
                db.session.add(target_user)

                try:
                    db.session.commit()
                except:
                    db.session.rollback()

                users = User.query.all()
                response = make_response(redirect(url_for('user_list', username=user.name, users=users)))
                return response
            return render_template('user_edit.html', username=user.name, target_user=target_user)
    else:
        return "<h1> 当前用户无权限查看该页面</h1>"


@app.route('/settings/user/delete/<id>', methods=['POST', 'GET'])
def delete_user(id):
    user_id = session.get('user_id')
    # user_id = request.cookies.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    else:
        user = User.query.get(int(user_id))
        if user.name == 'admin':
            ur = User.query.get(int(id))
            db.session.delete(ur)
            try:
                db.session.commit()
            except:
                db.session.rollback()

            print 'delete user data : ', ur
            users = User.query.all()
            response = make_response(redirect(url_for('user_list', username=user.name, users=users)))
            return response
        else:
            return "<h2> 当前用户无权限查看该页面</h2>"


'''
@app.errorhandler(404)
def page_not_found():
    return "<h1>page not found</h1>", 404
'''

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')



