from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from __init__ import app, db, lm
from forms import LoginForm, RegistrationForm, EditForm, PostForm
from models import User, Post
from datetime import datetime
from passlib.hash import sha256_crypt
from config import POSTS_PER_PAGE


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
@app.route('/index/', methods=['GET', 'POST'])
@app.route('/index/<int:page>/', methods=['GET', 'POST'])
@login_required
def index(page=1):
	try:
		form = PostForm()
		if form.validate_on_submit():
			post = Post(body=form.post.data, timestamp=datetime.utcnow(), author=g.user)
			db.session.add(post)
			db.session.commit()
			flash('Your post is now live!')
			return redirect(url_for('index'))

		posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
		return render_template('index.html',title='Home',form=form,posts=posts)		   
	
	except Exception as e:
		return(str(e))	

@app.route('/login/', methods=['GET', 'POST'])
def login():
	error = ''
	try:
		form = LoginForm()
		if form.validate_on_submit():
			session['remember_me'] = form.remember_me.data
			u = form.username.data
			p = form.password.data
			
			#flash('form error %s' % form.errors)
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
				#make the user follow him/herself
				db.session.add(user.follow(user))
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
@app.route('/user/<username>/<int:page>/')
@login_required
def user(username, page=1):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))
    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
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
	
	
@app.route('/follow/<username>/')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t follow yourself!')
        return redirect(url_for('user', username=username))
    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow ' + username + '.')
        return redirect(url_for('user', username=username))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + username + '!')
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>/')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('user', username=username))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow ' + username + '.')
        return redirect(url_for('user', username=username))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + username + '.')
    return redirect(url_for('user', username=username))