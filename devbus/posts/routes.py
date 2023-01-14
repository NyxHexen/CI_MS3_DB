from flask import (Blueprint, render_template, redirect,
                   request, jsonify, flash, abort)
from flask_login import login_required, current_user
from devbus.utils.models import Post, Comment, Subcomment
from devbus.posts.forms import NewPostForm, NewCommentForm, NewSubCommentForm


posts = Blueprint("posts", "__name__")


@posts.route("/posts/<id>", methods=["GET", "POST"])
@login_required
def view_post(id):
    """
    Returns the post on which the user has clicked
    into single view, loading all comments.
    """
    try:
        page_num = int(request.args.get('page'))
    except TypeError:
        page_num = 1
    post = Post.objects.get_or_404(id=id)
    comments = Post.objects.paginate_field('comments',
                                           page=page_num,
                                           per_page=10,
                                           doc_id=id)
    return render_template("posts/view_post.html", title="View Post",
                           post=post, comments=comments, page_num=page_num)


@posts.route("/posts/<id>/edit_post", methods=["GET", "POST"])
@login_required
def edit_post(id):
    """
    Allows the user to edit their own posts, once
    saved redirects back to view_post view.
    """
    post = Post.objects.get(id=id)
    if post.created_by != current_user:
        abort(403)
    form = NewPostForm()
    if form.validate_on_submit():
        form.populate_obj(post)
        post.created_by = current_user.id
        post.save()
        flash("Your post has been edited!", 'message')
        return redirect(f"/posts/{post.id}")
    elif request.method == "GET":
        form.post_title.data = post.post_title
        form.post_content.data = post.post_content
        form.code_language.data = post.code_language
        form.code_content.data = post.code_content
        form.post_type.data = post.post_type
    return render_template("posts/edit_post.html", title="Edit Post",
                           form=form, post=post)


@posts.route("/posts/<post_id>/<comment_id>", methods=["GET", "POST"])
@login_required
def view_comment(post_id, comment_id):
    """
    Returns the comment, and the post it belongs to,
    on which the user has clicked into single view,
    loading all subcomments.
    """
    try:
        page_num = int(request.args.get('page'))
    except TypeError:
        page_num = 1
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id)
    subcomments = Comment.objects.paginate_field('comments',
                                                 page=page_num,
                                                 per_page=10,
                                                 doc_id=comment_id)
    return render_template("posts/view_comment.html", title="View Comment",
                           post=post, comment=comment,
                           subcomments=subcomments,
                           page_num=page_num)


@posts.route("/posts/<id>/reply", methods=["GET", "POST"])
@login_required
def new_comment(id):
    """
    Renders same template as view_post, but with
    an additional form variable, created with WTForms.
    """
    try:
        page_num = int(request.args.get('page'))
    except TypeError:
        page_num = 1
    post = Post.objects.get(id=id)
    form = NewCommentForm()
    comments = Post.objects.paginate_field('comments',
                                           page=page_num,
                                           per_page=10,
                                           doc_id=id)
    if form.validate_on_submit():
        comment = Comment(created_by=current_user.id)
        form.populate_obj(comment)
        comment.save()
        post.comments.append(comment)
        post.save()
        flash("Your comment has been posted!", 'message')
        return redirect(f"/posts/{id}")
    return render_template("posts/view_post.html", title="New Comment",
                           post=post,
                           form=form,
                           comments=comments,
                           page_num=page_num)


@posts.route("/posts/<post_id>/<comment_id>/edit_reply", methods=["GET",
                                                                  "POST"])
@login_required
def edit_comment(post_id, comment_id):
    """
    Allows the user to edit their own comment, once
    saved redirects back to the post.
    """
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id)
    if comment.created_by != current_user:
        abort(403)
    form = NewCommentForm()
    if form.validate_on_submit():
        form.populate_obj(comment)
        comment.save()
        flash("Your comment has been edited!", 'message')
        return redirect(f"/posts/{post_id}")
    elif request.method == "GET":
        form.comment_content.data = comment.comment_content
        form.code_language.data = comment.code_language
        form.code_content.data = comment.code_content
    return render_template("posts/edit_comment.html", title="Edit Comment",
                           post=post,
                           comment=comment,
                           form=form)


