#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
import simplejson
import string
from database import db


class TNode(db.Model):
    __tablename__ = 'tnode'
    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.Integer)
    ordr = db.Column(db.Integer)
    name = db.Column(db.String(255))
    title =  db.Column(db.String(255))

    @classmethod
    def getRootNodes(cls):
        return TNode.query.filter_by(parent=None).order_by(TNode.ordr)
        
    @classmethod
    def getChildNodes(cls, pId):
        return TNode.query.filter_by(parent=pId).order_by(TNode.ordr)

    @classmethod
    def getIdByPath(cls, path):
        if path[0]=='/':
            path=path[1:]
        lpath = string.split(path,'/')
        first = lpath[0]
        o = TNode.query.filter_by(parent=None, name=first).order_by(TNode.ordr).first()
        if o is None: raise KeyError('object by path %s not found in tree' % path)
        for part in lpath[1:]:
            o = TNode.query.filter_by(parent=o.id, name=part).order_by(TNode.ordr).first()
            if o is None: raise KeyError('object by path %s not found in tree' % path)
        return o.id


class TMeta(db.Model):
    __tablename__ = 'tmeta'
    id = db.Column(db.Integer, primary_key=True)
    meta = db.Column(db.String(255))


