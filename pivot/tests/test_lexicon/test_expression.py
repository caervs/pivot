"""
Unit tests for the expression module
"""

from fractions import Fraction

from pivot.interface.shortcuts import V
from pivot.lexicon import expression


class ExpressionTestCase(object):
    """
    Abstract base class for Expression test cases
    """

    @staticmethod
    def assert_equal(left, right):
        """
        Assert that two Expressions are equal
        """
        msg = "{} != {}".format(left, right)
        assert left == right, msg

    def generate_from_data(self, data):
        """
        Generate test cases from an iterable of ordered pairs
        """
        for left, right in data:
            yield self.assert_equal, left, right


class TestExpressionsComposition(ExpressionTestCase):
    """
    Test composition of expressions
    """

    def test_first_level_composition(self):
        """
        test composing variables with all operators
        """
        oe = expression.OperationalExpression
        v1, v2 = map(expression.Variable, ["v1", "v2"])
        data = [
            [(v1 + v2), oe('+', v1, v2)],
            [(v1 - v2), oe('-', v1, v2)],
            [(v1 / v2), oe('/', v1, v2)],
            [(v1 * v2), oe('*', v1, v2)],
        ]
        yield from self.generate_from_data(data)

    def test_primitive_composition(self):
        """
        test medium level composition of expressions
        """
        oe = expression.OperationalExpression
        v1 = expression.Variable("v1")
        f = Fraction(3 / 5)
        data = [
            [(v1 + 1), oe('+', v1, 1)],
            [(v1 - 2.0), oe('-', v1, 2.0)],
            [(v1 / f), oe('/', v1, f)],
            [(1 * v1), oe('*', 1, v1)],
        ]
        yield from self.generate_from_data(data)

    def test_second_level_composition(self):
        """
        test slightly harder composition of expressions
        """
        oe = expression.OperationalExpression
        v1, v2 = map(expression.Variable, ["v1", "v2"])
        exp = (v1 + v2) / (v1 - v2)
        expected_exp = oe('/', oe('+', v1, v2), oe('-', v1, v2))
        self.assert_equal(exp, expected_exp)

    def test_compose_vectors_with_attrs(self):
        """
        Test a composing expression that has vectors with variable attributes
        """
        oe = expression.OperationalExpression
        v1, v2 = map(expression.Variable, ["v1", "v2"])
        exp = 1 + V(v1.x, v2.y)
        expected_exp = oe('+', 1, V(v1.x, v2.y))
        self.assert_equal(exp, expected_exp)
