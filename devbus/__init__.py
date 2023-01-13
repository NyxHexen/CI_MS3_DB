import os
from flask import Flask
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_bcrypt import Bcrypt
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_compress import Compress
if os.path.exists("env.py"):
    import env

# App Setup
app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = [{
    'host': os.environ.get("MONGO_URI"),
    'alias': 'default'
}]
app.config['FLASK_ADMIN_SWATCH'] = 'lumen'
app.secret_key = os.environ.get("SECRET_KEY")
db = MongoEngine(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.signin'
Compress(app)

from devbus.auth.routes import auth
from devbus.main.routes import main
from devbus.posts.routes import posts
from devbus.errors.handlers import errors
from devbus.admin.views import UserView, PostView, CommentView, MyHomeView
from devbus.utils.models import User, Post, Comment

# Flask Blueprint Registration
app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(posts)
app.register_blueprint(errors)

# Admin Views Registration
admin_page = Admin(app, name='DEVBUS', template_mode='bootstrap4',
                   index_view=(MyHomeView(
                    menu_class_name="btn btn-primary btn-sm ml-1")))
admin_page.add_view((UserView(User,
                    name='Users',
                    menu_class_name="btn btn-primary btn-sm ml-1")))
admin_page.add_view((PostView(Post,
                    name='Posts',
                    menu_class_name="btn btn-primary btn-sm ml-1")))
admin_page.add_view((CommentView(Comment,
                    name='Comments',
                    menu_class_name="btn btn-primary btn-sm ml-1")))
admin_page.add_link((MenuLink(
                    name="Log Out",
                    url='/logout',
                    class_name="btn btn-outline-warning btn-sm mr-3")))
admin_page.add_link((MenuLink(
                    name="Back to DB",
                    url='/',
                    class_name="btn btn-outline-primary btn-sm")))
