# coding:utf-8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import sql

app = Flask(__name__)
app.secret_key = 'secret database key'
app.debug = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_files/db_models.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime(timezone=True), default=sql.func.now())

    def __repr__(self):
        return u"< {0} , {1} >".format(self.name, self.email)


class Problem(db.Model):
    __tablename__ = 'problems'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    detail = db.Column(db.String(500))

    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = db.relationship('User', backref='problems')

    def __repr__(self):
        return u"< problem_id:{0},{1},cid: {2} >".format(self.id, self.title, self.creator_id)


class Solution(db.Model):
    __tablename__ = 'solutions'
    id = db.Column(db.Integer, primary_key=True)
    detail = db.Column(db.String(1000), nullable=False)
    score = db.Column(db.Integer, default=0)
    candidate_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    candidate = db.relationship('User', backref='solutions')
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'))
    problem = db.relationship('Problem', backref='solutions')

    def __repr__(self):
        return u"< solution_id:{0},{1},cid:{2},pid:{3} >".format(self.id, self.detail, self.candidate_id,
                                                                 self.problem_id)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    print('rebuild database')