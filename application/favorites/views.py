from operator import attrgetter
from flask import abort, render_template
from flask_user import current_user, login_required
from sqlalchemy.exc import IntegrityError

from application import app, db
from application.auth.models import User
from application.lines.models import Line
from application.favorites.models import favorites


@app.route("/favorites", methods=["GET"])
@app.route("/favorites/", methods=["GET"])
@login_required
def favorites_list():
    sorted_favorites = sorted(
        current_user.favorites, key=attrgetter("number", "specifier")
    )
    return render_template("favorites/list.html", lines=sorted_favorites)


@app.route("/favorites/<line_id>", methods=["POST"])
@app.route("/favorites/<line_id>/", methods=["POST"])
@login_required
def add_line_favorites(line_id):
    found_line = Line.query.get(line_id)
    current_user.favorites.append(found_line)

    try:
        db.session.commit()
        return "OK"
    except IntegrityError as error:
        db.session.rollback()

    abort(500)


@app.route("/favorites/<line_id>", methods=["DELETE"])
@app.route("/favorites/<line_id>/", methods=["DELETE"])
@login_required
def remove_line_favorites(line_id):
    found_line = Line.query.get(line_id)
    current_user.favorites.remove(found_line)

    try:
        db.session.commit()
        return "OK"
    except IntegrityError as error:
        db.session.rollback()

    abort(500)

