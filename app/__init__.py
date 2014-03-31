#!/usr/bin/python
# -*- coding: UTF-8 -*-
import database
import sys
import config
from .app import create_app

app = create_app(config=config, blueprints=config.BLUEPRINTS)

import views
