from flask import render_template,Blueprint
from devbus.utils.models import Post, User

main = Blueprint("main", "__name__")

@main.route("/")
def home():
    posts = Post.objects()
    return render_template("home.html",posts=posts)

@main.route("/<username>")
def view_user(username):
    user = User.objects.get(username=username)
    posts = Post.objects(created_by=user)
    return render_template("view_user.html", user=user, posts=posts)