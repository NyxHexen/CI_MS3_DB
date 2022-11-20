import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from devbus import mongo

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

class RegistrationForm(FlaskForm):
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
    submit = SubmitField('READY!')#

    def validate_username(self, username):
        is_unique_username = mongo.db.users.find_one({'username': username.data}) is None
        if not is_unique_username:
            raise ValidationError('Username is taken. Please pick another.')

    def validate_email(self, email):
        is_unique_email = mongo.db.users.find_one({'email': email.data}) is None
        if not is_unique_email:
            raise ValidationError('Email is taken. Please use another.')

    def validate_password(self, password):
        is_strong_password = True if password_check(password.data) else False
        if not is_strong_password:
            raise ValidationError('Password should contain an uppercase letter, a lowercase letter, a number, and a symbol.')

class LoginForm(FlaskForm):                  
    id = StringField('Username or Email Address', 
                            validators=[DataRequired()])
    password = PasswordField('Password',
                            validators=[DataRequired(), Length(max=32)])
    remember = BooleanField('Stay signed in')
    submit = SubmitField('Log In')