#!/usr/bin/python
# -*- coding: UTF-8 -*-
from interfaces import IMailSender, IConstRegistry
from zope.interface import implements
from demlib.sendmail import sendGmail
from zope.component import getUtility
import threading


def threadedfunc(fromf, To, Subject, Body, files, username, password, handler, data):
    sendGmail(fromf, To, Subject, Body, files, username, password)
    if handler is not None:
        handler(data)

class ThreadedGMailServer():
        """Многопоточная отправка почты через Gmail"""
        implements(IMailSender)
        def __init__(self):
            consts = getUtility(IConstRegistry)
            config = consts.get('MAILER')
            self.fromf = config['from']
            self.username = config['username']
            self.password = config['password']
            
        def send(self, To, Subject, Body, files=None, From=None, handler=None, data=None):
            fromf = From
            if fromf is None:
                fromf = self.fromf
            t = threading.Thread(target=threadedfunc, args=(fromf, To, Subject, Body, files, self.username, self.password, handler, data))
            t.start()
            #sendGmail(fromf, To, Subject, Body, files, self.username, self.password);
        def register(self):
                from zope.component import getGlobalSiteManager
                gsm = getGlobalSiteManager()
                gsm.registerUtility(self, IMailSender)


