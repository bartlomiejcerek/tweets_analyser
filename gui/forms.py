# -*- coding: utf-8 -*-
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, DecimalField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class ManualForm(FlaskForm):
    content = StringField('Tweet Content', validators=[DataRequired()], widget=TextArea())
    likes = DecimalField('Likes', validators=[DataRequired()])
    shares = DecimalField('Shares', validators=[DataRequired()])
    datetime = DateTimeField('Date and Time', validators=[DataRequired()], 
                             format='%d/%m/%Y %H:%M', default = datetime.datetime.utcnow)
    submit = SubmitField('Check Tweet')