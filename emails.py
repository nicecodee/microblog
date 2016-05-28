from flask.ext.mail import Message
from __init__ import mail
from config import ADMINS

def send_mail_get_pwd(user):
	msg = Message("[microblog] Retrieve Your password!",sender=ADMINS[0],recipients=[user.email])
	msg.body = "[microblog] Your original password is %s " % user.password
	mail.send(msg)