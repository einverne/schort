#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import hashlib

import sqlalchemy

from app import db
from app.logger import get_logger
from app.models import Url

DB_PATH = 'data/links.sqlite'

logger = get_logger(__file__)


def get_long_link(short_link):
    result = db.session.query(Url).filter(Url.shortLink == short_link).first()
    if result is None:
        return ""
    return result.longLink


def insert(short_id, origin_url, remote_addr):
    url = Url(short_link=short_id, long_link=origin_url, ip=remote_addr)
    db.session.add(url)
    db.session.commit()


def insert_id_unique(origin_url, custom_id=None, remote_addr=None):
    hash_url = hashlib.sha256(origin_url.encode()).digest()
    base64_url = base64.urlsafe_b64encode(hash_url).decode()
    if custom_id is None or custom_id == "":
        custom_id = base64_url[:4]  # 取 base64 前4位

    try:
        url_db = get_long_link(custom_id)
        if url_db == origin_url:
            logger.info("{} exist return {}".format(origin_url, custom_id))
            return custom_id
        elif url_db == '':
            insert(custom_id, origin_url, remote_addr)
            database_id = custom_id
        else:
            # 不一致 增加short ID位数
            logger.info("Found real hash collision for " + origin_url)
            if len(base64_url) - 1 >= len(custom_id) + 1:
                database_id = insert_id_unique(origin_url, custom_id=base64_url[:len(custom_id) + 1], remote_addr=remote_addr)
            else:
                logger.info("Can't produce a long enough hash from the new link to be unique. This should never happen")
                logger.info("Bailing out, you are on your own. Good luck.")
                logger.info("=========================================================================================")
    except sqlalchemy.exc.IntegrityError as e:
        logger.info("Hash already exists, does the long URL matches?")
    return database_id


if __name__ == '__main__':
    insert_id_unique("https://google.com", 'short', '')
    insert("short1", "long", "")
    get_long_link('short')
