from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class UserForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    name=StringField('Full Name',validators=[DataRequired()])
    phone=StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    location=StringField('Location (City, Country)', validators=[DataRequired()])
    personalurl=StringField('Personal/Social URL',validators=[DataRequired()]),
    bio=TextAreaField('Bio', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Submit')