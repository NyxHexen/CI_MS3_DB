from flask import render_template,Blueprint, redirect, flash
from devbus.utils.models import Post, User, DoesNotExist

main = Blueprint("main", "__name__")

@main.route("/")
def home():
    posts = Post.objects()
    return render_template("home.html",posts=posts)

@main.route("/user/<username>")
def view_user(username):
    try: 
        user = User.objects.get(username=username)
        posts = Post.objects(created_by=user.id) if user is not None else None
        return render_template("view_user.html", user=user, posts=posts)
    except DoesNotExist:
        flash("User you are looking for does not exist or has been deactivated", "red")
    return redirect("/")