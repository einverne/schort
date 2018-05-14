#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.handlers
from threading import Lock

from app.settings import LOG_FILENAME, LOG_LEVEL

cache = {}
lock = Lock()


def _get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(getattr(logging, LOG_LEVEL))

    console_handler = logging.StreamHandler()

    file_handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, backupCount=3, when='midnight')
    formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)6s] [%(pathname)s:%(lineno)s - %(funcName)s] '
                                  '%(message)s')

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


def get_logger(logger_name):
    global cache
    with lock:
        if not cache.get(logger_name):
            cache[logger_name] = _get_logger(logger_name)
    return cache.get(logger_name)
