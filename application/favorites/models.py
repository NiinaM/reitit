from application import db

favorites = db.Table(
    "favorites",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("line_id", db.Integer, db.ForeignKey("line.id"), primary_key=True),
)
