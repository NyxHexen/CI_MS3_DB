from datetime import datetime
from flask_login import UserMixin
from mongoengine import *
from devbus import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(id=user_id)

class User(Document, UserMixin):
    meta = {'collection': 'users'}
    user_type = StringField(default='user')
    f_name = StringField(max_length=16)
    l_name = StringField(max_length=16)
    username = StringField(min_length=6, max_length=16, unique=True)
    email = StringField(unique=True)
    password = StringField()
    profile_image = StringField(default="")
    bio = StringField(max_length=126, default="")
    languages = ListField(default=[])

class Post(Document):
    meta = {'collection': 'posts'}
    post_title = StringField(max_length=86)
    post_content = StringField()
    code_content = StringField()
    code_language = StringField()
    created_date = DateField(default=datetime.utcnow)
    created_by = StringField()
    replies = ListField()
    votes = DictField()
    post_type = StringField()