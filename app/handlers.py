"""Handlers for app"""
from crypt import methods

import sqlalchemy
from app.models import Users, Items, Feedback
from app.app import app, db
from flask import (
    make_response,
    redirect,
    render_template,
    escape,
    abort,
    request,
    session,
    url_for,
    flash,
)
from datetime import datetime, timedelta

# //app.register_error_handler('404.html', page_not_found)


@app.errorhandler(404)
def page_not_found(_):
    """Handles 404"""
    return render_template("404.html"), 404


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handles login"""
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        try:
            if Users.query.filter_by(name=name).one().validate(password):
                session["name"] = name
                flash(f"Welcome back, {name}", "success")
                return redirect(url_for("index"), code=301)
            flash("Wrong login or password", "warning")
        except sqlalchemy.exc.NoResultFound:
            flash("Wrong login or password", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Handles logout"""
    if session.get("name"):
        session.pop("name")
    return redirect("/", code=302)


@app.route("/<name>", methods=["GET", "POST"])
def profile(name):
    """Handles password changing"""
    if session.get("name") == name:
        if (user := Users.query.filter_by(name=name)) is not None:
            if request.method == "POST":
                user = user.one()
                old = request.form.get("old_password")
                new = request.form.get("new_password")
                if old == new:
                    flash("Новый пароль тот же, что и старый", "warning")
                elif user.validate(old):
                    user.set_password(new)
                    flash("Пароль изменен", "success")
                    db.session.add(user)
                    db.session.commit()
            return render_template("profile.html", user=user)
    flash("Please authenticate", "warning")
    return redirect(url_for("login"), code=301)


@app.route("/")
def index():
    """Handles main page"""
    resp = make_response(render_template("index.html"))
    if not request.cookies.get("test"):
        resp.set_cookie(
            "test", "testvalue", expires=datetime.now() + timedelta(minutes=30)
        )
    return resp


@app.route("/about", methods=["GET", "POST"])
def about():
    """Handles about us page"""
    feedback = Feedback.query.all()
    if request.method == "POST":
        name = request.form.get("login")
        text = request.form.get("text")
        if login != "" and text != "":
            feed = Feedback(name=name, text=text)
            db.session.add(feed)
            db.session.commit()
            feedback.append(feed)
    print(feedback)
    return render_template("about.html", feedback=feedback)


@app.route("/catalog")
def catalog():
    """Handles catalog"""
    min_price = int(request.args.get("min_price", 0))
    max_price = int(request.args.get("max_price", 10e9))
    items = Items.query.all()
    items = list(filter(lambda x: min_price <= x.price <= max_price, items))
    return render_template("catalog.html", items=items)


@app.route("/item/<item>")
def show_item_profile(item):
    """Handles item profile"""
    item = escape(item)
    return render_template("item.html", item=Items.query.filter_by(name=item).one())


@app.route("/register", methods=["GET", "POST"])
def reg():
    """Handles registration"""
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        try:
            Users.query.filter_by(name=name).one()
            flash("Name exists, choose another", "warning")
        except sqlalchemy.exc.NoResultFound as e:
            print(e, e.args)
            user = Users(name, password)
            db.session.add(user)
            db.session.commit()
            session["name"] = name
            flash(f"Welcome mr.{name}", "success")
            return redirect(url_for("index"))
    return render_template("reg.html")
