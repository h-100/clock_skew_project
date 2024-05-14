#!/usr/bin/python3

import os

basedir = os.path.abspath(os.path.dirname(__file__))
##preivous database --> new_app
class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'new_app_post_changes.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
