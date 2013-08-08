from app import db
from werkzeug import generate_password_hash, check_password_hash

class User(db.Model):
  # __tablename__ = 'users_user'
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(100), index = True, unique = True)
  name = db.Column(db.String(100))
  password = db.Column(db.String(100))
  # posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

  def __init__(self, name, username, password):
    self.name = name
    self.username = username.lower()
    self.set_password(password)

  def set_password(self, password):
    self.password = generate_password_hash(password)

  def __repr__(self):
    return '<User %r>' % (self.username)

  def is_authenticated(self):
      return True

  def is_active(self):
      return True

  def is_anonymous(self):
      return False

  def get_id(self):
      return unicode(self.id)

class Post(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  content = db.Column(db.String(200))
  timestamp = db.Column(db.DateTime)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
      return '<Post %r>' % (self.content)