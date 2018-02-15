# -*- coding: utf-8 -*-
from .config import DevelopmentConfig

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db)

    return app
