from flask import abort, redirect, render_template, request, url_for
from flask_user import roles_required
from sqlalchemy.exc import IntegrityError

from application import app, db
from application.stops.models import Stop
from application.routes.models import Route
from application.routes.forms import AttachStopForm, RouteForm


@app.route("/routes/<route_id>", methods=["GET"])
@app.route("/routes/<route_id>/", methods=["GET"])
def routes_single(route_id):
    found_route = Route.query.get(route_id)
    return render_template("routes/single.html", route=found_route)


@app.route("/routes/create?=<line_id>")
@app.route("/routes/create/?=<line_id>")
@roles_required("admin")
def routes_form(line_id):
    return render_template("routes/form.html", form=RouteForm(), line_id=line_id)


@app.route("/routes?=<line_id>", methods=["POST"])
@app.route("/routes/?=<line_id>", methods=["POST"])
@roles_required("admin")
def routes_create(line_id):
    form = RouteForm(request.form)

    if not form.validate():
        return render_template("routes/form.html", form=form, line_id=line_id)

    route_exists = Route.query.filter(
        Route.name == form.name.data, Route.line_id == line_id
    ).first()

    if route_exists:
        setattr(form.name, "errors", ["Route already exists."])
        return render_template("routes/form.html", form=form, line_id=line_id)

    created_route = Route(name=form.name.data)
    created_route.line_id = line_id

    db.session.add(created_route)

    try:
        db.session.commit()
        return redirect(url_for("lines_single", line_id=line_id))
    except:
        db.session.rollback()
        return render_template("routes/form.html", form=form, line_id=line_id)

    abort(500)


@app.route("/routes/<route_id>", methods=["DELETE"])
@app.route("/routes/<route_id>/", methods=["DELETE"])
@roles_required("admin")
def routes_single_delete(route_id):
    found_route = Route.query.get(route_id)
    db.session.delete(found_route)

    try:
        db.session.commit()
        return "OK"
    except IntegrityError as error:
        db.session.rollback()

    abort(500)


@app.route("/routes/<route_id>/edit", methods=["GET"])
@app.route("/routes/<route_id>/edit/", methods=["GET"])
@roles_required("admin")
def routes_single_edit_form(route_id):
    found_route = Route.query.get(route_id)
    form = RouteForm(request.form, name=found_route.name)
    return render_template(
        "routes/form.html", form=form, route=found_route, line_id=found_route.line_id
    )


@app.route("/routes/<route_id>", methods=["POST"])
@app.route("/routes/<route_id>/", methods=["POST"])
@roles_required("admin")
def routes_single_edit(route_id):
    form = RouteForm(request.form)
    found_route = Route.query.get(route_id)
    line_id = found_route.line_id

    if not form.validate():
        return render_template(
            "routes/form.html", form=form, route=found_route, line_id=line_id
        )

    route_exists = Route.query.filter(
        Route.name == form.name.data, Route.line_id == line_id
    ).first()

    if route_exists:
        setattr(form.name, "errors", ["Route already exists."])
        return render_template(
            "routes/form.html", form=form, route=found_route, line_id=line_id
        )

    new_route = Route(name=form.name.data)
    found_route.name = new_route.name

    try:
        db.session.commit()
        return redirect(url_for("lines_single", line_id=line_id))
    except:
        db.session.rollback()
        return render_template(
            "routes/form.html", form=form, route=found_route, line_id=line_id
        )

    abort(500)


@app.route("/routes/<route_id>/attach", methods=["GET"])
@app.route("/routes/<route_id>/attach/", methods=["GET"])
@roles_required("admin")
def attach_stop_form(route_id):
    found_route = Route.query.get(route_id)
    form = AttachStopForm(request.form)
    form.stop.choices = [
        (single_stop.id, single_stop.name)
        for single_stop in Stop.query.order_by(Stop.name.asc()).all()
    ]
    return render_template("routes/attach.html", form=form, route=found_route)


@app.route("/routes/<route_id>/attach", methods=["POST"])
@app.route("/routes/<route_id>/attach/", methods=["POST"])
@roles_required("admin")
def attach_stop(route_id):
    form = AttachStopForm(request.form)
    found_route = Route.query.get(route_id)
    found_stop = Stop.query.get(form.stop.data)
    found_route.stops.append(found_stop)

    try:
        db.session.commit()
        return redirect(url_for("routes_single", route_id=route_id))
    except:
        db.session.rollback()
        return render_template("routes/form.html", form=form, route=found_route)

    abort(500)


@app.route("/routes/<route_id>/attach/<stop_id>", methods=["DELETE"])
@app.route("/routes/<route_id>/attach/<stop_id>/", methods=["DELETE"])
@roles_required("admin")
def detach_stop(route_id, stop_id):
    found_route = Route.query.get(route_id)
    found_stop = Stop.query.get(stop_id)
    found_route.stops.remove(found_stop)

    try:
        db.session.commit()
        return "OK"
    except IntegrityError as error:
        db.session.rollback()

    abort(500)

