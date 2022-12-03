from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from devbus.utils.models import Post, Comment
from devbus.posts.forms import NewPostForm, NewCommentForm


posts = Blueprint('posts', '__name__')


@posts.route("/post/<id>", methods=["GET", "POST"])
@login_required
def view_post(id):
    post = Post.objects.get(id=id)
    form = NewCommentForm()
    if form.validate_on_submit():
        comment = Comment(created_by=current_user.id)
        form.populate_obj(comment)
        comment.save()
        post.comments.append(comment)
        post.save()
        return redirect(f"/post/{id}")
    return render_template("view_post.html", post=post, form=form)


@posts.route("/new_post", methods=["GET", "POST"])
@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post()
        form.populate_obj(post)
        post.created_by = current_user.id
        post.save()
        return redirect(f"/post/{post.id}")
    return render_template("new_post.html", form=form)