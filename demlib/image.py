#!/usr/bin/python
# -*- coding: UTF-8 -*-

from PIL import Image


def getK(im, maxx, maxy):
        w, h = im.size
        kw = float(w) / float(maxx)
        kh = float(h) / float(maxy)
        k = max(kw, kh)
        return k


def resizeIM(im, maxx, maxy):
        k = getK(im, maxx, maxy)
        w, h = im.size
        new_size = (int(float(w) / k), int(float(h) / k))
        return im.resize(new_size)


def resize(infile, outfile, maxx, maxy):
        resizeIM(Image.open(infile), maxx, maxy).save(outfile)
