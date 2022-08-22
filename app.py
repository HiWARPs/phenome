#!/usr/bin/env python
from flask import Flask
from flask_uploads import UploadSet, configure_uploads
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object('settings')

datafiles = UploadSet('datafiles')
configure_uploads(app, [datafiles])

CSRFProtect(app)

from views import *

if __name__ == '__main__':
	app.run()
