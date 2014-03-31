#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Приложение для хранения файлов"""
from hashlib import sha1
from upload import upload2directory
import os
import os.path
import shutil
import mimetypes
import tornado
import string
from tornado.web import authenticated


class FileStore(object):
        def __init__(self, path):
                """path - путь где будут храниться файлы в ФС
                """
                self.path = path

        def get_subpath(self, id):
                subpath = sha1()
                subpath.update(id)
                return subpath.hexdigest()

        def upload(self, id, request, fieldname):
                """id - идентификатор хранилища"""
                fullpath = os.path.join(self.path, self.get_subpath(id))
                if not os.path.exists(fullpath):
                        os.mkdir(fullpath)
                return upload2directory(request, fieldname, fullpath)

        def list(self, id):
                fullpath = os.path.join(self.path, self.get_subpath(id))
                if os.path.exists(fullpath):
                        for i in os.listdir(fullpath):
                                fn = os.path.join(fullpath, i)
                                if os.path.isfile(fn):
                                        yield i

        def get_fullpath(self, id, filename):
                fullpath = os.path.join(self.path, self.get_subpath(id))
                return os.path.join(fullpath, filename)

        def remove(self, id, filename):
                os.remove(self.get_fullpath(id, filename))
                if len(list(self.list(id))) == 0:
                        shutil.rmtree(os.path.join(self.path, self.get_subpath(id)))

        def mime(self, filename):
                return mimetypes.guess_type(filename)[0]

        def serve(self, id, handler, filename):
                mime = self.mime(filename)
                if mime:
                        handler.clear()
                        handler.set_header('Content-type', self.mime(filename))
                #CHECK
                fullpath = self.get_fullpath(id, filename)
                normpath = os.path.normpath(fullpath)
                normself = os.path.normpath(self.path)
                if not normpath.startswith(normself):
                        raise RuntimeError("bad filename")  # Попытка выхода из директории
                handler.write(open(normpath, 'rb').read())


class FileHandler(tornado.web.RequestHandler):

    @authenticated
    def post(self, operation, id):
        """Записать файл в хранилище"""
        self.application.files.upload(id, self.request, 'file')
        self.redirect(self.request.headers.get('referer', '/'))

    @authenticated
    def get(self, operation, id, filename):
        if operation == 'get':
                self.application.files.serve(id, self, filename)
        elif operation == 'del':
                self.application.files.remove(id, filename)
                self.redirect(self.request.headers.get('referer', '/'))
        else:
                self.write('wrong operation')

from demlib.image import resizeIM
from PIL import Image


class PhotoStore(FileStore):
        """Хранилище которое будет использоваться для фотоальбомов и т.п."""
        def __init__(self, path, sizes=None):
                """path - путь где будут храниться файлы в ФС
                sizes - list of sizes eg:['600x600','740x480','320x200']
                """
                self.path = path
                if sizes is None:
                        raise RuntimeError("sizes not specified")
                self.sizes = sizes[:]
                self.tsizes = {}
                for size in self.sizes:
                        w, h = string.split(size.lower(), 'x')
                        self.tsizes[size] = (int(w), int(h))

        def makeThumbnail(self, im, dest, fn, size):  # TODO вынести в отдельный поток
                if not os.path.exists(dest):
                        os.mkdir(dest)
                newIm = resizeIM(im, size[0], size[1])
                newIm.save(os.path.join(dest, fn))

        def upload(self, id, request, fieldname):
                fn = super(PhotoStore, self).upload(id, request, fieldname)
                # теперь сделаем все разрешения  #TODO вынести в отдельный поток
                subpath = self.get_subpath(id)
                fullpath = os.path.join(self.path, subpath)
                im = Image.open(os.path.join(fullpath, fn))
                for k, v in self.tsizes.items():
                        self.makeThumbnail(im, os.path.join(fullpath, k), fn, v)
                return subpath, fn

        def remove(self, id, filename):
                opj = os.path.join
                subpath = self.get_subpath(id)
                os.remove(self.get_fullpath(id, filename))
                for i in self.sizes:
                        os.remove(opj(opj(opj(self.path, subpath), i), filename))

                if len(list(self.list(id))) == 0:
                        shutil.rmtree(opj(self.path, subpath))
