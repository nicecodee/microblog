import smtplib
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.update(
			DEBUG=True,
			MAIL_SERVER='smtp.163.com'
			MAIL_PORT=465
			MAIL_USE_SSL=True
			MAIL_USERNAME='goodtre@163.com'
			MAIL_PASSWORD='Stone001')
			
mail = Mail(app)

@app.route('/send-mail/')
def send_mail():
	try:
		msg = Message("send mail haha",
		sender="goodtre@163.com",
		recipients=["goodtre@163.com"])
		msg.body = "yo! \n Have you head of me?"
		mail.send(msg)
		return 'Mail sent'
	
	except Exception as e:
		return str(e)
