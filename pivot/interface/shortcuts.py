"""
Useful tools to reduce the amount of code needed to use pivot
"""

from pivot.lexicon import expression
from pivot.ontology import plane


def update_with_variables(scope, variables):
    """
    update a dict to include variables of given names
    """
    scope.update((name, expression.Variable(name)) for name in variables)


def PV(x, y):  # pylint: disable=invalid-name
    """
    Return a PlaneVector given coordinates
    """
    return plane.PlaneVector((x, y))


def V(*items):  # pylint: disable=invalid-name
    """
    Return a Vector expression given items
    """
    return expression.Vector(*items)
