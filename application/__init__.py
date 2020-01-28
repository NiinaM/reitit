from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

# database init
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lines.db"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

# application features and views
from application import views

from application.lines import models
from application.lines import views

from application.auth import models
from application.auth import views

# application login
from application.auth.models import User
from os import urandom

app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# create database tables if necessary
db.create_all()
