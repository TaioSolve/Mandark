# -*- coding: utf-8 -*-
from Mandark.project.app import db
from sqlalchemy.ext.hybrid import hybrid_property
from flask_security import UserMixin, RoleMixin

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

organisations_projectmgrs = db.Table('organisations_projectmgrs',
                                     db.Column('organisation_id', db.Integer(),
                                               db.ForeignKey('organisation.id')),
                                     db.Column('projectmgr_id', db.Integer(),
                                               db.ForeignKey('projectmgr.id')))

organisations_projects = db.Table('organisations_projects',
                                  db.Column('organisation_id', db.Integer(),
                                            db.ForeignKey('organisation.id')),
                                  db.Column('project_id', db.Integer(),
                                            db.ForeignKey('project.id')))

change_request_types_change_request_submitters = \
    db.Table('change_request_types_change_request_submitters',
             db.Column('crt_id', db.Integer(),
                       db.ForeignKey('change_request_type.id')),
             db.Column('crs_id', db.Integer(),
                       db.ForeignKey('change_request_submitter.id')))


class User(db.Model, UserMixin):
    """
    User: defines users and their attribles for the website
    Parents: db.Model, flask.ext.security.UserMixin
    """
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(128), index=True)
    last_name = db.Column(db.String(128), index=True)
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

    @hybrid_property
    def is_moderator(self):
        return self.has_role('moderator')

    @hybrid_property
    def is_projectmgr(self):
        return self.has_role('projectmgr')

    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<models.Role[name=%s]>' % self.name


class Organisation(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    projectmgrs = db.relationship('Projectmgr',
                                  secondary=organisations_projectmgrs,
                                  backref=db.backref('organisations',
                                                     lazy='dynamic'))
    projects = db.relationship('Project', secondary=organisations_projects,
                               backref=db.backref('organisations',
                                                  lazy='dynamic'))

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<models.Organisation[name=%s]>' % self.name


class Projectmgr(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<models.ProjectMgr[name=%s]>' % self.name


class Project(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<models.Project[name=%s]>' % self.name


class ChangeRequestType(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255), unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<models.ChaneRequestType[name=%s]>' % self.name


class ChangeRequestSubmitter(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    cr_type = db.relationship('ChangeRequestType',
                              secondary=change_request_types_change_request_submitters,  # noqa
                              backref=db.backref('change_request_submitter',
                                                 lazy='dynamic'))
    project = db.Column(db.String(80))
    description = db.Column(db.String(255))
    date_submitted = db.Column(db.DateTime, default=db.func.now())
    date_required = db.Column(db.DateTime)
    priority = db.Column(db.String(12))
    change_reason = db.Column(db.Text)
    impact = db.Column(db.String(255))
    assumptions = db.Column(db.Text)
    comments = db.Column(db.Text)

    def __str__(self):
        return self.project

    def __repr__(self):
        return '<models.ChangeRequestSubmitter[project=%s]>' % self.name




