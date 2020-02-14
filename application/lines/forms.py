from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, validators


class LineForm(FlaskForm):
    number = IntegerField(
        "Line number",
        [validators.DataRequired(), validators.NumberRange(min=1, max=999)],
    )
    specifier = StringField(
        "Line specifier",
        [
            validators.Optional(),
            validators.Regexp("^[A-Z]+", message="Only characters A-Z are allowed."),
        ],
    )

    class Meta:
        csrf = False
