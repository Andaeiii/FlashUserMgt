# this is using flask-security
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore

# SQLAlchemyuserdatastore - to connect the databse to flask security..

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mainsec.db'

db = SQLAlchemy(app)

# each user can have many roles...
# and each role can belong to many users..
# so we need to create an association table....

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer,
                                 db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer,
                                 db.ForeignKey('role.id')))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    confirm_at = db.Column(db.DateTime)  # needed by Flask security...


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(255))


# now we connect our models to flask security...
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
