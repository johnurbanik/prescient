#!/usr/bin/env python3

import logging  # noqa

from flask import Flask
from flask_logs import LogSetup
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

logs = LogSetup()
logs.init_app(app)
