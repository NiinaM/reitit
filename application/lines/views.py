from flask import abort, redirect, render_template, request, url_for
from flask_user import current_user, login_required, roles_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import select

from application import app, db
from application.lines.models import Line
from application.auth.models import User
from application.favorites.models import favorites
from application.lines.forms import LineForm


@app.route("/lines", methods=["GET"])
@app.route("/lines/", methods=["GET"])
def lines_list():
    return render_template("lines/list.html", lines=Line.query.all())


@app.route("/lines/<line_id>", methods=["GET"])
@app.route("/lines/<line_id>/", methods=["GET"])
def lines_single(line_id):
    found_line = Line.query.get(line_id)

    is_favorite = False
    if current_user.is_authenticated:
        stmt = text(
            "SELECT COUNT(Line.id) FROM Line"
            " LEFT JOIN favorites ON favorites.line_id = Line.id"
            " WHERE (favorites.user_id = :current_user_id AND favorites.line_id = :current_line_id)"
        ).params(current_user_id=current_user.id, current_line_id=line_id)
        res = db.session.execute(stmt).first()

        is_favorite = res[0] > 0

    return render_template(
        "lines/single.html", line=found_line, is_favorite=is_favorite
    )


@app.route("/lines/<line_id>/edit", methods=["GET"])
@app.route("/lines/<line_id>/edit/", methods=["GET"])
@roles_required("admin")
def lines_single_edit_form(line_id):
    found_line = Line.query.get(line_id)
    form = LineForm(request.form, name=found_line.name)
    return render_template("lines/edit.html", form=form, line=found_line)


@app.route("/lines/<line_id>", methods=["POST"])
@app.route("/lines/<line_id>/", methods=["POST"])
@roles_required("admin")
def lines_single_edit(line_id):
    form = LineForm(request.form)
    found_line = Line.query.get(line_id)

    if not form.validate():
        return render_template("lines/edit.html", form=form, line=found_line)

    new_line = Line(form.name.data)
    found_line.name = new_line.name

    try:
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        setattr(form.name, "errors", ["Line already exists."])
        return render_template("lines/edit.html", form=form, line=found_line)

    return redirect(url_for("lines_single", line_id=line_id))


@app.route("/lines/<line_id>", methods=["DELETE"])
@app.route("/lines/<line_id>/", methods=["DELETE"])
@roles_required("admin")
def lines_single_delete(line_id):
    found_line = Line.query.get(line_id)
    db.session.delete(found_line)

    try:
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()


@app.route("/lines/create")
@app.route("/lines/create/")
@roles_required("admin")
def lines_form():
    return render_template("lines/create.html", form=LineForm())


@app.route("/lines", methods=["POST"])
@app.route("/lines/", methods=["POST"])
@roles_required("admin")
def lines_create():
    form = LineForm(request.form)

    if not form.validate():
        return render_template("lines/create.html", form=form)

    created_line = Line(form.name.data)

    db.session.add(created_line)

    try:
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        setattr(form.name, "errors", ["Line already exists."])
        return render_template("lines/create.html", form=form)

    return redirect(url_for("lines_list"))
