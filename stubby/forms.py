from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from stubby.models import User, Post


class AddClass(FlaskForm):
    course = StringField('Course or CRN', validators=[DataRequired()])
    submit = SubmitField('Add Class')
