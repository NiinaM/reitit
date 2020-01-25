from application import app, db
from flask import redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError
from application.lines.models import Line
from application.lines.forms import LineForm


@app.route("/lines", methods=["GET"])
@app.route("/lines/", methods=["GET"])
def lines_list():
    return render_template("lines/list.html", lines=Line.query.all())


@app.route("/lines/<line_id>", methods=["GET"])
@app.route("/lines/<line_id>/", methods=["GET"])
def lines_single(line_id):
    found_line = Line.query.get(line_id)
    return render_template("lines/single.html", line=found_line)


@app.route("/lines/<line_id>/edit", methods=["GET"])
@app.route("/lines/<line_id>/edit/", methods=["GET"])
def lines_single_edit_form(line_id):
    found_line = Line.query.get(line_id)
    form = LineForm(request.form, name=found_line.name)
    return render_template("lines/edit.html", form=form, line=found_line)


@app.route("/lines/<line_id>", methods=["POST"])
@app.route("/lines/<line_id>/", methods=["POST"])
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


@app.route("/lines/create")
@app.route("/lines/create/")
def lines_form():
    return render_template("lines/create.html", form=LineForm())


@app.route("/lines", methods=["POST"])
@app.route("/lines/", methods=["POST"])
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
