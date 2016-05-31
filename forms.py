from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextField, PasswordField, validators, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from models import User

class LoginForm(Form):
	username = StringField('username',  [validators.Required()])
	password = PasswordField('password',  [validators.Required()])
	remember_me = BooleanField('remember_me', default=False)
	
	
class RegistrationForm(Form):
	username = TextField('Username', [validators.Length(min=4, max=20)])
	email = TextField('Email Address', [validators.Length(min=8, max=50)])
	password = PasswordField('Password', [validators.Required(),validators.Length(min=6, max=30),
				validators.EqualTo('confirm', message="Password must match")])	
	confirm = PasswordField('Repeat Password')
	accept_tos = BooleanField('I accept the <a href="/tos/">Terms of Service</a> and the <a href="/privacy/">Privacy Notice</a> (Last updated May 2016)', [validators.Required()])
	

class EditForm(Form):
    username = StringField('username', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_username, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_username = original_username

    def validate(self):
        if not Form.validate(self):
            return False
        if self.username.data == self.original_username:
            return True
        user = User.query.filter_by(username=self.username.data).first()
        if user != None:
            self.username.errors.append('This username is already in use. Please choose another one.')
            return False
        return True
		
		
class PostForm(Form):
    post = StringField('', validators=[DataRequired()])
    submit = SubmitField('Submit')
	
class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])
	
class RetrievepwdForm(Form):
    username = StringField('username', validators=[DataRequired()])
	
class ChangepwdForm(Form):
	old_password = PasswordField('Old Password', [validators.Required()])	
	new_password = PasswordField('New Password', [validators.Required(),validators.Length(min=6, max=30),
				validators.EqualTo('confirm', message="Password must match")])	
	confirm = PasswordField('Repeat Password')