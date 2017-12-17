# -*- encoding=UTF-8 -*-

from lgblog import db, cache
from datetime import datetime
import random
import datetime
from . import bcrypt
from flask_login import AnonymousUserMixin
from flask import current_app
from unidecode import unidecode
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature

users_roles = db.Table('users_roles',
                       db.Column('user_id', db.String(45), db.ForeignKey('users.id')),
                       db.Column('role_id', db.String(45), db.ForeignKey('roles.id')))


class User(db.Model):
    """Represents Proected users."""

    # Set the name for table
    __tablename__ = 'users'
    id = db.Column(db.String(45), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    # Establish contact with Post's ForeignKey: user_id
    posts = db.relationship(
        'Post',
        backref='users',
        lazy='dynamic')

    roles = db.relationship(
        'Role',
        secondary=users_roles,
        backref=db.backref('users', lazy='dynamic'))

    @staticmethod
    @cache.memoize(60)
    def verify_auth_token(token):
        """Validate the token whether is night."""

        serializer = TimedJSONWebSignatureSerializer(
            current_app.config['SECRET_KEY'])
        try:
            # serializer object already has tokens in itself and wait for
            # compare with token from HTTP Request /api/posts Method `POST`.
            data = serializer.loads(token)
            print(data)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        user = User.query.filter_by(id=data['id']).first()
        return user

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = self.set_password(password)

    def __repr__(self):
        """Define the string format for instance of User."""
        return "<Model User `{}`>".format(self.username)

    def set_password(self, password):
        """Convert the password to cryptograph via flask-bcrypt"""
        return bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def is_authenticated(self):
        """Check the user whether logged in."""
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        """Check the user whether pass the activation process."""
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        """Get the user's uuid from database."""
        return unidecode(self.id)


# 多对多必须的中间关联表
posts_tags = db.Table('posts_tags',
                      db.Column('post_id', db.String(45), db.ForeignKey('posts.id')),
                      db.Column('tag_id', db.String(45), db.ForeignKey('tags.id')))


class Post(db.Model):
    """Represents Proected posts."""

    __tablename__ = 'posts'
    id = db.Column(db.String(45), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime)
    # Set the foreign key for Post
    user_id = db.Column(db.String(45), db.ForeignKey('users.id'))

    category_id = db.Column(db.String(64), db.ForeignKey('categories.id'))

    # Establish contact with Comment's ForeignKey: post_id
    comments = db.relationship('Comment',
                               backref='posts',
                               lazy='dynamic')

    # Establish relationship many to many: posts <==> tags
    tags = db.relationship('Tag',
                           secondary='posts_tags',
                           lazy='dynamic')

    def __init__(self, id, title):
        self.id = id
        self.title = title

    def __repr__(self):
        return "<Model Post `{}`>".format(self.title)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(64))
    # Establish relationship many to many: posts <==> category
    posts = db.relationship('Post',
                            backref='categories',
                            lazy='dynamic')

    def __init__(self, id, name):
        self.name = name
        self.id = id


class Comment(db.Model):
    """Represents Proected comments."""

    __tablename__ = 'comments'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    email = db.Column(db.String(255))
    date = db.Column(db.DateTime())
    post_id = db.Column(db.String(45), db.ForeignKey('posts.id'))

    def __init__(self,id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Model Comment `{}`>'.format(self.name)


class Tag(db.Model):
    """Represents Proected tags."""

    __tablename__ = 'tags'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255))

    posts = db.relationship('Post',
                            secondary='posts_tags',
                            lazy='dynamic')

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "<Model Tag `{}`>".format(self.name)


class Role(db.Model):
    """Represents Proected roles."""
    __tablename__ = 'roles'

    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "<Model Role `{}`>".format(self.name)
