"""
Unit tests for the matrix module
"""

import unittest

from pivot.ontology import matrix


class MatrixTestCase(unittest.TestCase):
    """
    Abstract base class for Matrix test cases
    """
    pass


# TODO more broken down tests
class TestReduction(MatrixTestCase):
    """
    Test reducing an augmented matrix to the identity matrix
    """

    def test_reduce_simple(self):
        """
        a simple test of row reduction
        """
        mat = matrix.AugmentedMatrix([[1, 3, -2, 5], [3, 5, 6, 7],
                                      [2, 4, 3, 8]])
        self.assertEqual(mat.reduced_form.constants,
                         matrix.Vector([-15, 8, 2]))
