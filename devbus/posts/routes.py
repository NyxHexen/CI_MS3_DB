from flask import Blueprint, render_template, redirect, request, jsonify, flash
from flask_login import login_required, current_user
from devbus.utils.models import Post, Comment
from devbus.posts.forms import NewPostForm, NewCommentForm


posts = Blueprint('posts', '__name__')


@posts.route("/post/<id>", methods=["GET", "POST"])
@login_required
def view_post(id):
    post = Post.objects.get(id=id)
    return render_template("view_post.html", post=post)


@posts.route("/post/<id>/new_comment", methods=["GET", "POST"])
@login_required
def new_comment(id):
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


@posts.route("/_update_votes/<id>/<vote>", methods=["GET", "POST"])
def update_votes(id, vote):
    if current_user.is_authenticated is False:
        flash("You must be signed in to do that!", "red")
        return jsonify(False)
    content = Post.objects(id=id).first()
    if current_user in content.votes["up"] and vote == "up":
        # If the user has upvoted before, and is pressing upvote btn again
        content.votes["up"].remove(current_user)
    elif current_user in content.votes["up"] and vote == "down":
        # If the user has upvoted before, and is pressing downvote btn
        content.votes["up"].remove(current_user)
        content.votes["down"].append(current_user)
    elif current_user in content.votes["down"] and vote == "up":
        # If the user has downvoted before, and is pressing upvote btn
        content.votes["down"].remove(current_user)
        content.votes["up"].append(current_user)
    elif current_user in content.votes["down"] and vote == "down":
        # If the user has downvoted before, and is pressing downvote btn again
        content.votes["down"].remove(current_user)
    else:
        # If the user has never voted before
        content.votes[vote].append(current_user)
    content.save()
    return jsonify(length_up = len(content.votes["up"]), length_down = len(content.votes["down"]))