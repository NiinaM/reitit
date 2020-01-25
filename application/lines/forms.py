from flask_wtf import FlaskForm
from wtforms import StringField, validators


class LineForm(FlaskForm):
    name = StringField(
        "Line name", [validators.DataRequired(), validators.Length(min=1)]
    )

    class Meta:
        csrf = False
