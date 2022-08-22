from app import *
import sqlite3, os
from flask import g


#@app.cli.command('initdb')
def init_db():
	with app.app_context(), get_db() as db, app.open_resource('schema.sql', mode='r') as f:
		db.executescript(f.read())


def connect_db():
	db = sqlite3.connect(app.config['DATABASE'])
	db.row_factory = sqlite3.Row
	return db


def get_db():
	if not hasattr(g, '_db'):
		g._db = connect_db()
	return g._db


@app.teardown_appcontext
def close_db(error):
	if hasattr(g, '_db'):
		g._db.close()


def query_db(query, *args):
	with get_db() as db:
		r = db.execute(query, args).fetchall()
	return r
