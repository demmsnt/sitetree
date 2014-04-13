#!/usr/bin/python
# -*- coding: UTF-8 -*-

import simplejson
from flask import render_template, request
from flask import Response, jsonify, Blueprint, current_app


page = Blueprint('jsonpage', __name__, 
                          template_folder='templates',
                          static_folder='static')


class JsonPage():
    def __init__(self, app, data):
        self.app = app
        self.data = data

    def render(self, request):
        return render_template(self.data['template'], data=self.data['data'])
        
def factory(app, data):
    return JsonPage(app, data)
