from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, Email

class StudentForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=2, max=50)])
    major = StringField('Major', validators=[InputRequired(), Length(min=2, max=50)])

class CourseForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=2, max=50)])
    credits = IntegerField('Credits', validators=[InputRequired()])
    professor = SelectField('Professor', coerce=int, validators=[InputRequired()])
