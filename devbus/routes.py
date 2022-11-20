from flask import (
    flash, render_template,
    redirect, request, session, url_for)
from devbus.forms import RegistrationForm, LoginForm
from devbus import mongo, app

@app.route("/")
def home():
    posts = mongo.db.posts.find()
    return render_template("home.html",posts=posts)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = {"user_type": "user",
                "username": form.username.data,
                "password": form.password.data,
                "f_name": form.f_name.data,
                "l_name": form.l_name.data,
                "email": form.email.data,
                "bio": "",
                "languages": []
                }
        mongo.db.users.insert_one(user)
        flash("Account created successfully!", "light-green black-text lighten-2")
        return redirect(url_for('signin'))
    return render_template("signup.html", title="Sign Up", form=form)

@app.route("/signin", methods=["GET", "POST"])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        if form.id.data == 'admin@devbus.com' and form.password.data == 'password':
            flash("You have been logged in!", 'light-blue lighten-2')
            return redirect(url_for('home'))
        else: 
            flash('Login Unsuccessful. Please check your username (or email) and password.', 'materialize-red lighten-1')
    return render_template("signin.html", title="License and Registration", form=form)

