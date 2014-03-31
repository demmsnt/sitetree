#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Основные интерфейсы для CMS"""
from zope.interface import Interface
from zope.interface import Attribute


class IConstRegistry(Interface):
        """Константы"""
        def get(key, default=None):
                """Вернет значение ключа"""
                pass

class IMailSender(Interface):
    """Посылальщик почты"""
    def send(To, Subject, Body, files=None, From=None, handler=None, data=None):
        """Отправит почту, ничего не возвращает, 
        так как почта ставится в очередь отправки и возможно
        не отправится
        """
        pass

class IAlchemyBase(Interface):
        def getSession(self):
            pass

        def getEngine(self):
            pass

        def getBase(self):
            pass
