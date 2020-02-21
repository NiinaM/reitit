from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, validators
from application.stops.models import Stop


class RouteForm(FlaskForm):
    name = StringField("Route name", [validators.DataRequired()])

    class Meta:
        csrf = False


class AttachStopForm(FlaskForm):
    stop = SelectField("Stop", validators=[validators.DataRequired()],)

    class Meta:
        csrf = False
