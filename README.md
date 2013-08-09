# Flitter
a micro-blogging web app implemented using Flask framework.   
Live example: [http://flitter-flask.herokuapp.com](http://flitter-flask.herokuapp.com/)

### What is included

* register using username and password
* password hashed
* all the posts are sorted by date
* logged in user can see a "create new post" button
* using Bootstrap 3, bourbon, sass for styling
* client side validation for new post limit to 200 characters
* user URL: http://localhost:port/username
* 404 page and 500 page

### What is not included
Due to time limit, the following features are not included

* Facebook Oauth [reference](http://pythonhosted.org/Flask-OAuth/)
* Pagination [reference](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ix-pagination)

### Setup on Local machine

Install dependency:

```
pip install flask
pip install flask-login
pip install sqlalchemy
pip install flask-sqlalchemy
pip install sqlalchemy-migrate
pip install flask-wtf
pip install pytz==2013b
pip install flask-babel==0.8
pip install flup
```
Clone and run:

```
git clone git@github.com:huchenme/flitter.git
cd flitter
python db_create.py
python db_migrate.py
python run.py
```
You can now go to [http://localhost:5000](http://localhost:5000) to test the application
