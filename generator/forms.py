"""Forms to securely accept equation parameters."""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, HiddenField
from wtforms.validators import InputRequired, ValidationError


# Custom validators
def validate_int(form, field):
    if type(field.data) != 'int':
        raise ValidationError('Min and max must be integers')

def validate_max_gte_min(form, field):
    if field.data < form.minimum.data:
        raise ValidationError('Max must be greater than or equal to min')


# Forms
class EquationForm(FlaskForm):
    equation = StringField("Equation: ", validators=[InputRequired()])
    submit = SubmitField("Proceed")

class VariableForm(FlaskForm):
    variable = HiddenField(validators=[InputRequired()])
    minimum = IntegerField("Min", validators=[InputRequired(), validate_int])
    maximum = IntegerField("Max", validators=[InputRequired(), validate_int, validate_max_gte_min])
    zero_ok = BooleanField("Zero Ok", default="checked")

class EquationParametersForm(FlaskForm):
    positive_only = BooleanField("Positive Answers Only", default=False)
    topic = StringField("Topic: ", validators=[InputRequired()])
    instructions = StringField("Instructions: ", validators=[InputRequired()])
    categories = StringField("Categories: ", validators=[InputRequired()])
