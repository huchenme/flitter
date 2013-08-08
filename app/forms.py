from flask.ext.wtf import Form, TextField
from flask.ext.wtf import Required

class LoginForm(Form):
  openid = TextField('openid', validators = [Required()])