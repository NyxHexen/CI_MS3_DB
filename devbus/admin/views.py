from flask import abort, redirect, flash
from flask_admin import AdminIndexView, expose
from flask_login import current_user
from flask_admin.contrib.mongoengine import ModelView
from devbus.utils.models import StringField, User, Post, Comment

class CustomView(ModelView):
    """
    Custom view to help limit who can access
    each of the DB views.
    """
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.user_type == 'superuser'
        )

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users 
        when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                flash("You must login first to visit this page.", "red white-text")
                return redirect("/signin")


class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        if not (current_user.is_active and
                current_user.is_authenticated and
                current_user.user_type == 'superuser'):
            if current_user.is_authenticated:
                abort(403)
            else:
                flash("You must login first to visit this page.", "red white-text")
                return redirect("/signin")
        users = User.objects()
        posts = Post.objects()
        comments = Comment.objects(type='comment')
        subcomments = Comment.objects(type='subcomment')
        return self.render('admin/index.html', users=users, posts=posts, comments=comments, subcomments=subcomments)

class UserView(CustomView):
    page_size = 50
    form_overrides = {'languages': StringField}
    column_exclude_list = ['password']
    can_create = False
    edit_modal = True


class PostView(CustomView):
    page_size = 50  
    create_modal = True
    edit_modal = True


class CommentView(CustomView):
    page_size = 50
    can_create = False
    edit_modal = True