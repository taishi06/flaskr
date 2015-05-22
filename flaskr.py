import MySQLdb
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

# some configuration
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
	return MySQLdb.connect(host='localhost', user='root', passwd='t3rt3r06', db='flaskr', debug=True)

# self explanatory requests
@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

# initialize database
def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

# index page, show all entries
@app.route('/')
def show_entries():
	cur = g.db.execute('SELECT title, `text` FROM entries ORDER BY id DESC')
	entries = cur.fetchall()
	return render_template('show_entries.html', entries=entries)

# adding entries
@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)	
	# insert new entry
	g.db.execute('INSERT INTO entries (title, text) VALUES (?, ?)', [request.form['title'], request.form['text']])
	# commit new entry
	g.db.commit()
	# flash message for success
	flash('New entry was successfully posted')
	# redirect to the entries
	return redirect(url_for('show_entries'))

# login, same page for the validation process
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

# logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


# run this file itself
if __name__ == '__main__':
	app.run()