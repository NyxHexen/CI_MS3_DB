from flask import Blueprint, render_template
from devbus.utils.models import Post, Comment, User


posts = Blueprint('posts', '__name__')


@posts.route("/post/<id>")
def view_post(id):
    post = Post.objects.get(id=id)
    return render_template("view_post.html", post=post)
