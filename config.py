#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEBUG=True
CSRF_ENABLED = True
SECRET_KEY = 'Treesite Secret'
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+BASE_DIR+'/base.db'
BLUEPRINTS={
            'tree':{'url_prefix':'/tree'},
           }
PASSWORDS="passwords.json"
AUTH_REALM='Login Required REALM'

APPCONFIG = BASE_DIR+'/config.json'
