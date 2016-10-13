#!/usr/bin/env python
# coding:utf-8


import sqlite3
from contextlib import closing
from flask import g

# sqlite3 /tmp/flaskr.db < schema.sql
def connect_db(app):
    return sqlite3.connect(app.config['DATABASE'])


def init_db(app, schema_file):
    with closing(connect_db(app)) as db:
        with app.open_resource(schema_file) as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv
