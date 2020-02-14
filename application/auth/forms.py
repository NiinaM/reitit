from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
from flask_user.forms import RegisterForm


class RegistrationForm(RegisterForm):
    # Add a country field to the Register form
    name = StringField("Name", validators=[validators.DataRequired()])
