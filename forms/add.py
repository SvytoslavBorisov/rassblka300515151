from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, RadioField
from wtforms.validators import DataRequired, Optional


class AddEmail(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], default='')
    submit = SubmitField('Добавить')
