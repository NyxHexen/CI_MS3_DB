from flask import render_template,Blueprint, redirect, flash, jsonify, request
from flask_login import login_required, current_user
from devbus.utils.models import Post, User, DoesNotExist

main = Blueprint("main", "__name__")

@main.route("/")
def home():
    try:
        page_num = int(request.args.get('page'))
    except:
        page_num = 1
    posts = Post.objects.paginate(
        page=page_num, 
        per_page=2)
    return render_template("home.html", posts=posts, page_num=(1 if page_num is None else page_num))

@main.route("/user/<username>")
@login_required
def view_user(username):
    try: 
        user = User.objects.get(username=username)
        posts = Post.objects(created_by=user.id) if user is not None else None
        return render_template("view_user.html", user=user, posts=posts)
    except DoesNotExist:
        flash("User you are looking for does not exist or has been deactivated", "red")
    return redirect("/")


@main.route("/search", methods=["GET", "POST"])
@main.route("/search/<filter>", methods=["GET", "POST"])
@main.route("/search/<filter>/<arg>", methods=["GET", "POST"])
@login_required
def search_results(arg="", filter=""):
    try:
        page_num = int(request.args.get('page'))
    except:
        page_num = 1
    if (arg == ""):
        arg = request.form.get('search_field')
        filter = request.form.get('filter_select')
    match filter:
        case "user":
            users = User.objects(username__icontains=arg)
            posts = Post.objects(created_by__in=users).paginate(page=page_num, per_page=2)
        case "lang":
            users = User.objects(languages__icontains=arg)
            posts = Post.objects(code_language__icontains=arg).paginate(page=page_num, per_page=2)
        case _:
            users = ""
            posts = Post.objects().paginate(page=page_num, per_page=2)
    return render_template("search_results.html", posts=posts, users=users, page_num=page_num)


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