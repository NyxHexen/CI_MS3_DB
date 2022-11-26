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
    profile_image = StringField(default="https://ci-ms3-devbus.s3.eu-west-1.amazonaws.com/default.jpg")
    bio = StringField(max_length=126, default="")
    languages = ListField(default=[])


class Post(Document):
    meta = {'collection': 'posts'}
    post_title = StringField(max_length=86)
    post_content = StringField()
    code_content = StringField()
    code_language = StringField()
    replies = ListField()
    votes = DictField() # { 'yes': ListField(), 'no': ListField() }
    post_type = StringField()
    created_by = StringField()
    created_date = DateField(default=datetime.utcnow)


class Comment(Document):
    meta = {'collection': 'comments'}
    content_id = ObjectIdField()
    comment_content = StringField(required=True)
    code_language = StringField()
    code_content = StringField()
    replies = ListField()
    votes = DictField()
    created_by = StringField()
    created_date = DateField(default=datetime.utcnow)
    is_verified = BooleanField()
