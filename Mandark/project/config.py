# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """Base Configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False'  # noqa
    # import binascii
    # import os
    # print(binascii.hexlify(os.urandom(24)))
    SECRET_KEY = "3833bffa12a864aaa90b8dda70d5c11694ab2ecfa3a99455"
    CSRF_ENABLED = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True
