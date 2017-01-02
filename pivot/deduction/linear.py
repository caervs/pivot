"""
Linear deduction engine and related tools
"""

import enum
import itertools
import operator

from pivot.interface.deducer import SolvingEngine
from pivot.lexicon import expression
from pivot.ontology import matrix
from pivot.ontology import plane

OPERATOR_MAP = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}


class SolutionMethod(enum.Enum):
    """
    A method to use when solving a linear system
    """
    BUILTIN = 0
    NUMPY = 1


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
            return OPERATOR_MAP[exp.operator](
                *list(map(cls.from_expression, exp.arguments)))
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
        return type(self)({
            efficient: -coefficient
            for efficient, coefficient in self.coefficients.items()
        })

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
        return type(self)({
            eff: matrix.divide(coe, divisor)
            for eff, coe in self.coefficients.items()
        })


class LinearEngine(SolvingEngine):
    """
    Deduction engine for solving linear systems
    """
    parsed_expression_class = SumOfProducts

    # TODO refactor
    @classmethod
    def solve_equation_set(cls, eq_set, method=SolutionMethod.NUMPY):  # pylint: disable=R0914
        """
        Return the solutions of a linear system as a dict mapping
        Variables to values

        Takes an optional method to use to solve the equation set
        Options are:
          - NUMPY: solve using numpy. This will convert all constants
                   to floats so it is only recommended if you are not
                   using a custom field
          - BUILTN: works with custom fields but is buggy so use with
                    caution
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
            matrix_entries.append([
                coefficients.get(variable, add_identity)
                for variable in variables
            ])
        rows = []
        for index, entry in enumerate(matrix_entries):
            zeroes = [add_identity] * (len(variables) - len(entry))
            rows.append(entry + zeroes + [augmentations[index]])

        if method == SolutionMethod.BUILTIN:
            # TODO investigate bug with BUILTIN method and return
            # to default when done
            reduced = matrix.AugmentedMatrix(rows).reduced_form
            return dict(zip(variables, reduced.constants))
        elif method == SolutionMethod.NUMPY:
            from numpy import array
            from numpy.linalg import solve
            mat = array(list(list(map(float, row[:-1])) for row in rows))
            constants = array(list(list(map(float, row[-1:])) for row in rows))
            solutions = [row[0] for row in solve(mat, constants)]
            return dict(zip(variables, solutions))
        else:
            raise ValueError(method)


class PlanarEngine(LinearEngine):
    """
    Deduction engine for solving linear systems consisting of 2d vectors
    """

    @classmethod
    def solve_equation_set(cls, eq_set, method=SolutionMethod.NUMPY):
        split_eq_set = set()
        for equation in eq_set:
            split_subj = cls.split_expression(equation.subj)
            split_obj = cls.split_expression(equation.obj)
            if len(split_subj) != len(split_obj):
                raise ValueError("Mixing vector and scalar expressions")
            for subj_part, obj_part in zip(split_subj, split_obj):
                split_eq_set.add(subj_part == obj_part)
        split_solutions = super().solve_equation_set(
            split_eq_set, method=method)
        vector_variables = {
            component.variable
            for component in split_solutions
        }
        return {
            vector_variable: plane.PlaneVector(
                (split_solutions[vector_variable.x],
                 split_solutions[vector_variable.y]))
            for vector_variable in vector_variables
        }

    @classmethod
    def _split_operational_expression(cls, exp):
        if exp.operator == "/":
            # TODO are expressions like 1 / 2 / 3 composed into single OE?
            divisor = cls.split_expression(exp.arguments[1])
            if len(divisor) != 1:
                raise ValueError("Cannot divide by vector")
            return [
                subexp / divisor[0]
                for subexp in cls.split_expression(exp.arguments[0])
            ]
        elif exp.operator == "*":
            scalar = cls.split_expression(exp.arguments[0])
            if len(scalar) != 1:
                raise ValueError("Cannot multiply by vector")
            return [
                scalar[0] * subexp
                for subexp in cls.split_expression(exp.arguments[1])
            ]

        subexpressions = list(map(cls.split_expression, exp.arguments))
        lengths = list(map(len, subexpressions))
        if min(lengths) != max(lengths):
            raise ValueError("Mixing vector and scalar expressions",
                             subexpressions, exp)
        components = []
        for i in range(min(lengths)):
            components.append(
                expression.OperationalExpression(exp.operator, *(subexpression[
                    i] for subexpression in subexpressions)))
        return components

    @classmethod
    def split_expression(cls, exp):
        """
        Given an expression for a planar vector returns a list [x, y] where x
        evaluates to the x component of the vector and y likewise
        """
        if not isinstance(exp, expression.Expression):
            return [exp]
        elif isinstance(exp, expression.Vector):
            return list(exp.items)
        elif isinstance(exp, expression.Variable):
            if isinstance(exp, expression.VariableAttribute) \
               and exp.attr_name in ('x', 'y'):
                return [exp]
            else:
                return [exp.x, exp.y]
        elif isinstance(exp, expression.OperationalExpression):
            return cls._split_operational_expression(exp)
        else:
            raise TypeError(type(exp))

    @classmethod
    def evaluate_expression(cls, exp, values):
        """
        return the value of an expression given values for its subexpressions
        """
        if not isinstance(exp, expression.Expression):
            return exp
        elif isinstance(exp, expression.Vector):
            if exp in values:
                return values[exp]
            else:
                return plane.PlaneVector((
                    cls.evaluate_expression(exp.items[0], values),
                    cls.evaluate_expression(exp.items[1], values), ))
        elif isinstance(exp, expression.Variable):
            if isinstance(exp, expression.VariableAttribute) \
               and exp.attr_name in ('x', 'y'):
                return getattr(values[exp.variable], exp.attr_name)
            else:
                return values[exp]
        elif isinstance(exp, expression.OperationalExpression):
            subvalues = [
                cls.evaluate_expression(subexp, values)
                for subexp in exp.arguments
            ]
            return OPERATOR_MAP[exp.operator](*subvalues)
        else:
            raise TypeError(type(exp))
