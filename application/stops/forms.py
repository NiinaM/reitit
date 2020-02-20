from flask_wtf import FlaskForm
from wtforms import StringField, validators


class StopForm(FlaskForm):
    name = StringField("Stop name", [validators.DataRequired()])

    class Meta:
        csrf = False
