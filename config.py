WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#---local mail server settings---
# MAIL_SERVER = 'localhost'
# MAIL_PORT = 25
# MAIL_USERNAME = None
# MAIL_PASSWORD = None

# mail server settings
DEBUG=True
MAIL_SERVER='smtp.163.com'
MAIL_PORT=465
MAIL_USE_SSL=True
MAIL_USERNAME='goodtre@163.com'
MAIL_PASSWORD='Stone001'
# administrator list
ADMINS = ['goodtre@163.com']

# pagination
POSTS_PER_PAGE = 3

#full text search
WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50