from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from __init__ import app, db, lm
from forms import LoginForm, RegistrationForm
from models import User
import datetime
from passlib.hash import sha256_crypt


@app.errorhandler(404)
def page_not_found(e):
	return  render_template("404.html")

	
@app.route('/')
@app.route('/index/')
@login_required
def index():
    user = g.user
    posts = [
        { 
            'author': {'username': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'username': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)
						   
						   

@app.route('/login/', methods=['GET', 'POST'])
def login():
	error = ''
	try:
		form = LoginForm()
		if form.validate_on_submit():
			session['remember_me'] = form.remember_me.data
			u = form.username.data
			p = form.password.data
			#check if username matches
			if User.query.filter_by(username=u, password=p).first() is None:
				flash("user not found")
			#check if password matches
			# else if sha256_crypt.verify(p, data):
			else:
				user = User.query.filter_by(username=u, password=p).first()
				flash("You are now logged in!")
				session['logged_in'] = True
				login_user(user)
				return redirect(url_for('index'))
		return render_template('login.html', 
							   title='Sign In',
							   form=form,
							   error=error)
						   
	except Exception as e:
		#return(str(e))							   
		error = "Invalid credentials, try again!"
		return render_template('login.html', title='Sign In',form=form,error=error)
		

@app.before_request
def before_request():
    g.user = current_user

	
					   
@lm.user_loader
def load_user(id):
    return User.query.get(int(id)) 
						   
						   
@app.route('/logout/')
def logout():
	logout_user()
	session.clear()
	flash("You have been logged out!")
	return redirect(url_for('index'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
	error = ''
	try:
		form = RegistrationForm(request.form)
		
		if form.validate_on_submit():
			u = form.username.data
			#p = sha256_crypt.encrypt((str(form.password.data)))
			p = form.password.data
			e = form.email.data
			d = datetime.datetime.utcnow()
			user = User(username=u, password=p, email=e, regdate=d)
			db.session.add(user)
			db.session.commit()
			session['logged_in'] = True
			login_user(user)
			flash('User successfully registered')
			return redirect(url_for('index'))
		#flash(form.errors)
		return render_template('register.html',form=form,error=error)
	except Exception as e:
		return render_template('register.html',form=form,error=error)