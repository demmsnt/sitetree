#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Main app"""
from app import app
import sys
import os.path

if __name__=='__main__':
    sys.path.insert(0,os.path.abspath(os.path.dirname(__file__)))
    if app.debug==False:
        print "Daemonize"
        from demlib.daemonize import daemonize
        daemonize(stdout='stdout.log', stderr='stderr.log')
    app.run()
