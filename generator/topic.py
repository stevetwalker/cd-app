"""
Accepts equations, then generates sample problems.
"""

# pylint: disable=C0103, W1202, R0201

import logging
import itertools
from sympy import FiniteSet, ConditionSet
from sympy.abc import x
from sympy.solvers import solveset
from sympy.parsing.sympy_parser import parse_expr,\
                                       standard_transformations,\
                                       implicit_multiplication_application
from sympy.printing import latex
import utilities


# Sample data
an_equation_dict = {'equation': 'a**2+b**2=c**2',
                    'positive_only': 'y',
                    'variables':
                    {'a': {'min': -1, 'max': 20, 'zero_ok': 'n', 'num_type': 'i'},
                     'b': {'min': 1, 'max': 20, 'zero_ok': None, 'num_type': 'i'},
                     'c': {'min': 1, 'max': 100, 'zero_ok': None, 'num_type': 'i'}}}


class Topic():
    """
    Store data associated with each equation.
        equation: User inputted equation  # May want to change this to sympy formatted equation
        type: Specifies whether it is an equation, inequality or expression. # Not built yet
        variables: Defines parameters for each variable.
        problems: Lists variable values for all valid problems.
    """

    @utilities.timer
    def __init__(self, equation_dict):
        """Initialize the equation object."""
        self.equation = equation_dict['equation']
        self.variables = equation_dict['variables']
        self.dict = equation_dict
        self.x = list(self.variables)[-1] # The variable to solve for


    def prep_equation(self):
        """
        Transform the inputted equation into a sympy readable equation.
        When solving, sympy only accepts expressions and assumes they're
        equal to 0. This code transforms equations into valid expressions.

        FYI: implicit_multiplication_application turns xyz into x*y*z
        """
        
        # This transforms the equation into an expression for sympy.
        prepped_equation = self.equation.replace("=", "-(") + ")"

        # This transforms the equation string into a sympy-readable equation.
        transformations = standard_transformations + (implicit_multiplication_application,)
        prepped_equation = parse_expr(prepped_equation, transformations=transformations)

        return prepped_equation


    @utilities.timer
    def generate_var_ranges(self):
        """
        Generate dict of all possible values for each input variable. Do
        not generate all possible values of self.x, as that's the variable
        we'll solve for.
        """

        var_ranges = {}
        for variable in self.variables:
            var = self.variables[variable]
            min_to_max = list(range(int(var['min']), int(var['max']) + 1))
            if (var['zero_ok'] == 'n' and 0 in min_to_max):
                min_to_max.remove(0)

            var_ranges[variable] = min_to_max

        return var_ranges


    @utilities.timer
    def generate_input_array(self, var_ranges):
        """
        Using the var_ranges, generate array of all possible variable-value
        combinations, excluding the variable to be solved for.
        """

        # Pull all possible values for each input variable from the
        # var_ranges dict. Do not pull possible values for the last
        # variable in the dict because that's the one we'll solve for.
        input_values = [var_ranges[k] for i, k in enumerate(var_ranges)
                        if i < len(var_ranges)-1]

        # Generate all possible variable combinations as a list of tuples
        input_array = list(itertools.product(*input_values))

        return input_array


    @utilities.timer
    def generate_valid_combos(self, prepped_equation, var_ranges, input_array):
        """Generate a list of variable combinations for all valid problems."""

        valid_combos = []

        # Generate the set of valid answer values as a FiniteSet. The
        # FiniteSet is necessary because sympy returns a FiniteSet when
        # it solves equations.
        solution_set = FiniteSet(*var_ranges[str(self.x)])

        # For every variable combination, substitute the values for each
        # input variable into the final_equation so sympy can solve for the
        # remaining variable.
        for var_values in input_array:
            final_equation = prepped_equation
            for i, var in enumerate(self.variables):
                if i < len(self.variables)-1:
                    final_equation = final_equation.subs(var, var_values[i])

            # Solve for self.x.
            answer = solveset(final_equation, self.x)

            #### Currently, this is just rigged to capture when we have a single integer solution
            if self.dict['positive_only'] == 'y':
                answer = answer.intersection(ConditionSet(x, x > 0))

            # Add valid combinations to valid_combos list, with each valid combo as a dict
            if answer.issubset(solution_set) and answer != set():
                valid_combo = {}
                valid_combo['values'] = {}

                # Add variable values to dict
                for i, var in enumerate(self.variables):
                    if i < len(self.variables)-1:
                        valid_combo['values'][var] = int(var_values[i])    ### Forces int, which needs to be updated

                # Add answer value(s) to dict
                valid_combo['values'][self.x] = [int(i) for i in answer]

                valid_combos.append(valid_combo)

        return valid_combos

    def write_problems(self, valid_combos):
        """Takes variable values and returns problem / answer pairs as LaTeX."""

        # To be used when converting the equation to sympy
        transformations = standard_transformations + (implicit_multiplication_application,)

        # To preserve the order of the expression, may need to sub each arg separately and then reconstruct the whole equation (sympy can identify each term as an arg)
        for combo in valid_combos:

            # Sympy doesn't like equations, so this allows it to evaluate
            # the left and right side independently
            subbed_left_side = self.equation[:self.equation.find('=')]
            subbed_right_side = self.equation[self.equation.find('=')+1:]

            for i, var in enumerate(self.variables):

                # Replace non-answer variables with values
                if i < len(self.variables)-1:
                    subbed_left_side = subbed_left_side.replace(var, str(combo['values'][var]))
                    subbed_right_side = subbed_right_side.replace(var, str(combo['values'][var]))

                # Store the answer(s)
                else:
                    if len(combo['values'][var]) == 1:
                        combo['answer'] = f"{var} = {combo['values'][var][0]}"
                    else:
                        combo['answer'] = f"{var} = {combo['values'][var]}"

            # Latexify each side of the equation, then concatenate
            latex_left_side = latex(parse_expr(subbed_left_side,
                                               transformations=transformations,
                                               evaluate=False))
            latex_right_side = latex(parse_expr(subbed_right_side,
                                                transformations=transformations,
                                                evaluate=False))
            latex_problem = str(latex_left_side) + ' = ' + str(latex_right_side)

            combo['problem'] = str(latex_problem)

    def generate_problems(self):
        """Update self.dict with list of viable inputs for each variable."""

        prepped_equation = self.prep_equation()
        var_ranges = self.generate_var_ranges()
        input_array = self.generate_input_array(var_ranges)
        valid_combos = self.generate_valid_combos(prepped_equation, var_ranges, input_array)
        self.write_problems(valid_combos)
        self.dict['problems'] = valid_combos
        logging.info(f"Generated {len(self.dict['problems'])} valid problems.")
        logging.info(self.dict['problems'])
