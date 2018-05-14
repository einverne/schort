#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.flask_config import Config

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models, schort  # 导入models，定义数据库结构
