import os
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
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

from devbus import routes