# coding:utf-8
import os
from flask.ext.mail import Mail
from flask.ext.mail import Message
from flask import Flask

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'stmp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)
msg = Message('test subject', sender='1372488211@qq.com', recipients=['1459652670@qq.com'])
msg.body = 'text body'
msg.html = '<b> HTML </b> body'
with app.app_context():
    mail.send(msg)