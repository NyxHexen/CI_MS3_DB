from flask import (
    flash, render_template,
    redirect, request, session, url_for)
from flask_login import login_user, current_user, logout_user, login_required
from devbus import db, app, bcrypt
from devbus.forms import RegistrationForm, LoginForm
from devbus.models import User, Post


@app.route("/")
def home():
    posts = Post.objects()
    return render_template("home.html",posts=posts)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
                    f_name=form.f_name.data,
                    l_name=form.l_name.data,
                    email=form.email.data)
        user.save()
        flash("Account created successfully!", "light-green black-text lighten-2")
        return redirect(url_for('signin'))
    return render_template("signup.html", title="Sign Up", form=form)


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        print(user)
        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next = request.args.get('next')
            flash(f"Hi, {user.f_name}!" if user.f_name else f"Welcome, {user.username}!")
            return redirect(next) if next else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your email or password.', 'materialize-red lighten-1')
    return render_template("signin.html", title="License and Registration", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", title="Profile")