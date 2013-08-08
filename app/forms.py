from flask.ext.wtf import Form, TextField, PasswordField, SubmitField
from flask.ext.wtf import Required, EqualTo, Length
from models import User

class LoginForm(Form):
  username = TextField('Username', [Required()])
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