@posts.route("/posts/<post_id>/<comment_id>/reply", methods=["GET", "POST"])
@login_required
def new_subcomment(post_id, comment_id):
    """
    Similar to view comment, but instead passes an additional
    form variable, containing a form created with WTForms.
    On submit redirects to post page.
    """
    try:
        page_num = int(request.args.get('page'))
    except TypeError:
        page_num = 1
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id)
    subcomments = Comment.objects.paginate_field('comments',
                                                 page=page_num,
                                                 per_page=10,
                                                 doc_id=comment_id)
    sub_form = NewSubCommentForm()
    if sub_form.validate_on_submit():
        sub_comment = Subcomment(created_by=current_user.id)
        sub_form.populate_obj(sub_comment)
        comment.comments.append(sub_comment)
        sub_comment.save()
        comment.save()
        flash("Your comment has been posted!", 'message')
        return redirect(f"/posts/{post_id}/{comment_id}")
    return render_template("posts/view_comment.html", title="New Subcomment",
                           post=post,
                           comment=comment,
                           sub_form=sub_form,
                           subcomments=subcomments,
                           page_num=page_num)


@posts.route("/posts/<post_id>/<comment_id>/<subcomment_id>/edit_subreply",
             methods=["GET", "POST"])
@login_required
def edit_subcomment(post_id, comment_id, subcomment_id):
    """
    Renders a WTForm, similar to add_subcomment, which
    allows the user to edit their subcomment. On successful
    submission, redirects back to view comment page.
    """
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id)
    subcomment = Comment.objects.get(id=subcomment_id)
    if subcomment.created_by != current_user:
        abort(403)
    form = NewSubCommentForm()
    if form.validate_on_submit():
        form.populate_obj(subcomment)
        subcomment.save()
        flash("Your comment has been edited!", 'message')
        return redirect(f"/posts/{post_id}/{comment_id}")
    elif request.method == "GET":
        form.comment_content.data = subcomment.comment_content
    return render_template(
        "posts/edit_subcomment.html",
        title="Edit Subcomment",
        post=post,
        comment=comment,
        subcomment=subcomment,
        form=form,
    )


@posts.route("/new_post", methods=["GET", "POST"])
@login_required
def new_post():
    """
    Providers a form, created with WTForms, which allows the
    user to create a new post.
    """
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post()
        form.populate_obj(post)
        post.created_by = current_user.id
        post.save()
        flash("Your post has been created!", 'message')
        return redirect(f"/posts/{post.id}")
    return render_template("posts/new_post.html", title="New Post", form=form)


@posts.route("/_update_votes/<id>/<vote>", methods=["GET", "POST"])
def update_votes(id, vote):
    """
    Function does not render/use a template at all; this is the back-end
    logic of the post and comments vote buttons. Depending on the button
    pressed updates the database and then sends a JSON response to the AJAX
    in the front end to update visually.
    """
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
        length_up=len(content.votes["up"]),
        length_down=len(content.votes["down"])
    )


@posts.route("/posts/<id>/delete")
@login_required
def delete_post(id):
    """
    Allows the user to delete their post
    This function does not render a template,
    instead if actions the delete_post request and
    redirects back to home page.
    """
    post = Post.objects.get(id=id)
    post.delete()
    flash("Your post has been deleted!", "green")
    return redirect("/")


@posts.route("/<comment_id>/delete_comment")
@login_required
def delete_comment(comment_id):
    """
    Allows user to delete their own comment, which
    also deletes any subcomments.
    Does not render a template, instead actions the request
    and then redirects back to the post page.
    """
    post = Post.objects.get(comments=comment_id)
    comment = Comment.objects.get(id=comment_id)
    for subcomment in comment.comments:
        subcomment.delete()
    post.update(pull__comments=comment)
    comment.delete()
    flash("Your comment has been deleted!", "green")
    return redirect(f"/posts/{post.id}")


@posts.route("/<comment_id>/<subcomment_id>/delete_subcomment")
@login_required
def delete_subcomment(comment_id, subcomment_id):
    """
    Allows user to delete their own subcomment.
    Does not render a template, instead actions the request
    and then redirects back to the post page.
    """
    comment = Comment.objects.get(id=comment_id)
    post = Post.objects.get(comments__icontains=comment.id)
    subcomment = Comment.objects.get(id=subcomment_id)
    comment.update(pull__comments=subcomment.id)
    subcomment.delete()
    flash("Your comment has been deleted!", "green")
    return redirect(f"/posts/{post.id}")
