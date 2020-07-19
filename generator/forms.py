"""Forms to securely accept equation parameters."""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired

class EquationForm(FlaskForm):
    equation = StringField("Equation: ", validators=[DataRequired()])
    submit = SubmitField("Proceed")

class VariableForm(FlaskForm):
    minimum = IntegerField("Min", validators=[DataRequired()])
    maximum = IntegerField("Max", validators=[DataRequired()])
    zero_ok = BooleanField("Zero Ok", default=True)

class EquationParametersForm(FlaskForm):
    positive_only = BooleanField("Positive Answers Only", default=False)
