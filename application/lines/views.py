from flask import abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
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
        is_favorite = db.session.execute(
            select([favorites])
            .where(favorites.c.user_id == current_user.id)
            .where(favorites.c.user_id == found_line.id)
        ).first()

    return render_template(
        "lines/single.html", line=found_line, is_favorite=is_favorite
    )


@app.route("/lines/<line_id>/edit", methods=["GET"])
@app.route("/lines/<line_id>/edit/", methods=["GET"])
@login_required
def lines_single_edit_form(line_id):
    found_line = Line.query.get(line_id)
    form = LineForm(request.form, name=found_line.name)
    return render_template("lines/edit.html", form=form, line=found_line)


@app.route("/lines/<line_id>", methods=["POST"])
@app.route("/lines/<line_id>/", methods=["POST"])
@login_required
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
@login_required
def lines_single_delete(line_id):
    found_line = Line.query.get(line_id)
    db.session.delete(found_line)

    try:
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()


@app.route("/lines/create")
@app.route("/lines/create/")
@login_required
def lines_form():
    return render_template("lines/create.html", form=LineForm())


@app.route("/lines", methods=["POST"])
@app.route("/lines/", methods=["POST"])
@login_required
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
