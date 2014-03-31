#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Работа с временными данными"""

import tempfile
import shutil


class temp:
        def __init__(self):
                self.cleaned = False
                self.path = tempfile.mkdtemp()

        def clean(self):
                if not self.cleaned:
                        shutil.rmtree(self.path)
                        self.cleaned = True

        def __del__(self):
                self.clean()
