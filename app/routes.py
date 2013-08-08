from flask import request, render_template, flash, redirect, g, session, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from werkzeug import check_password_hash, generate_password_hash
from app import app, db, login_manager
from forms import LoginForm, SignupForm, EditForm, PostForm
from models import User, Post
from datetime import datetime

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

@app.route('/', methods = ['GET', 'POST'])
def home():
  if g.user.is_authenticated():
    return redirect(url_for('user', username = g.user.username))
  return render_template("index.html",
    title = 'Home',
    posts = posts)

@app.route('/users')
def users():
  users = User.query.all()
  posts = Post.query.all()
  return render_template("users.html",
    title = 'Users',
    posts = posts,
    users = users)

@app.route('/login')
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
  posts = user.posts.order_by("timestamp desc").all()
  return render_template('user.html',
    user = user,
    posts = posts)

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
  form = EditForm(request.form)
  if form.validate_on_submit():
    g.user.name = form.name.data
    g.user.username = form.username.data
    db.session.add(g.user)
    db.session.commit()
    flash('Your changes have been saved.', 'success')
    return redirect(url_for('edit'))
  else:
    form.name.data = g.user.name
    form.username.data = g.user.username
  return render_template('edit.html',
    form = form)

@app.route('/posts/new', methods = ['GET', 'POST'])
@login_required
def new_post():
  form = PostForm(request.form)
  if form.validate_on_submit():
    post = Post(content = form.post.data, timestamp = datetime.utcnow(), author = g.user)
    db.session.add(post)
    db.session.commit()
    flash('Your post is now live!', 'success')
    return redirect(url_for('user', username = current_user.username))
  return render_template('new_post.html',
    title = 'New Post',
    form = form)
