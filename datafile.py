from app import *
from db import *
# from forms import *	# TODO: deal with circular imports


def get_filtered_data(subm_id, flatform):
	data = []
	with DataFile(subm_id) as f:
		for l in f.get_data():
			a = []
			for xcol in flatform.xcols:
				if xcol.checked:
					x = l[xcol.n]
					if not (xcol.min and xcol.min > x or xcol.max and xcol.max < x):
					# if xcol.min <= x <= xcol.max:
						a.append(x)
			if a:
				data.append(a + [l[ycol.n] for ycol in flatform.ycols if ycol.checked])
	return data


def get_data_from_file(f, nrows=None):
	d = []
	for l in f:
		if nrows and len(d) == nrows:
			break
		if l.strip() != '':
			try:
				d.append(map(float, l.replace(';',' ').replace(',',' ').strip().split()))
			except:
				pass
	if len(d) != 0:
		nmax = max(map(len, d))
		d = [l + [None]*(nmax-len(l)) for l in d]
	return d


class DataFile:
	def __init__(self, subm_id=1, filename=None, file=None):
		if file:
			self.file = file
		else:
			filename = filename or datafiles.path(query_db('select datafile from submissions where id=?', subm_id)[0]['datafile'])
			self.file = open(filename)
	def get_data(self, nrows=None):
		return get_data_from_file(self.file, nrows=nrows)
	def __enter__ (self):
		return self
	def __exit__ (self, exc_type, exc_value, traceback):
		self.file.close()

openDataFile = DataFile