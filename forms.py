from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextField, PasswordField, validators

class LoginForm(Form):
	username = StringField('username',  [validators.Required()])
	password = PasswordField('password',  [validators.Required()])
	remember_me = BooleanField('remember_me', default=False)
	

class RegistrationForm(Form):
	username = TextField('username', [validators.Length(min=4, max=20)])
	email = TextField('Email Address', [validators.Length(min=8, max=50)])
	password = PasswordField('Password', [validators.Required(),validators.Length(min=6, max=30),
				validators.EqualTo('confirm', message="Password must match")])	
	confirm = PasswordField('Repeat Password')
	accept_tos = BooleanField('I accept the <a href="/tos/">Terms of Service</a> and the <a href="/privacy/">Privacy Notice</a> (Last updated May 2016)', [validators.Required()])