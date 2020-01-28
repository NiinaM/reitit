from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, bcrypt, db
from application.auth.models import User
from application.auth.forms import LoginForm, RegistrationForm


@app.route("/auth/login", methods=["GET", "POST"])
@app.route("/auth/login/", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data).first()
    password_matches = (
        bcrypt.check_password_hash(user.password, form.password.data) if user else False
    )

    if user is None or password_matches is False:
        return render_template(
            "auth/loginform.html", form=form, error="No such username or password."
        )

    login_user(user)
    return redirect(url_for("index"))


@app.route("/auth/logout")
@app.route("/auth/logout/")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/auth/register", methods=["GET", "POST"])
@app.route("/auth/register/", methods=["GET", "POST"])
def auth_registration():
    if request.method == "GET":
        return render_template("auth/registrationform.html", form=RegistrationForm())

    form = RegistrationForm(request.form)

    password_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

    # check that password matches with verification field
    if not bcrypt.check_password_hash(password_hash, form.password_verification.data):
        setattr(form.password_verification, "errors", ["Passwords do not match."])
        return render_template("auth/registrationform.html", form=form)

    created_user = User(form.name.data, form.username.data, password_hash)
    db.session.add(created_user)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        setattr(form.username, "errors", ["Username already exists."])
        return render_template("auth/registrationform.html", form=form)

    login_user(created_user)
    return redirect(url_for("index"))

