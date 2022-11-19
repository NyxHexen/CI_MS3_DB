from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

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

class LoginForm(FlaskForm):                  
    id = StringField('Username or Email Address', 
                            validators=[DataRequired()])
    password = PasswordField('Password',
                            validators=[DataRequired(), Length(max=32)])
    remember = BooleanField('Stay signed in')
    submit = SubmitField('Log In')