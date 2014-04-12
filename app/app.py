#!/usr/bin/python
# -*- coding: UTF-8 -*-
import database
from flask import Flask
import sys

def create_app(config=None, blueprints=None):
    """
    Фабрика приложений
    blueprints - список блюпринтов в виде строк
    """
    app = Flask(__name__)
    app.config.from_object(__name__)
    if config is not None:
        app.config.from_object(config)
    database.db.init_app(app)
    if blueprints is not None:
        for k, v in blueprints.items():
            app.logger.debug("Register Blueprint %s" % k)
            m = __import__(k)
            app.register_blueprint(m.bp, url_prefix=v['url_prefix'])
    if 'initdb' in sys.argv:
        app.logger.debug('Init tatabase')
        with app.app_context():
            database.db.create_all()
    return app

