import os
import dns
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import RegistrationForm, LoginForm
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def home():
    posts = mongo.db.posts.find()
    return render_template("home.html",posts=posts)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Account created successfully!", "light-green lighten-2")
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


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True) # REMOVE BEFORE DEPLOYMENT AND SUBMISSION