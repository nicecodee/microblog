from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from __init__ import app, db, lm
from forms import LoginForm, RegistrationForm, EditForm
from models import User
from datetime import datetime
from passlib.hash import sha256_crypt


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

	
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
    return render_template('index.html',title='Home',user=user,posts=posts)
						   
						   

@app.route('/login/', methods=['GET', 'POST'])
def login():
	error = ''
	try:
		form = LoginForm()
		if form.validate_on_submit():
			session['remember_me'] = form.remember_me.data
			u = form.username.data
			p = form.password.data
			#check username 
			if User.query.filter_by(username=u).first() is not None:
				user = User.query.filter_by(username=u).first()
				tmp_p = user.password
				#check password hash matching
				if sha256_crypt.verify(p, tmp_p):
					session['logged_in'] = True
					login_user(user)
					flash("You are now logged in!")
					return redirect(url_for('index'))
				
			flash("Invalid credentials, try again!")	
		return render_template('login.html', title='Sign In',form=form,error=error)
						   
	except Exception as e:
		#return(str(e))	
		error = "Invalid credentials, try again!"
		return render_template('login.html', title='Sign In',form=form,error=error)
		

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
	
					   
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
			recommend_name = User.make_unique_username(u)
			
			#flash('1st error %s' % form.errors)
			#check duplicated username
			if User.query.filter_by(username=u).first() is not None:		
				flash('username taken!  Try another. For example: %s' % recommend_name)
				#flash('2nd error %s' % form.errors)
				return render_template('register.html', form=form,error=error)
			else:
				p = sha256_crypt.encrypt((str(form.password.data))) #hash the password
				e = form.email.data
				d = datetime.utcnow()
				user = User(username=u, password=p, email=e, regdate=d)
				db.session.add(user)
				db.session.commit()
				session['logged_in'] = True
				login_user(user)
				flash('User successfully registered')
				#flash('3rd error %s' % form.errors)
				return redirect(url_for('index'))
			#flash('4th error %s' % form.errors)
		return render_template('register.html',form=form,error=error)
	except Exception as e:
		#return(str(e))
		#flash('5th error %s' % form.errors)
		return render_template('register.html',form=form,error=error)
		
		
@app.route('/user/<username>/')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user == None:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html',user=user,posts=posts)	


@app.route('/edit/', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.username)
    if form.validate_on_submit():
        g.user.username = form.username.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.username.data = g.user.username
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)	