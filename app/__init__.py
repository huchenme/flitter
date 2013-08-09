import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from momentjs import momentjs
app.jinja_env.globals['momentjs'] = momentjs

from app import routes, models

if not app.debug and os.environ.get('HEROKU') is None:
  import logging
  from logging.handlers import RotatingFileHandler
  file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
  file_handler.setLevel(logging.INFO)
  file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
  app.logger.addHandler(file_handler)
  app.logger.setLevel(logging.INFO)
  app.logger.info('microblog startup')

if os.environ.get('HEROKU') is not None:
  import logging
  stream_handler = logging.StreamHandler()
  app.logger.addHandler(stream_handler)
  app.logger.setLevel(logging.INFO)
  app.logger.info('microblog startup')