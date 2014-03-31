#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Base app views"""
from flask import render_template, request, Response, redirect, url_for, g
from . import app
import os.path
import json
import tree_models


@app.errorhandler(401)
def noAuth(e):
    return Response(
        render_template('noauth.html'), 401,
        {'WWW-Authenticate': 'Basic realm="%s"' % app.config.get('AUTH_REALM','Login Required')}
        )


@app.route('/app/notconfig')
def noConfig():
    return render_template('notconfig.html')


@app.errorhandler(404)
def page404(e):
    return render_template('404.html'), 404


@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static',filename='favicon.ico'))


@app.before_request
def loadAppConfig():
    app_cfg = app.config.get('APPCONFIG', None)
    if app_cfg is None or not os.path.exists(app_cfg):
        g.app_config=None
    g.app_config = json.loads(open(app_cfg,'rb').read())


#@app.context_processor
#def setAppConfig():
#    return dict(app_config=g.app_config)


@app.route('/<subpath>')
def pages(subpath):
    loadAppConfig()
    #print dir(g),g.get('app_config')
    if g.app_config:
        app.logger.debug('app_cfg is %s' % str(app.config.get('APPCONFIG', None)))
        return redirect(url_for('noConfig'))
    cfg = g.app_config
    root_path =  g.app_config['ROOT_PATH']
    full_path = root_path
    if subpath is not None:
        full_path=full_path+'/'+subpath
    oid = tree_models.TNode.getIdByPath(full_path)
    return "Hello world "+str(oid)


@app.route('/')
def root():
    return pages(None)
