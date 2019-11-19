from flask_wtf import Form
from wtforms import StringField, BooleanField,  TextAreaField, SelectMultipleField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .models import Task


class TaskForm(Form):
    name = StringField('name', validators=[DataRequired()])
    year = DateField('year', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])


class STaskForm(Form):
    year = DateField('year', validators=[DataRequired()])
