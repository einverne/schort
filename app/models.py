#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from app import db


class Url(db.Model):
    shortLink = db.Column(db.TEXT, primary_key=True)
    longLink = db.Column(db.TEXT)
    timestamp = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    ip = db.Column(db.String(256))

    def __init__(self, short_link, long_link, ip):
        self.shortLink = short_link
        self.longLink = long_link
        self.ip = ip

    def __repr__(self):
        return '<Url {}, {}>'.format(self.shortLink, self.longLink)