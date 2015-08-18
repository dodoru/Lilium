# coding:utf-8

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import sql

app = Flask(__name__)
app.secret_key = 'secret database key'
app.debug = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_files/lilium.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime(timezone=True), sql.func.now())

    def __repr__(self):
        return "< users_id:{0},{1},{2}".format(self.id, self.name, self.email)


class Problem(db.Model):
    __tablename__='problems'
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),unique=True,nullable=False)
    detail=db.Column(db.String(500))

    creator_id=db.Column(db.Integer,db.ForeignKey)
    creator=db.relationship('User',backref='problems')

    def __repr__(self):
        return