import numbers
# Symbolic mathematics
from sympy import *

def trigonometric(number):

    return dict({   'sin': str(sin(number)),
                    'cos': str(cos(number)),
                    'tan': str(tan(number)),
                    'cot': str(cot(number))})

def get_all(input):
    # Initialize results dictionary
    results = dict({'input': input})

    # Check if input is a nubmer
    try:
        number = float(input)
        # Update results dictionary with trigonometric calculations
        results.update(trigonometric(number))
    except ValueError:
        pass

    return results
