#!/usr/bin/env python
from flask import render_template, session, url_for, request, redirect, flash, abort, jsonify
from app import *
from db import *
from forms import *
from datafile import *
import os, time, datetime


@app.route('/')
def index():
	return browse()


@app.route('/browse')
def browse():
	form = SearchForm(request.args, csrf_enabled=False)
	if form.validate():
		keywords = ['%'+k+'%' for k in form.keyword.data.split()]
		submissions = list(map(dict, query_db('select * from submissions where '+' or '.join(['title like ?']*len(keywords))+' order by date_submitted desc limit 10', *keywords)))
	else:
		submissions = list(map(dict, query_db('select * from submissions where confirmed=1 order by date_submitted desc limit 10')))
	for subm in submissions:
		(subm['author'],) = query_db('select * from users where id=?', subm['author_id'])
		subm['date_submitted'] = datetime.datetime.utcfromtimestamp(subm['date_submitted']).strftime('%Y-%m-%d')
	return render_template('browse.html', submissions=submissions, search_keyword=(form.keyword.data or ''))


@app.route('/submit', methods=['GET', 'POST'])
def submit():
	form = SubmissionForm()
	if form.validate_on_submit():
		form = flat(form)
		filename = datafiles.save(request.files['datafile'])
		with get_db() as db:
			c = db.cursor()
			vals = [1, int(time.time()), form.title, form.description, filename, 0]
			c.execute('insert into submissions (author_id, date_submitted, title, description, datafile, confirmed) values (?, ?, ?, ?, ?, ?)', vals)
			subm_id = c.lastrowid
		flash('Your submission was successful. Please, edit the submission to finish confirmation.')
		return redirect(url_for('edit', subm_id=subm_id))
	return render_template('submit.html', form=form)


def abort_not_found_subm_id(view):
	def dview(subm_id, *args, **kwargs):
		if not query_db('select * from submissions where id=?', subm_id):
			return abort(404)
		view(subm_id, *args, **kwargs)
	return dview


def abort_not_confirmed_subm_id(view):
	def dview(subm_id, *args, **kwargs):
		if not query_db('select * from submissions where id=? and confirmed=1', subm_id):
			return abort(404)
		view(subm_id, *args, **kwargs)
	return dview


@abort_not_confirmed_subm_id
@app.route('/<int:subm_id>')
def show(subm_id):
	# form = DataRequestFormFactory.create(subm_id)()
	columns = sorted(query_db('select * from datacolumns where subm_id=?', subm_id), key=lambda c: c['n'])
	form = DataRequestForm(request.args, columns=columns)
	# if form.validate_on_submit():
	# 	data = get_filtered_data(subm_id, flat(form))
	# 	return '<br>\r\n'.join(map(lambda a: '&nbsp;&nbsp;    '.join(map(lambda x: '%E'%x, a)), data))
	(subm,) = query_db('select * from submissions where id=?', subm_id)
	return render_template('show.html', subm=subm, form=form)


@abort_not_confirmed_subm_id
@app.route('/<int:subm_id>/extract')
def extract(subm_id):
	columns = sorted(query_db('select * from datacolumns where subm_id=?', subm_id), key=lambda c: c['n'])
	form = DataRequestForm(request.args, columns=columns)
	if form.validate():
		data = get_filtered_data(subm_id, flat(form))
		return '<br>\r\n'.join(map(lambda a: '&nbsp;    '.join(map(lambda x: '%E'%x, a)), data))
	(subm,) = query_db('select * from submissions where id=?', subm_id)
	return render_template('show.html', subm=subm, form=form)


@abort_not_found_subm_id
@app.route('/<int:subm_id>/edit', methods=['GET', 'POST'])
def edit(subm_id):
	if request.method == 'POST':
		form = DataColumnForm()
		if form.validate_on_submit():
			form = flat(form)
			args = form.title, form.units, form.role, subm_id, form.n
			with get_db() as db:
				c = db.cursor()
				if c.execute('select * from datacolumns where subm_id=? and n=?', args[-2:]).fetchall():
					c.execute('update datacolumns set title=?, units=?, role=? where subm_id=? and n=?', args)
				else:
					c.execute('insert into datacolumns (title, units, role, subm_id, n) values (?, ?, ?, ?, ?)', args)
				c.execute('update submissions set confirmed=1 where id=?', (subm_id,))
		return jsonify(form.errors)
	else:	# GET
		(subm,) = query_db('select * from submissions where id=?', subm_id)
		cols = {col['n']:col for col in query_db('select * from datacolumns where subm_id=?', subm_id)}
		with DataFile(subm_id) as f:
			data = [['%E'%a for a in l] for l in f.get_data(10)]
		forms = [DataColumnForm(data=cols[i]) if i in cols else DataColumnForm(n=i) for i in range(len(data[0]))]
		return render_template('edit.html', subm=subm, data=data, forms=forms)


@app.route('/login', methods=['POST'])
def login():
	return abort(501)


@app.route('/logout', methods=['POST'])
def logout():
	return abort(501)


@app.route('/about')
def about():
	return abort(501)


@app.route('/contact')
def contact():
	return abort(501)