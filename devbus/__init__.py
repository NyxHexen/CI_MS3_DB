import os
from bson.objectid import ObjectId
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
if os.path.exists("env.py"):
    import env


app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = [{
    'host': os.environ.get("MONGO_URI"),
    'alias': 'default'
}]
app.secret_key = os.environ.get("SECRET_KEY")
db = MongoEngine(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.signin'

from devbus.auth.routes import auth
from devbus.main.routes import main
from devbus.posts.routes import posts

app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(posts)