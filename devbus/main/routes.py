from flask import render_template,Blueprint
from devbus.utils.models import Post

main = Blueprint("main", "__name__")

@main.route("/")
def home():
    posts = Post.objects()
    return render_template("home.html",posts=posts)