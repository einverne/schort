#!/usr/bin/env sh

gunicorn -c gunicorn_config.py -w 4 -b 0.0.0.0:4000 app:app