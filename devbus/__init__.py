import os
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
if os.path.exists("env.py"):
    import env


app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

from devbus import routes