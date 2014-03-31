#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Загрузка файла"""

import os
import os.path


def upload(request, fieldname):
        """Загрузит файл и вернет его содержимое и имя"""
        fn = request.files[fieldname][0]['filename']
        return fn, request.files[fieldname][0]['body']


def upload2directory(request, fieldname, path):
        """Загрузит файл в каталог"""
        fn = request.files[fieldname][0]['filename']
        filename = os.path.basename(fn)
        f = open(os.path.join(path, filename), 'wb')
        f.write(request.files[fieldname][0]['body'])
        f.close()
        return fn


def upload2file(request, fieldname, filename):
#        fn = request.files[fieldname][0]['filename']
        f = open(filename, 'wb')
        f.write(request.files[fieldname][0]['body'])
        f.close()
