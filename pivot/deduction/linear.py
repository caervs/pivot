"""
Linear deduction engine and related tools
"""

import itertools
import operator

from pivot.interface.deducer import SolvingEngine
from pivot.lexicon import expression
from pivot.ontology import matrix

OPERATOR_MAP = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}


class SumOfProducts(object):
    """
    Models an expression that is the sum of products of primitives
    """
    # TODO should have field attribute instead
    # TODO alternatively should be able to get
    # additive and multiplicate identity just by
    # subtracting and dividing coefficient from itself
    mult_identity = 1
    add_identity = 0

    def __init__(self, coefficients):
        self.coefficients = coefficients

    @classmethod
    def from_expression(cls, exp):
        """
        Create a SumOfProducts from an Expression
        """
        if not isinstance(exp, expression.Expression):
            return cls({cls.mult_identity: exp})
        elif isinstance(exp, expression.Variable):
            return cls({exp: cls.mult_identity})
        elif isinstance(exp, expression.OperationalExpression):
            return OPERATOR_MAP[exp.operator](*map(cls.from_expression,
                                                   exp.arguments))
        else:
            raise TypeError(type(exp))

    @classmethod
    def multiply_efficients(cls, eff0, eff1):
        """
        Multiply two multiplicands and reduce
        """
        if eff0 == cls.mult_identity:
            return eff1

        if eff1 == cls.mult_identity:
            return eff0
        return eff0 * eff1

    def __add__(self, other):
        coefficients = {}
        all_coefficients = itertools.chain(self.coefficients.items(),
                                           other.coefficients.items())
        for efficient, coefficient in all_coefficients:
            if efficient in coefficients:
                coefficients[efficient] += coefficient
            else:
                coefficients[efficient] = coefficient

        return type(self)(coefficients)

    def __neg__(self):
        return type(self)({efficient: -coefficient
                           for efficient, coefficient in
                           self.coefficients.items()})

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        coefficients = {}
        for eff0, coe0 in self.coefficients.items():
            for eff1, coe1 in other.coefficients.items():
                eff = self.multiply_efficients(eff0, eff1)
                coefficients[eff] = coe0 * coe1
        return type(self)(coefficients)

    def __truediv__(self, other):
        if set(other.coefficients.keys()) != {self.mult_identity}:
            raise ValueError("Division of expressions not supported")
        divisor = other.coefficients[self.mult_identity]
        return type(self)({eff: matrix.divide(coe, divisor)
                           for eff, coe in self.coefficients.items()})


class LinearEngine(SolvingEngine):
    """
    Deduction engine for solving linear systems
    """
    parsed_expression_class = SumOfProducts

    @classmethod
    def solve_equation_set(cls, eq_set):
        """
        Return the solutions of a linear system as a dict mapping
        Variables to values
        """
        mult_identity = cls.parsed_expression_class.mult_identity
        add_identity = cls.parsed_expression_class.add_identity
        variables = []
        matrix_entries = []
        augmentations = []
        for equation in eq_set:
            coefficients = cls.parsed_expression_class.from_expression(
                equation.subj - equation.obj).coefficients
            augmentations.append(-coefficients.get(mult_identity,
                                                   add_identity))
            old_variables = set(variables + [mult_identity])
            variables.extend(set(coefficients) - old_variables)
            matrix_entries.append([coefficients.get(variable, add_identity)
                                   for variable in variables])
        rows = []
        for index, entry in enumerate(matrix_entries):
            zeroes = [add_identity] * (len(variables) - len(entry))
            rows.append(entry + zeroes + [augmentations[index]])

        reduced = matrix.AugmentedMatrix(rows).reduced_form
        return dict(zip(variables, reduced.constants))
