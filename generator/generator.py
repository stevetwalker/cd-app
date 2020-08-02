"""Processes user inputs, then writes topic and problem data to the db."""

import logging
import utilities
import database as db
from topic import Topic
from forms import EquationForm, VariableForm, EquationParametersForm


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
    var_dict = {}
    for i, variable in enumerate(data_dict.getlist('variable')):

        # zero_ok returns a list of all variables where zero_ok is checked
        if variable in data_dict.getlist('zero_ok'):
            zero_result = 'y'
        else:
            zero_result = 'n'

        var_dict[variable] = {
            'min': data_dict.getlist('minimum')[i],
            'max': data_dict.getlist('maximum')[i],
            'zero_ok': zero_result,
            'num_type': 'i'} ### Temporarily hard coded, but will need to fix ###

    return var_dict


def create_equation_dict(var_dict, data_dict):
    """Package equation parameters into equation_dict."""

    # Split categories from string to dict
    category_list = data_dict['categories'].split(', ')
    category_dict = {}
    for i, category in enumerate(category_list):
        category_dict[str(i)] = category

    # Assess positive_only equation parameter
    if 'positive_only' in data_dict.keys():
        positive_only = 'y'
    else:
        positive_only = 'n'

    # Package equation parameters into equation_dict
    equation_dict = {'equation': data_dict['eq'],
                     'topic': data_dict['topic'],
                     'instructions': data_dict['instructions'],
                     'categories': category_dict,
                     'positive_only': positive_only,
                     'variables': var_dict}

    logging.info(equation_dict)
    return equation_dict

def build_topic(data_dict):
    """Get equation info, generate problems and write result to db."""

    utilities.start_logging()

    # Identify all valid problem combinations
    var_dict = package_variables(data_dict)
    eq_dict = create_equation_dict(var_dict, data_dict)
    topic = Topic(eq_dict)
    topic.generate_problems()
    print('generate problems')
    logging.info(topic.dict)

    # Store all information in the database
    topic_id = db.write_to_topics_db(topic.dict)
    return topic_id
