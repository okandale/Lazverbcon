import sqlite3
from flask import g
import os

try:
    DATABASE = os.environ["DATABASE_URL"]
except KeyError as e:
    raise KeyError("Please specify the 'DATABASE_URL' environment variable.") from e

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()