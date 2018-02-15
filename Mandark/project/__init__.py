# -*- coding: utf-8 -*-
from flask import Flask
from flask_admin import Admin
from flask_admin.base import MenuLink
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('Mandark.project.config.DevelopmentConfig')

    db.init_app(app)
    migrate.init_app(app, db)
    '''
    csrf.init_app(app)

from Mandark.project import models

userstore = SQLAlchemyUserDatastore(db, models.User, models.Role)
Security(app, userstore)

print('I Get HERE!!')
try:
    with app.app_context:
        userstore.find_or_create_role(name='admin',
                                      description='Administrator')
        userstore.find_or_create_role(name='user',
                                      description='General User')
        userstore.create_user(email='admin@taiosolve.xyz',
                              password='admin')
        userstore.create_user(email='user@taiosolve.xyz',
                              password='user')
        userstore.add_role_to_user('admin@taiosolve.xyz', 'admin')
        userstore.add_role_to_user('user@taiosolve.xyz', 'user')
        db.session.commit()
except Exception:
    db.session.rollback()
from Mandark.project.views import common, main, admin
app.register_blueprint(main.main)

app_admin = Admin(app, 'Administration Section',
                  template_mode='bootstrap3',
                  index_view=admin.AdminIndexView())
app_admin.add_view(admin.UserModelView(models.User, db.session))
app_admin.add_view(admin.RoleModelView(models.Role, db.session))
app_admin.add_link(MenuLink(name='Back to Site', url='/'))
'''

    return app
