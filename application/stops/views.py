from flask import abort, redirect, render_template, request, url_for
from flask_user import current_user, login_required, roles_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import cast, func, select

from application import app, db
from application.stops.models import Stop
from application.stops.forms import StopForm


@app.route("/stops", methods=["GET"])
@app.route("/stops/", methods=["GET"])
def stops_list():
    return render_template(
        "stops/list.html", stops=Stop.query.order_by(Stop.name.asc()).all(),
    )


@app.route("/stops/create")
@app.route("/stops/create/")
@roles_required("admin")
def stops_form():
    return render_template("stops/form.html", form=StopForm())


@app.route("/stops", methods=["POST"])
@app.route("/stops/", methods=["POST"])
@roles_required("admin")
def stops_create():
    form = StopForm(request.form)

    if not form.validate():
        return render_template("stops/form.html", form=form)

    stop_exists = Stop.query.filter(Stop.name == form.name.data).first()

    if stop_exists:
        setattr(form.name, "errors", ["Stop already exists."])
        return render_template("stops/form.html", form=form)

    created_stop = Stop(name=form.name.data)
    db.session.add(created_stop)

    try:
        db.session.commit()
        return redirect(url_for("stops_list"))
    except:
        db.session.rollback()
        return render_template("stops/form.html", form=form)

    abort(500)
