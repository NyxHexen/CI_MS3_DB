from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField


class SearchFieldForm(FlaskForm):
    search = StringField('Looking for something?')
    filter = SelectField('Filter By', choices=[('username', 'username'),
                                               ('language', 'language')])
    submit = SubmitField('<i class="material-icons">search</i>')
