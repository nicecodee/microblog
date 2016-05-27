from flask.ext.mail import Message
from __init__ import mail
from config import ADMINS

def follower_notification(followed,follower):
	msg = Message("[microblog] %s is now following you!" % follower.username,sender=ADMINS[0],recipients=[followed.email])
	msg.body = "yo! \n Have you head of me?"
	mail.send(msg)
	