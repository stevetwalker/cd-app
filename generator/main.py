import os

from flask import Flask, render_template, request, redirect, url_for, session
import logging
import generator
import utilities
import database as db
from forms import EquationForm, VariableForm, EquationParametersForm

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY').encode()
app.config['SECRET_KEY'] = app.secret_key #Following instructions for WTForms

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    """Get equation parameters, then generate all viable problems."""
    equation_form, equation_params = EquationForm(), EquationParametersForm()
    variables, variable_forms = [], []

    if equation_form.validate_on_submit():
        equation = equation_form.equation.data
        print(equation)

        # Identify the vars in the equation and create a VariableForm for each
        variables = sorted(set([char for char in equation if char.isalpha()]))
        for var in variables:
            var = VariableForm()
            variable_forms.append(var)
        print(variables, variable_forms)

    return render_template('generator.jinja2',
                           equation_form=equation_form,
                           variable_forms=variable_forms,
                           variables=variables,
                           equation_params=equation_params,
                           error=None)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
