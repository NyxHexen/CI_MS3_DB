from flask import Blueprint, render_template
from flask_login import login_required
from devbus.utils.models import Post, Comment
from devbus.posts.forms import NewPostForm


posts = Blueprint('posts', '__name__')


@posts.route("/post/<id>")
@login_required
def view_post(id):
    post = Post.objects.get(id=id)
    return render_template("view_post.html", post=post)


@posts.route("/new_post")
@login_required
def new_post():
    form = NewPostForm()
    return render_template("new_post.html", form=form)