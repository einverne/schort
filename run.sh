#!/usr/bin/env bash

gunicorn -c config.py -w 4 -b 0.0.0.0:4000 schort:app