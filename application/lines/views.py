from application import app, db
from flask import redirect, render_template, request, url_for
from application.lines.models import Line


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
    return render_template("lines/edit.html", line=found_line)


@app.route("/lines/<line_id>", methods=["POST"])
@app.route("/lines/<line_id>/", methods=["POST"])
def lines_single_edit(line_id):
    found_line = Line.query.get(line_id)
    found_line.name = request.form.get("name")
    db.session().commit()
    return redirect(url_for("lines_single", line_id=line_id))


@app.route("/lines/create")
@app.route("/lines/create/")
def lines_form():
    return render_template("lines/create.html")


@app.route("/lines", methods=["POST"])
@app.route("/lines/", methods=["POST"])
def lines_create():
    created_line = Line(request.form.get("name"))

    db.session.add(created_line)
    db.session.commit()

    return redirect(url_for("lines_list"))
