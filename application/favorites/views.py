from flask import abort
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError

from application import app, db
from application.lines.models import Line
from application.favorites.models import favorites


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

