from flask_user import UserMixin
from application import db
from application.models import Base
from application.favorites import models


class User(Base, UserMixin):
    __tablename__ = "user"

    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default="")
    active = db.Column(db.Boolean(), nullable=False, server_default="1")
    roles = db.relationship("Role", secondary="user_role")
    favorites = db.relationship(
        "Line", secondary=models.favorites, lazy="subquery", backref="users",
    )


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRole(db.Model):
    __tablename__ = "user_role"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer(), db.ForeignKey("role.id", ondelete="CASCADE"))
