# coding:utf-8

import os
# import ipdb
from flask.ext.mail import Mail
from flask.ext.mail import Message
from flask import Flask, render_template

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASK_MAIL_SUBJECT_PREFIX'] = 'Lilium Accounts'
app.config['FLASKY_MAIL_SENDER'] = '1372488211@qq.com'

mail = Mail(app)


# todo, 发送邮件找回密码
# def send_email(to, subject, template, **kwargs):
def send_email(to_email, body):
    msg = Message(app.config['FLASK_MAIL_SUBJECT_PREFIX'], sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to_email])
    # msg.body=render_template(template+'.txt',**kwargs)
    # msg.html=render_template(template+'.html',**kwargs)
    msg.body = 'text body'
    msg.html = '<br><h3>your password for Lilium is <b>  <u>' + str(body) + '</u> </b></h3>'
    with app.app_context():
        mail.send(msg)

