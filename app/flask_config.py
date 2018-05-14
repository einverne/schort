#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'schort.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
