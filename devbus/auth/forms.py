from PIL import Image
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import (StringField, PasswordField, SubmitField,
                     BooleanField, ValidationError, Field, TextAreaField)
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.widgets import TextArea
from devbus.utils.models import User
from devbus.auth.utils import password_check


class SignUpForm(FlaskForm):
    f_name = StringField('First Name (Optional)',
                         validators=[Length(max=16)])
    l_name = StringField('Last Name (Optional)',
                         validators=[Length(max=16)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=6, max=16)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=8, max=32)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 Length(max=32),
                                                 EqualTo('password')])
    submit = SubmitField('READY!')

    def validate_username(self, username):
        is_unique_username = len(User.objects(username=username.data)) == 0
        if not is_unique_username:
            raise ValidationError('Username is taken. Please pick another.')

    def validate_email(self, email):
        is_unique_email = len(User.objects(email=email.data)) == 0
        if not is_unique_email:
            raise ValidationError('Email is taken. Please use another.')

    def validate_password(self, password):
        is_strong_password = True if password_check(password.data) else False
        if not is_strong_password:
            raise ValidationError('''Password should contain an uppercase
            letter, a lowercase letter, a number, and a symbol.''')


class SignInForm(FlaskForm):
    email = StringField('Email Address',
                        validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(max=32)])
    remember = BooleanField('Stay signed in')
    submit = SubmitField('Log In')


class TagListField(Field):
    """
    Custom form field, new line separated tags, stores input as a list
    for storage in DB.
    """
    widget = TextArea()

    def _value(self):
        if self.data:
            return '\r\n'.join(self.data)
        else:
            return ''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split('\r\n')]
        else:
            self.data = []


class UpdateProfileForm(FlaskForm):
    f_name = StringField('First Name',
                         validators=[Length(max=16)])
    l_name = StringField('Last Name',
                         validators=[Length(max=16)])
    username = StringField('Username',
                           validators=[Length(min=6, max=16)])
    email = StringField('Email',
                        validators=[Email()])
    bio = TextAreaField('Bio', validators=[Length(max=120)])
    languages = TagListField('My Superpowers')
    profile_image = FileField('Update Profile Picture',
                              validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save Changes')

    def validate_username(self, username):
        if username.data != current_user.username:
            is_unique_username = len(User.objects(username=username.data)) == 0
            if not is_unique_username:
                raise ValidationError('''Username is taken.
                                      Please pick another.''')

    def validate_email(self, email):
        if email.data != current_user.email:
            is_unique_email = len(User.objects(email=email.data)) == 0
            if not is_unique_email:
                raise ValidationError('Email is taken. Please use another.')

    def validate_profile_image(self, profile_image):
        if profile_image.data:
            image = Image.open(profile_image.data)
            image_w, image_h = image.size
            if image_w < 350 or image_h < 350:
                raise ValidationError('Image must be 350px by 350px at least.')


class ForgotPwdForm(FlaskForm):
    email = StringField('Email',
                        validators=[Email()])
    submit = SubmitField('Reset')


class NewPwdForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=8, max=32)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 Length(max=32),
                                                 EqualTo('password')])
    submit = SubmitField('Update Password')

    def validate_password(self, password):
        is_strong_password = True if password_check(password.data) else False
        if not is_strong_password:
            raise ValidationError('''Password should contain an uppercase
                                     letter, a lowercase letter,
                                     a number, and a symbol.''')


class ChangePwdForm(FlaskForm):
    old_password = PasswordField('Old Password',
                                 validators=[DataRequired(),
                                             Length(min=8, max=32)])
    new_password = PasswordField('New Password',
                                 validators=[DataRequired(),
                                             Length(min=8, max=32)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 Length(max=32),
                                                 EqualTo('password')])
    submit = SubmitField('Update Password')

    def validate_password(self, password):
        is_strong_password = True if password_check(password.data) else False
        if not is_strong_password:
            raise ValidationError('''Password should contain an
                                    uppercase letter, a lowercase letter,
                                    a number, and a symbol.''')


class DeleteAccountForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired()])
    submit = SubmitField('Yes')
