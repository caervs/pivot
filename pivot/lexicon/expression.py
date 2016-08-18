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

    def __hash__(self):
        return hash(frozenset(self.parts.items()))

    def __eq__(self, other):
        equation = importlib.import_module("pivot.lexicon.equation")
        same_exp = super().__eq__(other)
        return equation.Equation(self, other, reflexive=same_exp)


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

    def __getattr__(self, attr_name):
        if attr_name.startswith("_"):
            return getattr(super(), attr_name)
        return VariableAttribute(self, attr_name)


class VariableAttribute(Variable):
    """
    The attribute of a variable (which is also a variable)
    """

    @preprocessor
    def preprocess(variable, attr_name):
        """
        Preprocess VariableAttribute attributes
        """
        pass

    def __repr__(self):
        return "{}.{}".format(self.variable, self.attr_name)


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


class Vector(Expression):
    """
    An expression denoting an ontological Vector (i.e. an expression that is an
    enumeration of subexpressions)
    """

    @preprocessor
    def preprocess(*items):
        """
        Preprocess Vector attributes
        """
        pass

    def __repr__(self):
        return "V({})".format(", ".join(map(repr, self.items)))
