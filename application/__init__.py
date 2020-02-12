from os import environ
import secrets
from flask import Flask
from flask_user import UserManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

from flask_sqlalchemy import SQLAlchemy

if environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lines.db"
    app.config["SQLALCHEMY_ECHO"] = True

# flask user settings
app.config["USER_APP_NAME"] = "Reitit"
app.config["USER_ENABLE_EMAIL"] = False
app.config["USER_ENABLE_USERNAME"] = True
app.config["USER_ENABLE_CHANGE_USERNAME"] = False
app.config["USER_ENABLE_CHANGE_PASSWORD"] = False
app.config["SECRET_KEY"] = secrets.token_urlsafe(32)

db = SQLAlchemy(app)

# application features and views
from application import database
from application import views

from application.lines import models
from application.lines import views

from application.auth import models
from application.auth import forms
from application.auth.models import User

from application.favorites import models
from application.favorites import views

# application login
class CustomUserManager(UserManager):
    def customize(self, app):
        self.RegisterFormClass = forms.RegistrationForm


user_manager = CustomUserManager(app, db, User)

# initialize database
try:
    database.init_db(db, user_manager)
except:
    print("Error during database initialization")
