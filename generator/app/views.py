from flask import Flask, render_template, request, redirect, url_for, session
from flask_appbuilder import BaseView, ModelView, AppBuilder, expose, has_access
from flask_appbuilder.models.mongoengine.interface import MongoEngineInterface
from app import appbuilder, generator, utilities

import logging
import app.database as db
from app.forms import EquationForm, VariableForm, EquationParametersForm
from app.models import Topics


class GenerateTopics(BaseView):
    """Admin's topic generation view ('/')"""

    route_base = '/'
    default_view = 'generate'

    @expose('/generate', methods=['GET', 'POST'])
    @has_access # password protected
    def generate(self):
        """Get equation parameters, then generate all viable problems."""
        equation_form, equation_params = EquationForm(), EquationParametersForm()

        if request.method == 'POST':

            try:
                # If submitting valid equation data, get var data from equation
                if equation_form.validate_on_submit():
                    equation, variables, variable_forms = \
                        generator.process_equation(equation_form, equation_params)

                    self.update_redirect()
                    return self.render_template('generator.html',
                                                equation_form=equation_form,
                                                variable_forms=variable_forms,
                                                variables=variables,
                                                equation_params=equation_params)

                # If submitting variable and equation params, store them in equation_dict
                if equation_params.validate_on_submit():
                    topic_id = generator.build_topic(request.form)

                    return redirect(url_for('GenerateTopics.results', topic_id=topic_id))

            except Exception as err:
                   print(err)

        self.update_redirect()
        return self.render_template('generator.html', equation_form=equation_form)


    @expose('/results', methods=['GET', 'POST'])
    @has_access # password protected
    def results(self):
        """Display generated problems."""
        topic_id = request.args.get('topic_id')
        topic_data = Topics.objects.get(id=topic_id)
        print(topic_data)

        if request.method == 'POST':
            try:
                return redirect(url_for('GenerateTopics.generate'))

            except Exception as err:
                   print(err)

        self.update_redirect()
        return self.render_template('results.html',
                                    topic=topic_data['topic'],
                                    equation=topic_data['equation'],
                                    instructions=topic_data['instructions'],
                                    categories=topic_data['categories'],
                                    problems=topic_data['problems'])

# Adds Generate link to persistent nav, which directs to the default_view
appbuilder.add_view(GenerateTopics, "Generate") # Optional parameter of category=dropdown_name


"""
    Database admin views
"""

class TopicsModelView(ModelView):
    route_base = '/topics'
    datamodel = MongoEngineInterface(Topics)

    label_columns = {'topic': 'Topic',
                     'equation': 'Equation',
                     'instructions': 'Instructions',
                     'variables': 'Variables',
                     'problems': 'Problems'}

    # Data on summary page
    list_columns = ['topic', 'equation']

    # Data on details page
    show_fieldsets = [
        ('Topic Info', {'fields': ['topic', 'equation', 'instructions']}),
        ('Variable Info', {'fields': ['variables']}),
        ('Problems', {'fields': ['problems']})
        ]

appbuilder.add_view(TopicsModelView, "Database")



"""
    Application wide 404 error handler
"""

@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

