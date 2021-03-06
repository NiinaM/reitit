from application import db
from application.models import Base


class Route(Base):
    __tablename__ = "route"

    name = db.Column(db.String(144), nullable=False, unique=True)
    line_id = db.Column(db.Integer, db.ForeignKey("line.id"), nullable=False)
    stops = db.relationship("Stop", secondary="route_stop")

    def __init__(self, name):
        self.name = name


class RouteStop(db.Model):
    __tablename__ = "route_stop"
    id = db.Column(db.Integer(), primary_key=True)
    route_id = db.Column(db.Integer(), db.ForeignKey("route.id", ondelete="CASCADE"))
    stop_id = db.Column(db.Integer(), db.ForeignKey("stop.id", ondelete="CASCADE"))
