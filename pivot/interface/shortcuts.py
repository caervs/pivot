"""
Useful tools to reduce the amount of code needed to use pivot
"""

from pivot.lexicon.expression import Variable


def update_with_variables(scope, variables):
    """
    update a dict to include variables of given names
    """
    scope.update((name, Variable(name)) for name in variables)
