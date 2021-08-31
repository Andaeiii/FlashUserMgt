import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter


app = Flask(__name__)


app.config['SECRET_KEY'] = 'thisisasecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myapp.db'

# other configuration values...
app.config['CSRF_ENABLED'] = True
app.config['USER_ENABLE_EMAIL'] = False

# create db for application ...
db = SQLAlchemy(app)


class User(db.Model, UserMixin):        # create table...
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')


# set up the flask_user config object....
db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)


@app.route('/')
def index():
    return 'this is the homepage....'


@app.route('/profile')
@login_required  # only accessible to people who are logged in..
def profile():
    return 'this is the profile page... '


if __name__ == '__main__':
    app.run(debug=True)
