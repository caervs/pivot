"""
Unit tests for the linear deduction engine
"""

import unittest

from pivot.deduction import linear
from pivot.lexicon import equation
from pivot.lexicon import expression


class SumOfProductsTestCase(unittest.TestCase):
    """
    Abstract base class for SumOfProducts test cases
    """
    pass


class BasicExpressionComposition(SumOfProductsTestCase):
    """
    Basic tests of SumOfProducts expression composition
    """

    def test_simple_expression(self):
        """
        Test creating a simple expression
        """
        x = expression.Variable("x")
        sop = linear.SumOfProducts.from_expression(x)
        self.assertEqual(sop.coefficients, {x: 1})

    def test_add_same(self):
        """
        Test creating a mono-vairable expression and adding it to itself
        """
        x = expression.Variable("x")
        sop = linear.SumOfProducts.from_expression(x + x)
        self.assertEqual(sop.coefficients, {x: 2})

    def test_add_different(self):
        """
        Test adding expressions with different variables
        """
        x, y = map(expression.Variable, ["x", "y"])
        sop = linear.SumOfProducts.from_expression(x + y)
        self.assertEqual(sop.coefficients, {x: 1, y: 1})

    def test_add_mixed(self):
        """
        Test adding mixture of same and different variables
        """
        x, y = map(expression.Variable, ["x", "y"])
        sop = linear.SumOfProducts.from_expression(x + y + x)
        self.assertEqual(sop.coefficients, {x: 2, y: 1})

    def test_add_mixed_with_coeffs(self):
        """
        Test adding mixture of same and different variables with coefficients
        """
        x, y = map(expression.Variable, ["x", "y"])
        sop = linear.SumOfProducts.from_expression(2 * x + 3 * y + x)
        self.assertEqual(sop.coefficients, {x: 3, y: 3})

    def test_add_mixed_with_division(self):
        """
        Test adding mixture of same and different variables with division
        """
        x, y = map(expression.Variable, ["x", "y"])
        sop = linear.SumOfProducts.from_expression((2 * x + 3 * y + x) / 3)
        self.assertEqual(sop.coefficients, {x: 1, y: 1})


class LinearEngineTestCase(unittest.TestCase):
    """
    Abstract base class for cases testing the linear deduction engine
    """
    pass


class BasicEquationSolving(LinearEngineTestCase):
    """
    Test basic linear equation solving
    """

    def test_simple_equation(self):
        """
        simple test of linear equation solving
        """
        x, y = map(expression.Variable, ["x", "y"])
        eq_set = equation.EquationSet.from_equations(x=1, y=x)
        solutions = linear.LinearEngine.solve_equation_set(eq_set)
        self.assertEqual(solutions, {x: 1, y: 1})

    def test_medium_equation(self):
        """
        medium complexity test of linear equation solving
        """
        x, y, z = map(expression.Variable, ["x", "y", "z"])
        eq_set = equation.EquationSet.from_equations(
            x == 5 - 3 * y + 2 * z,
            x == ((7 - 5 * y - 6 * z) / 3),
            x == ((8 - 4 * y - 3 * z) / 2), )
        solutions = linear.LinearEngine.solve_equation_set(eq_set)
        self.assertEqual(solutions, {x: -15, y: 8, z: 2})
