#!flask/bin/python
from app import app
# disable debug in production
app.run(debug = True)