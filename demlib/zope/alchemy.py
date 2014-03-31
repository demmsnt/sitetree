#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""SQL Alchemy base"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from zope.interface import implements
from interfaces import IAlchemyBase


class AlchemyBase():

        implements(IAlchemyBase)

        def __init__(self, url, echo=True):
            self.engine = create_engine(url, echo=echo)
            self.Base = declarative_base()

        def getSession(self):
            return sessionmaker(bind=self.engine)()

        def getEngine(self):
            return self.engine

        def getBase(self):
            return self.Base

        def register(self):
                from zope.component import getGlobalSiteManager
                gsm = getGlobalSiteManager()
                gsm.registerUtility(self, IAlchemyBase)
