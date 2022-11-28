from flask import (
    flash, render_template,
    redirect, request, url_for, Blueprint)
from flask_login import login_user, current_user, logout_user, login_required
from itsdangerous import TimedSerializer
from devbus import bcrypt
from devbus.auth.forms import SignUpForm, SignInForm, UpdateProfileForm, ForgotPwdForm
from devbus.auth.utils import upload_image
from devbus.utils.models import User


auth = Blueprint('auth', '__name__')

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username = form.username.data,
                    password = bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
                    f_name = form.f_name.data,
                    l_name = form.l_name.data,
                    email = form.email.data)
        user.save()
        flash("Account created successfully!", "light-green black-text lighten-2")
        return redirect(url_for('auth.signin'))
    return render_template("signup.html", title="Sign Up", form=form)


@auth.route("/signin", methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SignInForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next = request.args.get('next')
            flash(f"Hi, {user.f_name}!" if user.f_name else f"Welcome, {user.username}!")
            return redirect(next) if next else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check your email or password.', 'materialize-red lighten-1')
    return render_template("signin.html", title="License and Registration", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@auth.route("/profile")
@login_required
def profile():
    form = UpdateProfileForm()
    return render_template("profile.html", title="Profile", form=form)


@auth.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        form.populate_obj(current_user)
        if form.profile_image.data:
            image_url = upload_image(form.profile_image.data)
            current_user.profile_image = image_url
        current_user.save()
        flash('Got it! Your profile has been updated.', 'message')
        return redirect('/profile')
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.f_name.data = current_user.f_name
        form.l_name.data = current_user.l_name
        form.languages.data = current_user.languages
        form.bio.data = current_user.bio
    return render_template("edit_profile.html", title="Edit Profile", form=form)


@auth.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated: 
        return redirect("home")
    form = ForgotPwdForm()
    if form.validate_on_submit():
        user = User.objects.get(email=form.email.data)
        print(user.generate_pw_token())
    return render_template("forgot_password.html", title="Forgotten Password?", form=form)