#! C:\Users\carljame\Envs python

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = b'\x83\xd1Q/r\x04[\x9f\xb34\x1e\xff\xdf\xc2\xe5Z\xcc3\x1a\xc7\x88v&}'
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://jovian34:circuit161522city@jovian34.mysql.pythonanywhere-services.com/jovian34$j34dvd_dev'
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://jovian34:circuit161522city@jovian34.mysql.pythonanywhere-services.com/jovian34$j34dvd_test'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://jovian34:circuit161522city@jovian34.mysql.pythonanywhere-services.com/jovian34$j34dvd'


config_by_name = dict(
    dev = DevelopmentConfig,
    test = TestingConfig,
    prod = ProductionConfig
)



