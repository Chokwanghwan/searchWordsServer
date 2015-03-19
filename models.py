# -*- coding:utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/secondTest.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(100))
    recentUrl = db.Column(db.String(100))
    word = db.Column(db.String(100))
    mean = db.Column(db.String(100))
    deleteCheck = db.Column(db.String(2)) # default = N

    # username = db.Column(db.String(80), unique=True)
    # email = db.Column(db.String(120), unique=True)

    def __init__(self, account, recentUrl, word, mean, deleteCheck):
        self.account = account
        self.recentUrl = recentUrl
        self.word = word
        self.mean = mean
        self.deleteCheck = deleteCheck

    def __repr__(self):
        return '<User %r>' % self.account