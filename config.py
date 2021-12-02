import os
basedir = os.path.abspath(os.path.dirname(__file__))

# App info
SECRET_KEY = 'secret'
WTF_CSRF_ENABLED = True
DEBUG = True

# Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False