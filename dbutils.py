#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import hashlib
import sqlite3
import time

from flask import g

DB_PATH = 'data/links.sqlite'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
    return db


def init_db():
    c = get_db().cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS links (shortLink UNIQUE NOT NULL, longLink, timestamp, ip, redirectMethod);''')
    get_db().commit()


def get_long_link(short_link):
    c = get_db().cursor()
    result = c.execute('SELECT longLink FROM links WHERE shortLink=?', (short_link,)).fetchone()
    return result


def insert(short_id, origin_url, remote_addr):
    c = get_db().cursor()
    c.execute('INSERT INTO links VALUES (?, ?, ?, ?, ?)', (short_id, origin_url, int(time.time()), remote_addr, "default"))
    get_db().commit()


def insert_id_unique(origin_url, custom_id=None, remote_addr=None):
    hash_url = hashlib.sha256(origin_url.encode()).digest()
    base64_url = base64.urlsafe_b64encode(hash_url).decode()
    if custom_id is None or custom_id == "":
        custom_id = base64_url[:1]  # 取 base64 前4位

    try:
        insert(custom_id, origin_url, remote_addr)
        database_id = custom_id
    except sqlite3.IntegrityError as e:
        print("Hash already exists, does the long URL matches?")
        long_url_db = get_long_link(custom_id)
        if origin_url == long_url_db[0]:
            # 短链接和长连接一致 直接返回
            print(origin_url + " is already in database with id " + custom_id + ". Serving old id")
            database_id = custom_id
        else:
            # 不一致 增加short ID位数
            print("Found real hash collision for " + origin_url)
            if len(base64_url) - 1 >= len(custom_id) + 1:
                database_id = insert_id_unique(origin_url, custom_id=base64_url[:len(custom_id) + 1], remote_addr=remote_addr)
            else:
                print("Can't produce a long enough hash from the new link to be unique. This should never happen")
                print("Bailing out, you are on your own. Good luck.")
                print("=========================================================================================")
    return database_id
