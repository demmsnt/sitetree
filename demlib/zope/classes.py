#!/usr/bin/python
# -*- coding: UTF-8 -*-
from interfaces import IConstRegistry
from zope.interface import implements


class ConstRegistry():
        """Реестр констант"""
        implements(IConstRegistry)

        def __init__(self, consts=None):
                if consts:
                        self.consts = consts
                else:
                        self.consts = {}

        def get(self, key, default=None):
                if default:
                        return self.consts.get(key, default)
                return self.consts.get(key)

        def register(self):
                from zope.component import getGlobalSiteManager
                gsm = getGlobalSiteManager()
                gsm.registerUtility(self, IConstRegistry)
