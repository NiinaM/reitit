from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, validators


class RouteForm(FlaskForm):
    name = StringField("Route name", [validators.DataRequired()],)

    class Meta:
        csrf = False
