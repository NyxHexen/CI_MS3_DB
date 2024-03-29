import os
from flask import (
    flash, render_template,
    redirect, request, url_for, Blueprint, abort)
from flask_login import login_user, current_user, logout_user, login_required
from itsdangerous import SignatureExpired
from devbus import bcrypt
from devbus.auth.forms import (
    SignUpForm, SignInForm, UpdateProfileForm,
    DeleteAccountForm, ForgotPwdForm, NewPwdForm,
    ChangePwdForm)
from devbus.auth.utils import upload_image, send_reset_email
from devbus.utils.models import User, Post, Comment


auth = Blueprint('auth', '__name__')


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Registers a new user in the users collection,
    then if successful redirects to the sign in page.
    """
    if current_user.is_authenticated:
        return redirect("/")
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password = (
                        bcrypt.generate_password_hash(form.password.data)
                        .decode('utf-8')),
                    f_name = form.f_name.data,
                    l_name = form.l_name.data,
                    email = form.email.data)
        user.save()
        flash("Account created successfully!",
              "light-green black-text lighten-2")
        return redirect(url_for('auth.signin'))
    return render_template("auth/signup.html", title="Sign Up", form=form)


@auth.route("/signin", methods=["GET", "POST"])
def signin():
    """
    Checks if user exists and logs in the users,
    then if successful redirects them to the page they
    wanted to access or home page.
    """
    if current_user.is_authenticated:
        flash("You are already logged in!", "yellow black-text")
        return redirect("/")
    form = SignInForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if ((user is not None) and
                bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember=form.remember.data)
            next = request.args.get('next')
            flash((f"Hi, {user.f_name}!"
                   if user.f_name else f"Welcome, {user.username}!"))
            return redirect(next) if next else redirect("/")
        else:
            flash('Login Unsuccessful. Please check your email or password.',
                  'red darken-2')
    return render_template("auth/signin.html",
                           title="License and Registration", form=form)


@auth.route("/logout")
def logout():
    """
    Logs out user and redirects to home page.
    """
    logout_user()
    return redirect("/")


@auth.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """
    Renders the user's profile/account and handles
    the delete button functionality.
    In order to delete their account, the user must
    provide their password.
    """
    user = User.objects.get(id=current_user.id)
    form = DeleteAccountForm()
    if (form.validate_on_submit()
            and bcrypt.check_password_hash(user.password, form.password.data)):
        return redirect(f"/profile/_{current_user.id}/delete_user")
    elif (form.validate_on_submit()
            and not bcrypt.check_password_hash(
                    user.password, form.password.data)):
        flash("Incorrect password. Please try again.", 'red')
    return render_template("auth/profile.html", title="Profile", user=user,
                           form=form)


@auth.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    """
    This function renders the edit profile template,
    and allows the user to change their profile details.
    """
    form = UpdateProfileForm()
    if form.validate_on_submit():
        form.populate_obj(current_user)
        if form.profile_image.data is not None:
            img_url = upload_image(form.profile_image.data)
            current_user.profile_image = img_url
        elif form.profile_image.data is None:
            """
            populate_obj method is destructive, so to ensure that the member's
            picture doesn't get overwritten to the default one every time they
            update their profile we must re-assign it's value from db before it
            is saved.
            """
            current_user.profile_image = (User.objects.get(id=current_user.id)
                                          .profile_image)
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
        form.profile_image.data = current_user.profile_image
    return render_template("auth/edit_profile.html", title="Edit Profile",
                           form=form)


@auth.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    """
    This function helps users who have forgotten their password.
    Upon entering e-mail address that is in already in the DB,
    flask-mail sends an email with a password reset token link.
    """
    if current_user.is_authenticated:
        flash("You are already logged in!", "yellow black-text")
        return redirect("/")
    form = ForgotPwdForm()
    if form.validate_on_submit():
        user = User.objects.get(email=form.email.data)
        if user is not None:
            reset_email = send_reset_email(user)
            if reset_email is not False:
                flash(
                    '''Thanks! If you have an account with us
                 you will shortly receive an e-mail
                 with instructions on how to reset your password.''')
                return redirect("/signin")
            else:
                flash('''Connection timed out. Please try again in a
                 few minutes.''', "yellow black-text")
                return redirect('/forgot_password')
    return render_template("auth/forgot_password.html",
                           title="Forgotten Password?", form=form)


@auth.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """
    Route is accessed by accessing the reset password token link
    which flask-mail sends via e-mail when the user submits the
    forgot_password form. If token is valid, the user is able to
    choose a new password. If the token is expired, they are
    redirected to login.
    """
    if current_user.is_authenticated:
        flash("You are already logged in!", "yellow black-text")
        return redirect("/")
    form = NewPwdForm()
    try:
        user_id = User.verify_pwd_token(token)
    except SignatureExpired:
        flash("This token is no longer valid. Please try again!",
              "materialize-red")
        return redirect("/signin")
    user = User.objects.get(id=user_id)
    if form.validate_on_submit():
        user.password = (bcrypt.generate_password_hash(form.password.data)
                         .decode('utf-8'))
        user.save()
        flash("Your password has been reset! You can now login.", "green")
        return redirect("/signin")
    return render_template("auth/reset_password.html", title="Reset Password",
                           form=form)


@auth.route("/profile/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """
    Route is accessed through the user's profile and
    allows the user to change their password by providing
    current and new password.
    """
    form = ChangePwdForm()
    user = User.objects.get(id=current_user.id)
    if form.validate_on_submit():
        user.password = (bcrypt.generate_password_hash(form.new_password.data)
                         .decode('utf-8'))
        user.save()
        flash("Your password has been reset! You can now login.", "green")
        return redirect("/signin")
    return render_template("auth/change_password.html",
                           title="Change Password", form=form)


@auth.route("/profile/_<id>/delete_user", methods=["GET", "POST"])
@login_required
def delete_user(id):
    """
    This function does not render a template, but instead
    actions the user deletion requests and then redirects to
    the home page.
    When called, this function deletes all posts, comments,
    subcomments that the user has added, then also deletes user account.
    """
    user = User.objects(id=id).first()
    if (current_user != user):
        abort(403)
    logout_user()
    posts = Post.objects(created_by=id)
    comments = Comment.objects(created_by=user.id)
    for comment in comments:
        comments_ref = Post.objects(comments=comment)
        subcomments_ref = Comment.objects(comments=comment)
        if comments_ref is not None:
            comments_ref.update(pull__comments=comment)
        if subcomments_ref is not None:
            subcomments_ref.update(pull__comments=comment.id)
        comment.delete()
    posts.delete()
    user.delete()
    flash('Sorry to see you go! Your account has now been deleted.', 'yellow black-text')
    return redirect("/")
