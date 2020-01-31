from application import db


class Line(db.Model):
    __tablename__ = "line"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    name = db.Column(db.String(144), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

