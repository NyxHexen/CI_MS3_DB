import re
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, PasswordField, SubmitField, 
                    BooleanField, ValidationError, Field, TextAreaField)
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.widgets import TextArea
from devbus.routes import current_user
from devbus.models import User


def password_check(password):
    """
    https://stackoverflow.com/questions/16709638/checking-the-strength-of-a-password-how-to-check-conditions#32542964
    Verify the strength of 'password' and return boolean.
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

    # overall result
    password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )

    return password_ok


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
                            validators=[DataRequired(), Length(min=8, max=32)])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), Length(max=32), EqualTo('password')])
    user_image = FileField()
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
            raise ValidationError('Password should contain an uppercase letter, a lowercase letter, a number, and a symbol.')

        
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
        if current_user:
            self.data = current_user.languages
        elif valuelist:
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
    update_image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save Changes', id="update_submit", name="update_submit")

    def validate_username(self, username):
        if username.data != current_user.username:
            is_unique_username = len(User.objects(username=username.data)) == 0
            if not is_unique_username:
                raise ValidationError('Username is taken. Please pick another.')

    def validate_email(self, email):
        if email.data != current_user.email:
            is_unique_email = len(User.objects(email=email.data)) == 0
            if not is_unique_email:
                raise ValidationError('Email is taken. Please use another.')
     
        
class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password',
                            validators=[DataRequired(), Length(min=8, max=32)])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), Length(max=32), EqualTo('password')])
    submit = SubmitField('Update')

    def validate_password(self, password):
        is_strong_password = True if password_check(password.data) else False
        if not is_strong_password:
            raise ValidationError('Password should contain an uppercase letter, a lowercase letter, a number, and a symbol.')