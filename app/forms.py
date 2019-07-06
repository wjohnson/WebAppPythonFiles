from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, IntegerField, SelectField,TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional
from flask_wtf.file import FileField, FileAllowed, FileRequired


class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])
    submit = SubmitField('Search')
