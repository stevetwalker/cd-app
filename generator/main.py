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

    if request.method == 'POST':

        try:
            # If submitting valid equation data, get var data from equation
            if equation_form.validate_on_submit():
                equation, variables, variable_forms = \
                    generator.process_equation(equation_form, equation_params)
                return render_template('generator.jinja2',
                                       equation_form=equation_form,
                                       variable_forms=variable_forms,
                                       variables=variables,
                                       equation_params=equation_params)

            # If submitting variable and equation params, store them in equation_dict
            if equation_params.validate_on_submit():
                topic_id = generator.build_topic(request.form)

                return redirect(url_for('results', topic_id=topic_id))

        except Exception as err:
               print(err)

    return render_template('generator.jinja2', equation_form=equation_form)


@app.route('/results', methods=['GET', 'POST'])
def results():
    """Display generated problems."""
    topic_id = request.args.get('topic_id')
    topic_data = db.get_topic_from_id_in_url(topic_id)

    return render_template('results.jinja2',
                           topic=topic_data['topic'],
                           equation=topic_data['equation'],
                           instructions=topic_data['instructions'],
                           categories=topic_data['categories'],
                           problems=topic_data['problems'])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
