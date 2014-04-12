#!/usr/bin/python
# -*- coding: UTF-8 -*-

import simplejson
from flask import render_template, request
from flask import Response, jsonify, Blueprint, current_app


from app.tree_models import TNode
from app.database import db
from app.auth import requires_auth


ztree = Blueprint('ztree', __name__, 
                          template_folder='templates',
                          static_folder='static')

@ztree.route('/')
@requires_auth
def root():
    return render_template('tree.html')

@ztree.route('/style.css')
def style():
    return render_template('style.css')
	

@ztree.route('/_tree/nodes', methods=['POST'])
@requires_auth
def node():
    d=[]
    if 'id' in request.form:
        r_id = int(request.form['id'])
        current_app.logger.debug('r_id %i' % r_id)
        if r_id==-1:
            searchf = TNode.getRootNodes()
        else:
            searchf = TNode.getChildNodes(r_id)
        for i in searchf:
            d.append({'id': i.id,
                      'pId': r_id, 
                      'name': i.name,
                      'isParent':True
                      })
    else:
        d.append({'id': -1,
                  'name': 'root',
                  'isParent':True
                  })

    resp = Response(simplejson.dumps(d), status=200, mimetype='application/json')
    return resp


@ztree.route('/_tree/addnode')
@requires_auth
def addNode():
    parent = request.args['parent']
    name = request.args['name']
    nnode = TNode()
    nnode.name=name
    if parent!='-1':
        parent=int(parent)
        nnode.parent=parent
        nnode.ordr=1
    else:
        nnode.parent=None
    db.session.add(nnode)
    db.session.commit()
    return jsonify(status='Ok', node_id=nnode.id)


@ztree.route('/_tree/editnode')
@requires_auth
def editNode():
    node_id = request.args['node']
    name = request.args['name']
    node = db.session.query(TNode).get(int(node_id))
    node.name=name
    db.session.add(node)
    db.session.commit()
    return jsonify(status='Ok', node_id=node.id)
    
    
@ztree.route('/_tree/delnode')
@requires_auth
def delNode():
    node_id = request.args['node']
    db.session.query(TNode).filter(TNode.id==int(node_id)).delete()
    current_app.logger.warning('Delete orphan nodes istelf (by hand)')
    db.session.commit()
    return jsonify(status='Ok')


@ztree.route('/_tree/movenode')
@requires_auth
def moveNode():
    node_id = request.args['node']
    target_id = int(request.args['target'])
    movetype =  request.args['movetype']
    node = db.session.query(TNode).get(int(node_id))
    if movetype == 'inner':
        parent = target_id
        node.parent=parent
        if parent == -1:
            nodes = list(TNode.getRootNodes())
        else:
            nodes = list(TNode.getChildNodes(parent))
        for i, o in enumerate(nodes):
            o.ordr=i
            db.session.add(o)
        node.ordr = len(nodes)+2
        
    elif movetype in ('next', 'prev'):
        nodes = list(TNode.getChildNodes(node.parent))
        result = []
        for i in nodes:
            if i.id==target_id and movetype=='prev':
                result.append(node)
            if i.id!=node.id:
                result.append(i)
            if i.id==target_id and movetype=='next':
                result.append(node)
        
        for i, o in enumerate(result):
            o.ordr=i
            db.session.add(o)
    db.session.commit()
    return jsonify(status='Ok')

