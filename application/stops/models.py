from application import db
from application.models import Base


class Stop(Base):
    __tablename__ = "stop"

    name = db.Column(db.String(144), nullable=False)

    def __init__(self, name):
        self.name = name

