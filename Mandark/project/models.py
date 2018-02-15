# -*- coding: utf-8 -*-
from Mandark.project.app import db
from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property
from flask_security import UserMixin, RoleMixin
from jwt import encode as jwtencode, decode as jwtdecode
from jwt import InvalidTokenError, ExpiredSignatureError
from datetime import datetime, timedelta
from werkzeug.security import gen_salt
"""
We need a table to relate users to roles by id.
This is an example of a many-to-many relationship in SQLAlchemy
i.e. a user can have many roles and roles can have many users
"""
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    """
    User: defines users and their attribles for the website
    Parents: db.Model, flask.ext.security.UserMixin
    """
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=False)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(50))
    current_login_ip = db.Column(db.String(50))
    login_count = db.Column(db.Integer)
    confirmed_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime(), default=db.func.now())
    updated_at = db.Column(db.DateTime(),
                           default=db.func.now(),
                           onupdate=db.func.now())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        """Flask admin needs this to print the user correctly"""
        return self.email

    def __repr__(self):
        return '<models.User[email=%s]>' % self.email

    @hybrid_property
    def is_admin(self):
        """Lame example of hybrid property"""
        return self.has_role('admin')

    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    @staticmethod
    def encode_auth_token(user_id):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')
                ),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            auth_token = jwtencode(payload,
                                   current_app.config.get('SECRET_KEY'),
                                   algorithm='HS256')
            return auth_token
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwtdecode(auth_token,
                                current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except ExpiredSignatureError:
            return 'Signature Expired. Please log in again.'
        except InvalidTokenError:
            return 'Invalid Token. Please log in again.'


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<models.Rol[name=%s]>' % self.name
