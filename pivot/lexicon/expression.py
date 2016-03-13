"""
Models for symbols and symbolic expressions
"""

import importlib
from fractions import Fraction

from replicate.replicable import Replicable, preprocessor

PRIMITIVE_EXPRESSION_TYPES = (int, float, Fraction)


class Expression(Replicable):
    """
    A mathematical expression. May be operationally composed with other expressions
    """
    __add__ = lambda *args: OperationalExpression('+', *args)
    __sub__ = lambda *args: OperationalExpression('-', *args)
    __mul__ = lambda *args: OperationalExpression('*', *args)
    __truediv__ = lambda *args: OperationalExpression('/', *args)

    __radd__ = lambda *args: OperationalExpression('+', *reversed(args))
    __rsub__ = lambda *args: OperationalExpression('-', *reversed(args))
    __rmul__ = lambda *args: OperationalExpression('*', *reversed(args))
    __rtruediv__ = lambda *args: OperationalExpression('/', *reversed(args))

    def __le__(self, other):
        equation = importlib.import_module("pivot.lexicon.equation")
        return equation.Equation(self, other)


class Variable(Expression):
    """
    A single variable
    """

    @preprocessor
    def preprocess(name):
        """
        Preprocess Variable attributes
        """
        pass

    def __repr__(self):
        return self.name


class OperationalExpression(Expression):
    """
    An operational composition of two expressions
    """

    @preprocessor
    def preprocess(operator, *arguments):
        """
        Preprocess OperationalExpression attributes
        """
        pass

    def __repr__(self):
        delimiter = " {} ".format(self.operator)
        return delimiter.join(map(repr, self.arguments))
