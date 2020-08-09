"""Processes user inputs, then writes topic and problem data to the db."""

import logging
from app import utilities
from app.topic import Topic
from app.forms import EquationForm, VariableForm, EquationParametersForm
from app.models import Topics


def process_equation(equation_form, equation_params):
    """
    Identify variables in the submitted equation, then return the equation
    string, a list of variables and a second list with a corresponding 
    VariableForm for each variable.
    """

    equation = equation_form.equation.data
    print(equation)

    # Identify the vars in the equation and create a VariableForm for each
    variables = sorted(set([char for char in equation if char.isalpha()]))
    variable_forms = []
    for var in variables:
        var = VariableForm()
        variable_forms.append(var)
    print(variables, variable_forms)

    return equation, variables, variable_forms


def package_variables(data_dict):
    """Package variable parameters into var_dict."""
    var_docs = []
    for i, variable in enumerate(data_dict.getlist('variable')):

        # zero_ok returns a list of all variables where zero_ok is checked
        if variable in data_dict.getlist('zero_ok'):
            zero_result = True
        else:
            zero_result = False

        var_dict = {
            'variable': variable,
            'min': int(data_dict.getlist('minimum')[i]),
            'max': int(data_dict.getlist('maximum')[i]),
            'zero_ok': zero_result,
            'num_type': 'i'} ### Temporarily hard coded, but will need to fix ###

        var_docs.append(var_dict)

    return var_docs


def create_equation_dict(var_docs, data_dict):
    """Package equation parameters into equation_dict."""

    # Split categories from string to list
    category_list = data_dict['categories'].split(', ')

    # Assess positive_only equation parameter
    if 'positive_only' in data_dict.keys():
        positive_only = True
    else:
        positive_only = False

    # Package equation parameters into equation_dict
    equation_dict = {'equation': data_dict['eq'],
                     'topic': data_dict['topic'],
                     'instructions': data_dict['instructions'],
                     'categories': category_list,
                     'positive_only': positive_only,
                     'variables': var_docs}

    logging.info(equation_dict)
    return equation_dict


def build_topic(data_dict):
    """Get equation info, generate problems and write result to db."""

    utilities.start_logging()
    # Identify all valid problem combinations
    var_docs = package_variables(data_dict)
    eq_dict = create_equation_dict(var_docs, data_dict)
    topic = Topic(eq_dict)
    topic.generate_problems()
    logging.info(topic.dict)

    # Save to Topics database with mongoengine
    logging.info('Sending to the databases.')
    topic_doc = Topics(**topic.dict)
    topic_doc.save()
    logging.info(f'Saved {topic_doc.topic} to the database.')

    return topic_doc.id
