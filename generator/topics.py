"""
Topic creation functions: Gets topic parameters, then returns valid problems.

Next steps:
    Add testing (see generator for sample dict).
    Add decimal handling
    Add fraction handling
    Add expression handling
    Add inequality handling
    Add quadratic handling
"""

# pylint: disable=R1723, R0912

import logging

import generator
import utilities
import database as db


def get_equation():
    """Get equation from user."""

    return input("What's your equation?\n  ")
    #### In the future, validate that it's an acceptable equation


def get_positive_only():
    """Determine whether answers must be positive."""

    while True:
        prompt = "Do the answers have to be positive? (y/n)\n>>"
        positive_only = input(prompt).lower()

        if positive_only in ('y', 'n'):
            break
        else:
            print("Please choose Yes (y) or No (n).")

    return positive_only


#### In the future, allow the user to:
    # Determine which variable to solve for (e.g. important that it's x in a quadratic)
    # Determine whether real or complex numbers are allowable (see domain= argument for solveset)


def get_var_parameters(equation):
    """
    Identify the variables in the equation, then parameters for each one.

        min: minimum value for this variable (type = int)
        max: maximum value for this variable (type = int)
        num_type: integer or decimal (type = str)
            # May add fraction and imaginary in the future, though those
              may be more important for outputs than inputs
        zero_ok: 'y' if zero is an acceptable value, 'n' if not

    Return as dict.
    """

    var_dict = {}

    # Identify the variables in the equation
    var_list = [char for char in equation if char.isalpha()]

    # Get parameters for each variable
    for var in sorted(set(var_list)):
        print(f"\nTell me about {var}.")

        # Get the minimum value of this variable
        while True:
            try:
                minimum = int(input("  Minimum: "))
                break
            except ValueError:
                print("Please enter an integer!")

        # Get the maximum value of this variable
        while True:
            try:
                maximum = int(input("  Maximum: "))
                if maximum < minimum:
                    print("Maximum must be greater than minimum.")
                else:
                    break
            except ValueError:
                print("Please enter an integer!")

        # If the variable range includes 0, ask whether 0 is a valid value
        if minimum <= 0 <= maximum:
            while True:
                zero_ok = input("  Zero ok (y/n): ").lower()

                if zero_ok in ('y', 'n'):
                    break
                else:
                    print("Please choose Yes (y) or No (n).")
        else:
            zero_ok = None

        # Get the variable type
        while True:
            num_type = input("  Integer (i) or Decimal (d): ")

            if num_type.lower() in ('i', 'd'):
                break
            else:
                print("Please choose Integer (i) or Decimal (d).")

        # Store the variable parameters in a dict
        var_dict[var] = {'min': minimum,
                         'max': maximum,
                         'zero_ok': zero_ok,
                         'num_type': num_type.lower()}

    return var_dict


def create_equation_dict(equation, positive_only, var_dict):
    """Build the initial equation dictionary."""

    equation_dict = {'equation': equation,
                     'positive_only': positive_only,
                     'variables': var_dict}

    return equation_dict


#### In the future, determine whether it's an equation, expression, or inequality


def main():
    """Get equation info, generate problems and write result to db."""

    utilities.start_logging()

    # Get equation info from user
    equation = get_equation()
    positive_only = get_positive_only()
    var_dict = get_var_parameters(equation)

    # Identify all valid problem combinations
    eq_dict = create_equation_dict(equation, positive_only, var_dict)
    equation = generator.Equation(eq_dict)
    equation.generate_problems()
    logging.info(equation.dict)

    # Store all information in the database
    db.write_to_topics_db(equation.dict)

if __name__ == "__main__":
    main()
