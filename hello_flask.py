#!/usr/bin/env python
# coding:utf-8


import os
import db

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = '<Oc\xe90X\xd2\xe3\xce`\xd2\xf4\xdd\xd2\xdc{P\x1dy\xe5\xce\xd1.\xe1'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)


@app.before_request
def before_request():
    g.db = db.connect_db(app)


@app.teardown_request
def teardown_request(exception):
    g.db.close()


def get_secret_key():
    return os.urandom(24)


if __name__ == '__main__':
    if not os.path.exists(os.path.join(os.path.dirname(__file__), app.config['DATABASE'])):
        db.init_db(app, 'schema.sql')

    app.run()


