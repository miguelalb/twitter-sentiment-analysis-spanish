
from flask_wtf import FlaskForm
from wtforms.fields.html5 import IntegerRangeField
from wtforms import SubmitField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, NumberRange 


class TweetsForm(FlaskForm):
    screen_name = SelectMultipleField('Candidato',choices=[],validators=[DataRequired()])
    cant_tweets = IntegerRangeField(validators=[NumberRange(min=20, max=100)])
    submit1 = SubmitField('Tweets')


class MentionsForm(FlaskForm):
    terminos = SelectMultipleField('Termino',choices=[],validators=[DataRequired()])
    cant_mentions = IntegerRangeField(validators=[NumberRange(min=20, max=100)])
    submit2 = SubmitField('Mentions')