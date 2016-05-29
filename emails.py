from flask.ext.mail import Message
from __init__ import mail, app
from config import ADMINS
from threading import Thread




#--send email asynchronously by using multithreading--
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_mail_get_pwd(user):
	msg = Message("[microblog] Retrieve Your password!",sender=ADMINS[0],recipients=[user.email])
	msg.body = "[microblog] Your original password is %s " % user.password
	thr = Thread(target=send_async_email, args=[app, msg])
	thr.start()		
		

		
		
#---Note that Flask-Mail sends emails synchronously---
# def send_mail_get_pwd(user):
	# msg = Message("[microblog] Retrieve Your password!",sender=ADMINS[0],recipients=[user.email])
	# msg.body = "[microblog] Your original password is %s " % user.password
	# mail.send(msg)
	
	


