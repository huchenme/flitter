from flask import request, render_template, flash, redirect, g, session, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from werkzeug import check_password_hash, generate_password_hash
from app import app, db, login_manager
from forms import LoginForm, SignupForm
from models import User

@login_manager.user_loader
def load_user(id):
  return User.query.get(int(id))

@app.before_request
def before_request():
  g.user = current_user

@app.errorhandler(404)
def internal_error(error):
  return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
  db.session.rollback()
  return render_template('500.html'), 500

@app.route('/')
def home():
  user = { 'nickname': 'Miguel' } # fake user
  posts = [ # fake array of posts
  {
    'author': { 'nickname': 'John' },
    'body': 'Beautiful day in Portland!'
  },
  {
    'author': { 'nickname': 'Susan' },
    'body': 'The Avengers movie was so cool!'
  }
  ]
  return render_template("index.html",
    title = 'Home',
    user = user,
    posts = posts)

@app.route('/users')
def users():
  users = User.query.all()
  return render_template("users.html",
    title = 'Users',
    users = users)

@app.route('/login', methods = ['GET', 'POST'])
def login():
  form = LoginForm(request.form)
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data.lower()).first()
    if user and check_password_hash(user.password, form.password.data):
      login_user(user, remember = True)
      flash('Welcome %s!' % user.name, 'success')
      return redirect(request.args.get('next') or url_for('home'))
    flash('Wrong username or password', 'danger')
  return render_template('login.html',
    title = 'Sign In',
    form = form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm(request.form)
  if form.validate_on_submit():
    # create an user instance not yet stored in the database
    user = User(name=form.name.data, username=form.username.data, \
      password=form.password.data)
    # Insert the record in our database and commit it
    db.session.add(user)
    db.session.commit()
    login_user(user, remember = True)

    # flash will display a message to the user
    flash('Thanks for signing up', 'success')
    # redirect user to the 'home' method of the user module.
    return redirect(url_for('home'))
  return render_template("signup.html", form=form)

@app.route('/logout')
def logout():
  logout_user()
  flash('You were logged out', 'success')
  return redirect(url_for('home'))

@app.route('/<username>')
def user(username):
  user = User.query.filter_by(username = username).first()
  if user == None:
    return render_template('404.html'), 404
  posts = [
      { 'author': user, 'body': 'Test post #1' },
      { 'author': user, 'body': 'Test post #2' }
  ]
  return render_template('user.html',
    user = user,
    posts = posts)

