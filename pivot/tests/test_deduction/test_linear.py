"""
Unit tests for the linear deduction engine
"""

import unittest

from pivot.deduction import linear
from pivot.interface.shortcuts import PV, V
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


class PlanarEngineTestCase(unittest.TestCase):
    """
    Abstract base class for cases testing the planar deduction engine
    """
    pass


class BasicPlanarEquationSolving(PlanarEngineTestCase):
    """
    Test basic linear equation solving
    """

    def test_simple_equation(self):
        """
        simple test of planar equation solving
        """
        v1, v2 = map(expression.Variable, ["v1", "v2"])
        eq_set = equation.EquationSet.from_equations(v1=V(1, 2), v2=V(3, 4))
        solutions = linear.PlanarEngine.solve_equation_set(eq_set)
        self.assertEqual(solutions, {v1: PV(1, 2), v2: PV(3, 4)})

    def test_medium_equation(self):
        """
        medium complexity test of planar equation solving
        """
        v1, v2, v3 = map(expression.Variable, ["v1", "v2", "v3"])
        eq_set = equation.EquationSet.from_equations(
            v1 == V(5, 5) - 3 * v2 + 2 * v3,
            v1 == ((V(7, 7) - 5 * v2 - 6 * v3) / 3),
            v1 == ((V(8, 8) - 4 * v2 - 3 * v3) / 2), )
        solutions = linear.PlanarEngine.solve_equation_set(eq_set)
        self.assertEqual(solutions, {
            v1: PV(-15, -15),
            v2: PV(8, 8),
            v3: PV(2, 2),
        })


class BasicExpressionEvaluation(PlanarEngineTestCase):
    """
    Test PlanarEngine evaluate_expression method
    """

    def test_single_var_expression(self):
        """
        test evaluating a single expression
        """
        v1 = expression.Variable("v1")
        actual = linear.PlanarEngine.evaluate_expression(v1, {v1: 1})
        self.assertEqual(1, actual)

    def test_vector_expression(self):
        """
        test a vector expression consisting of attr expressions
        """
        v1, v2 = map(expression.Variable, ["v1", "v2"])
        vecexp = V(v1.x, v2.y)
        context = {v1: PV(1, 2), v2: PV(3, 4)}
        actual = linear.PlanarEngine.evaluate_expression(vecexp, context)
        self.assertEqual(PV(1, 4), actual)

    def test_operation(self):
        """
        test an operation expression
        """
        v1, v2 = map(expression.Variable, ["v1", "v2"])
        opexp = v1 + v2
        context = {v1: PV(1, 2), v2: PV(3, 4)}
        actual = linear.PlanarEngine.evaluate_expression(opexp, context)
        self.assertEqual(PV(4, 6), actual)
