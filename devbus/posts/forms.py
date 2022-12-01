from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import (StringField, SubmitField, 
                    TextAreaField, RadioField)
from wtforms.validators import DataRequired, Length


class NewPostForm(FlaskForm):
    post_title = StringField('Post Title',
                                    validators=[DataRequired()])
    post_content = StringField('Post Content', 
                                    validators=[DataRequired()])
    code_content = TextAreaField('Code Content', 
                                    validators=[])
    code_language = StringField('Code Language')
    post_type = RadioField("Post Type", choices=["post", "assist"],default="post")
    submit = SubmitField('POST')