from __init__ import db
from hashlib import md5

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	password = db.Column(db.String(20))
	email = db.Column(db.String(120), index=True, unique=True)
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	regdate = db.Column(db.DateTime)
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime)	
		

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id)  # python 2
		except NameError:
			return str(self.id)  # python 3		
				
	def __repr__(self):
		return '<User %r>' % (self.username)

	# Newly added for user avatars
	def avatar(self, size):
		return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)		

	#to make the username unique		
	@staticmethod
	def make_unique_username(username):
		if User.query.filter_by(username=username).first() is None:
			return username
		version = 2
		while True:
			new_username = username + str(version)
			if User.query.filter_by(username=new_username).first() is None:
				break
			version += 1
		return new_username		
		
		
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)