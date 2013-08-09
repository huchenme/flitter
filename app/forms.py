from flask.ext.wtf import Form, TextField, PasswordField, SubmitField, TextAreaField
from flask.ext.wtf import Required, EqualTo, Length
from flask import g
from models import User

class LoginForm(Form):
  user_name = TextField('Username', [Required()])
  password = PasswordField('Password', [Required()])
  submit = SubmitField("Login")

class SignupForm(Form):
  name = TextField('Full Name', [Required(), Length(min=2)])
  username = TextField('Username', [Required(), Length(min=2)])
  password = PasswordField('Password', [Required(), Length(min=6)])
  confirm = PasswordField('Repeat Password', [
    EqualTo('password', message="Passwords must match")
    ])
  submit = SubmitField("Sign up")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    user = User.query.filter_by(username = self.username.data.lower()).first()
    if user:
      self.username.errors.append("The username is already taken")
      return False
    else:
      return True

class EditForm(Form):
  name = TextField('Full Name', [Required(), Length(min=2)])
  username = TextField('Username', [Required(), Length(min=2)])
  submit = SubmitField("Save changes")

  def validate(self):
    if not Form.validate(self):
      return False
    if g.user.username != self.username.data.lower():
      user = User.query.filter_by(username = self.username.data.lower()).first()
      if user:
        self.username.errors.append("The Username is already taken")
        return False
      else:
        return True
    else:
      return True

class PostForm(Form):
  post = TextAreaField('Say something...', [Required(), Length(max=200)])
  submit = SubmitField('Post!')