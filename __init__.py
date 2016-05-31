from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.login import LoginManager
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.bootstrap import Bootstrap



app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)
moment = Moment(app)
bootstrap = Bootstrap(app)


lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


#import views and models at the bottom
import views, models



#send mail for loggin
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'microblog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

#local logging file
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
	
	#limiting the size of a log file to one megabyte, and keep the last 10 log files as backups.
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
	
	#timestamp,logging level and the file and line number where the message originated in addition to the log message and the stack trace
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	
	#To make the logging more useful, lowering the logging level. This will write useful messages to the log without having to call them errors.
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')
	


if __name__ == "__main__":
	app.run()