"""
Unit tests for the equation module
"""

import unittest

from pivot.lexicon import equation
from pivot.lexicon import expression


class EquationTestCase(unittest.TestCase):
    """
    Abstract base class for equation test cases
    """
    pass


class TestEquationFromDictDef(EquationTestCase):
    """
    Test creating an EquationSet from a dict
    """

    def test_simple_equation(self):
        """
        Test creating a simple equation
        """

        @equation.EquationSet.from_dict_def
        def equationset(x):
            """
            A simple equation set
            """
            return dict(x=x)

        x = expression.Variable("x")
        expected_set = equation.EquationSet([equation.Equation(x, x)])
        self.assertEqual(equationset, expected_set)

    def test_linear_equation(self):
        """
        Test creating a linear equation of medium complexity
        """

        @equation.EquationSet.from_dict_def
        def equationset(x, _y, _z):
            """
            Medium-complexity equation set
            """
            return dict(y=2 * x + 1, z=3 * x, x=1)

        x, y, z = map(expression.Variable, ["x", "y", "z"])
        expected_set = equation.EquationSet([
            equation.Equation(x, 1),
            equation.Equation(y, 2 * x + 1),
            equation.Equation(z, 3 * x),
        ])
        self.assertEqual(equationset, expected_set)
