import logging
from flask import Flask
from flask_appbuilder.security.mongoengine.manager import SecurityManager
from flask_appbuilder import AppBuilder
from flask_mongoengine import MongoEngine

"""Logging configuration"""
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')
db = MongoEngine(app)
appbuilder = AppBuilder(app, security_manager_class=SecurityManager)


"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""    

from app import views, models

