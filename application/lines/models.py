from application import db
from application.models import Base


class Line(Base):
    __tablename__ = "line"

    name = db.Column(db.String(144), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

