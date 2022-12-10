from flask import Blueprint, render_template, redirect, request, jsonify, flash
from flask_login import login_required, current_user
from devbus.utils.models import Post, Comment, Subcomment
from devbus.posts.forms import NewPostForm, NewCommentForm, NewSubCommentForm


posts = Blueprint("posts", "__name__")


@posts.route("/posts/<id>", methods=["GET", "POST"])
@login_required
def view_post(id):
    post = Post.objects.get(id=id)
    return render_template("view_post.html", post=post)


@posts.route("/posts/<id>/edit_post", methods=["GET", "POST"])
@login_required
def edit_post(id):
    post = Post.objects.get(id=id)
    form = NewPostForm()
    if form.validate_on_submit():
        form.populate_obj(post)
        post.created_by = current_user.id
        post.save()
        return redirect(f"/posts/{post.id}")
    elif request.method == "GET":
        form.post_title.data = post.post_title
        form.post_content.data = post.post_content
        form.code_language.data = post.code_language
        form.code_content.data = post.code_content
        form.post_type.data = post.post_type
    return render_template("edit_post.html", form=form, post=post)


@posts.route("/posts/<post_id>/<comment_id>", methods=["GET", "POST"])
@login_required
def view_comment(post_id, comment_id):
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id)
    return render_template("view_comment.html", post=post, comment=comment)


@posts.route("/posts/<id>/reply", methods=["GET", "POST"])
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
        return redirect(f"/posts/{id}")
    return render_template("view_post.html", post=post, form=form)


@posts.route("/posts/<post_id>/<comment_id>/edit_reply", methods=["GET", "POST"])
@login_required
def edit_comment(post_id, comment_id):
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id)
    form = NewCommentForm()
    if form.validate_on_submit():
        form.populate_obj(comment)
        comment.save()
        return redirect(f"/posts/{post_id}")
    elif request.method == "GET":
        form.comment_content.data = comment.comment_content
        form.code_language.data = comment.code_language
        form.code_content.data = comment.code_content
    return render_template("edit_comment.html", post=post, comment=comment, form=form)


@posts.route("/posts/<post_id>/<comment_id>/reply", methods=["GET", "POST"])
@login_required
def new_subcomment(post_id, comment_id):
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id)
    sub_form = NewSubCommentForm()
    if sub_form.validate_on_submit():
        sub_comment = Subcomment(created_by=current_user.id)
        sub_form.populate_obj(sub_comment)
        comment.comments.append(sub_comment)
        sub_comment.save()
        comment.save()
        return redirect(f"/posts/{post_id}/{comment_id}")
    return render_template(
        "view_comment.html", post=post, comment=comment, sub_form=sub_form
    )


@posts.route("/posts/<post_id>/<comment_id>/<subcomment_id>/edit_subreply", methods=["GET", "POST"])
@login_required
def edit_subcomment(post_id, comment_id, subcomment_id):
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id)
    subcomment = Comment.objects.get(id=subcomment_id)
    form = NewSubCommentForm()
    if form.validate_on_submit():
        form.populate_obj(subcomment)
        subcomment.save()
        return redirect(f"/posts/{post_id}/{comment_id}")
    elif request.method == "GET":
        form.comment_content.data = subcomment.comment_content
    return render_template(
        "edit_subcomment.html",
        post=post,
        comment=comment,
        subcomment=subcomment,
        form=form,
    )


@posts.route("/new_post", methods=["GET", "POST"])
@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post()
        form.populate_obj(post)
        post.created_by = current_user.id
        post.save()
        return redirect(f"/posts/{post.id}")
    return render_template("new_post.html", form=form)


@posts.route("/_update_votes/<id>/<vote>", methods=["GET", "POST"])
def update_votes(id, vote):
    if current_user.is_authenticated is False:
        flash("You must be signed in to do that!", "red")
        return jsonify(False)
    post_set = Post.objects(id=id).first()
    comment_set = Comment.objects(id=id).first()
    content = post_set if post_set is not None else comment_set
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
    return jsonify(
        length_up=len(content.votes["up"]), length_down=len(content.votes["down"])
    )


@posts.route("/posts/<id>/delete")
@login_required
def delete_post(id):
    post = Post.objects.get(id=id)
    post.delete()
    flash("Your post has been deleted!", "green")
    return redirect("/")


@posts.route("/<comment_id>/delete_comment")
@login_required
def delete_comment(comment_id):
    post = Post.objects.get(comments=comment_id)
    comment = Comment.objects.get(id=comment_id)
    for subcomment in comment.comments:
        subcomment.delete()
    post.update(pull__comments=comment)
    comment.delete()
    flash("Your comment has been deleted!", "green")
    return redirect("/")
