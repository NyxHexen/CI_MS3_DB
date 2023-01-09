from datetime import datetime
from flask_login import UserMixin
from mongoengine import *
from itsdangerous import URLSafeTimedSerializer
from devbus import login_manager, app


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

    def generate_pwd_token(self):
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'], 'reset_pwd')
        return s.dumps(str(self.id))
    
    @staticmethod
    def verify_pwd_token(token, max_age=1800):
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'], 'reset_pwd')
        return s.loads(token, max_age=max_age)


class Subcomment(Document):
    meta = {'collection': 'comments'}
    comment_content = StringField(required=True)
    votes = DictField(default={"up": [], "down": []})
    created_by = ReferenceField(User)
    created_date = DateField(default=datetime.utcnow)


class Comment(Document):
    meta = {'collection': 'comments'}
    comment_content = StringField(required=True)
    code_language = StringField()
    code_content = StringField()
    comments = ListField(ReferenceField(Subcomment))
    votes = DictField(default={"up": [], "down": []})
    created_by = ReferenceField(User)
    created_date = DateField(default=datetime.utcnow)


class Post(Document):
    meta = {'collection': 'posts'}
    post_title = StringField(max_length=86)
    post_content = StringField()
    code_content = StringField()
    code_language = StringField()
    comments = ListField(ReferenceField(Comment))
    votes = DictField(default={"up": [], "down": []})
    post_type = StringField()
    created_by = ReferenceField(User)
    created_date = DateField(default=datetime.utcnow)
