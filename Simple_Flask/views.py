from flask import Flask, render_template, url_for, request, redirect, flash, abort
from flask_login import login_required, login_user, current_user, logout_user, AnonymousUserMixin
from Simple_Flask import logger
from Simple_Flask.forms import LoginForm, SignupForm, ChangePasswordForm
from Simple_Flask.models import User
from Simple_Flask import app, db, login_manager, models
import os

basedir = os.path.abspath(os.path.dirname(__file__))
Logger = logger.Logger()
Logger.log("Started.")


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    password=form.password.data,
                    role="Pending")
        if not User.query.all():
            user.role = "Admin" # first user created is Admin
        db.session.add(user)
        db.session.commit()
        flash("welcome {}! please login.".format(user.email))
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)


@app.route("/change_password/<user_id>", methods=["GET", "POST"])
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password(user_id=None):  # a flask view function
    form = ChangePasswordForm()
    if current_user.role == "Admin" and user_id is not None:
        user = User.get_user_by_id(user_id)
    else:
        user = User.get_user_by_id(current_user.id)
    if form.validate_on_submit():
        user.password=form.password.data
        db.session.commit()
        flash("password for {} changed.".format(user.email))
        return redirect(url_for('index'))
    return render_template("change_password.html", form=form, user=user)



@app.route("/enable_user/<user_id>")
@login_required
def enable_user(user_id=None):
    if current_user.role=="Admin":
        user = User.get_user_by_id(user_id)
        user.role = "Enabled"
        db.session.commit()
        return redirect(url_for("admin"))
    else:
        return redirect(url_for("index"))


@app.route("/disable_user/<user_id>")
@login_required
def disable_user(user_id=None):
    if current_user.role=="Admin":
        user = User.get_user_by_id(user_id)
        user.role = "Disabled"
        db.session.commit()
        return redirect(url_for("admin"))
    else:
        return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user_by_email(form.email.data)
        # don't allow login for users not yet enabled
        if user.role == "Pending":
            flash("Your account is not activated yet. Please contact your administrator")
            Logger.log("LOGIN PENDING - users IP:{0} USER:{1} ROLE:{2}".format(
                request.remote_addr, user.email, user.role))
        elif user.role == "Disabled":
            flash("Your account is disabled. Please contact your administrator")
            Logger.log("LOGIN DISABLED - users IP:{0} USER:{1} ROLE:{2}".format(
                request.remote_addr, user.email, user.role))
        else: # if account has a valid role, and password is correct, then login
            if user is not None and user.check_password(form.password.data):
                login_user(user, form.remember_me.data)
                flash("Logged in as {}.".format(user.email))
                Logger.log("LOGIN SUCCEEDED - users IP:{0} USER:{1} ROLE:{2}".format(
                    request.remote_addr, current_user.email, current_user.role))
                return redirect(url_for('index'))
            else: # other reasons for failure
                Logger.log("LOGIN FAILED - users IP:{0} USER:{1} ROLE:{2}".format(
                    request.remote_addr, user.email, user.role))
                flash('Incorrect username or password')
    return render_template("login.html", form=form)


# send to login page when a user accesses a page they are not authorised to
login_manager.unauthorized_callback = login


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if current_user.role=="Admin":
        return render_template("admin.html")
    else:
        flash("You are not an administrator. This event has been logged.")
        Logger.log("ACCESS VIOLATION - users IP:{0} USER:{1} ROLE:{2}".format(
            request.remote_addr, current_user.email, current_user.role))
        return redirect(url_for("index"))


@app.route ("/drop")
@login_required
def drop():
    if current_user.role == "Admin":
        db.drop_all()
        message = "DROP DONE."
    else:
        message = "NO"
    return message, 200


@app.route ("/init")
def init():
    r = db.create_all()
    return "INIT DONE "+str(r),200


@app.route("/index", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
@login_required
def index():  # a flask view function
    return render_template("index.html")


@app.context_processor
def inject_tags():
    return dict(users=User.query.all())


@app.errorhandler(404)
@app.errorhandler(405)
def server_error(e):
    Logger.log("ERR404 IP:{0} URL:{1}".format(request.remote_addr, request.url))
    return render_template("404.html"), 404

