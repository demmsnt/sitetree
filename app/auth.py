#!/usr/bin/python
# -*- coding: UTF-8 -*-
from functools import wraps
from flask import request, Response, current_app, redirect, url_for, abort
import simplejson
import hashlib
import os


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    cfg = current_app.config
    fname = os.path.join(cfg['BASE_DIR'], cfg['PASSWORDS']) #TODO cache and etc
    js_obj = simplejson.loads(open(fname,'r').read())
    user = js_obj.get(username, None)
    if user is None:
        return None
    mdpass = hashlib.md5()
    mdpass.update(password)
    mdpass=mdpass.hexdigest()
    if user['password']!=mdpass:
        return None
    return user['rights']


def get_rights(curr_request):
    auth = curr_request.authorization
    return check_auth(auth.username, auth.password)


def authenticate():
    """Sends a 401 response that enables basic auth"""
    abort(401)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
