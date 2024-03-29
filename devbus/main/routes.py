from flask import render_template, Blueprint, redirect, flash, jsonify, request
from flask_login import login_required
from devbus.utils.models import Post, User, DoesNotExist

main = Blueprint("main", "__name__")


@main.route("/")
def home():
    """
    This function renders the home page and provides
    a list of all posts in chronological order.
    """
    try:
        page_num = int(request.args.get('page'))
    except TypeError:
        page_num = 1
    posts = Post.objects().order_by('-created_date').paginate(
        page=page_num,
        per_page=10)
    return render_template("main/home.html",
                           posts=posts,
                           page_num=page_num)


@main.route("/user/<username>")
@login_required
def view_user(username):
    try:
        try:
            page_num = int(request.args.get('page'))
        except TypeError:
            page_num = 1
        user = User.objects.get(username=username)
        posts = (Post.objects(created_by=user.id)
                 .paginate(page=page_num, per_page=10)
                 if user is not None else None)
        return render_template("main/view_user.html",
                               title=username, user=user, posts=posts)
    except DoesNotExist:
        flash('''User you are looking for does not exist or
         has been deactivated''', "red")
    return redirect("/")


@main.route("/search", methods=["GET", "POST"])
@main.route("/search/<filter>", methods=["GET", "POST"])
@main.route("/search/<filter>/<arg>", methods=["GET", "POST"])
@login_required
def search_results(arg="", filter=""):
    try:
        page_num = int(request.args.get('page'))
    except TypeError:
        page_num = 1
    if (arg == ""):
        arg = request.form.get('search_field')
        filter = request.form.get('filter_select')
    match filter:
        case "user":
            users = User.objects(username__icontains=arg)
            posts = (Post.objects(created_by__in=users)
                     .paginate(page=page_num, per_page=10))
        case "lang":
            users = User.objects(languages__icontains=arg)
            posts = (Post.objects(code_language__icontains=arg)
                     .paginate(page=page_num, per_page=10))
        case _:
            users = (User.objects() if arg == ""
                     else User.objects(username__icontains=arg))
            posts = Post.objects().paginate(page=page_num, per_page=10)
    return render_template("main/search_results.html",
                           title="Search Results", posts=posts,
                           users=users, page_num=page_num)


@main.route("/_search/<filter>/<arg>", methods=["GET", "POST"])
@login_required
def search(arg=None, filter="user"):
    match filter:
        case "user":
            items = User.objects(username__icontains=arg)
        case "lang":
            items = Post.objects(code_language__icontains=arg)
        case _:
            return jsonify(False)
    return jsonify(items=items)
