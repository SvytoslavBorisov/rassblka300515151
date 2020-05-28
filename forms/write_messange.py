from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, RadioField
from wtforms.validators import DataRequired, Optional


class SendMessage(FlaskForm):
    text = TextAreaField('Текст письма', validators=[DataRequired()], default='')
    type = RadioField('Тип', choices=[('text', 'Текст'), ('html', 'Html')])
    submit = SubmitField('Отправить')
