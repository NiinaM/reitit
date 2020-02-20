from application import db

route_stop = db.Table(
    "route_stop",
    db.Column(
        "route_id",
        db.Integer,
        db.ForeignKey("route.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "stop_id",
        db.Integer,
        db.ForeignKey("stop.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
