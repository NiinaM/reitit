from application import db
from application.models import Base


class Line(Base):
    __tablename__ = "line"

    number = db.Column(db.Integer, nullable=False)
    specifier = db.Column(db.String(10), nullable=True)
    routes = db.relationship("Route", backref="line", lazy=True)

    def __init__(self, number, specifier):
        self.number = number
        self.specifier = specifier

    def get_name(self):
        return "".join([str(self.number), self.specifier if self.specifier else ""])

