# -*- encoding=UTF-8 -*-

from lgtalk import db
from datetime import datetime
import random




class User(db.Model):
    # __tablename__ = 'user'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32))
    salt = db.Column(db.String(32))
    head_url = db.Column(db.String(256))

    def __init__(self, username, password, salt=''):
        self.username = username
        self.password = password
        self.salt = salt
        self.head_url = 'http://images.nowcoder.com/head/' + str(random.randint(0,1000)) +  'm.png'

    def __repr__(self):
        return '[User %d %s]' % (self.id, self.username)


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256))
    content = db.Column(db.TEXT)
    user_id = db.Column(db.INTEGER)
    created_date = db.Column(db.DATETIME)
    status = db.Column(db.Integer, default=0)  # 0 正常 1 被删除

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.created_date = datetime.now()

    def __repr__(self):
        return '<Article %d %s>' % (self.title, self.content)


class Comment(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(1024))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Integer, default=0)  # 0 正常 1 被删除
    user = db.relationship('User')

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return '<Comment %d %s>' % (self.id, self.content)


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(64))

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return '<Tag %d %s>' % (self.id, self.content)


class Catagory(db.Model):
    __tablename__ = 'catagory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(64))

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return '<Catagory %d %s>' % (self.id, self.content)

