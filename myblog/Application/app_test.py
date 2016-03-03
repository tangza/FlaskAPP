__DEBUG = True

#########################################################################

import sqlite3
from flask import Flask, request, session, g, redirect
from flask import render_template, url_for, abort, flash

from contextlib import closing

# configuration
DATABASE = 'D:/Workspace/python/gitroot/FlaskApp/myblog/Application/tmp/myblog.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

#########################################################################

app = Flask(__name__)
app.config.from_object(__name__)

#########################################################################

def connect_db():
    #print app.config['DATABASE']
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
    g.db.close()

#########################################################################

@app.route('/')
def greeting():
    return 'Welcome, flask is COOL!'

#@app.route('/test/hello/')
@app.route('/test/hello/<username>')
def hello(username=None):
    #return 'Hello %s' % username
    return render_template('hello.html', name=username)

@app.route('/entries')
def show_entries():
    cur = g.db.execute('select title, content from entries order by id desc')
    entries = [dict(title=row[0], content=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/addEntry', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, content) values (?, ?)', [request.form['title'], request.form['content']])
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
            session['logged_in'] = True     #session object built in flask framework
            flash('You were logged in')     #flash method shows infomation
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

#########################################################################

if __name__ == '__main__':
    if __DEBUG:
        app.run(debug=True)
    else :
        app.run(host='0.0.0.0')
