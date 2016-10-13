#!/usr/bin/env python
# coding:utf-8


import os
import db

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    #DATABASE=os.path.join(os.path.dirname(__file__), 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='<Oc\xe90X\xd2\xe3\xce`\xd2\xf4\xdd\xd2\xdc{P\x1dy\xe5\xce\xd1.\xe1',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


@app.before_request
def before_request():
    g.db = db.connect_db(app)


@app.teardown_request
def teardown_request(exception):
    g.db.close()


def get_secret_key():
    return os.urandom(24)


@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    if not os.path.exists(app.config['DATABASE']):
        db.init_db(app, 'schema.sql')
    app.run()


