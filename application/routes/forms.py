from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, validators
from application.stops.models import Stop


class RouteForm(FlaskForm):
    name = StringField("Route name", [validators.DataRequired()])

    class Meta:
        csrf = False


class AttachStopForm(FlaskForm):
    stop_choices = Stop.query.order_by(Stop.name.asc()).all()
    stop = SelectField(
        "Stop",
        choices=[(single_stop.id, single_stop.name) for single_stop in stop_choices],
        validators=[validators.DataRequired()],
    )

    class Meta:
        csrf = False
