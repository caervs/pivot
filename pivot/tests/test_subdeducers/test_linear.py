import unittest

from pivot.subdeducers.linear import Vector, Matrix, LinearDeducer

class VectorTestCase(unittest.TestCase):
    pass


class DyadicOperations(VectorTestCase):
    def test_add(self):
        v0 = Vector([1, 2, 3])
        v1 = Vector([4, 5, 6])
        vsum = Vector([5, 7, 9])
        self.assertEqual(v0 + v1, vsum)

    def test_sub(self):
        v0 = Vector([1, 2, 3])
        v1 = Vector([4, 5, 6])
        vdiff = Vector([-3, -3, -3])
        self.assertEqual(v0 - v1, vdiff)

    def test_mult(self):
        v0 = Vector([1, 2, 3])
        v1 = Vector([4, 5, 6])
        self.assertEqual(v0 * v1, 32)

    def test_scalar_mult(self):
        v0 = Vector([1, 2, 3])
        coefficient = 4
        vprod = Vector([4, 8, 12])
        self.assertEqual(coefficient * v0, vprod)

    def test_scalar_div(self):
        v0 = Vector([2, 4, 8])
        coefficient = 2
        vprod = Vector([1, 2, 4])
        self.assertEqual(v0 / coefficient, vprod)


class MutatingOperations(VectorTestCase):
    def test_iadd(self):
        v0 = Vector([1, 2, 3])
        v1 = Vector([4, 5, 6])
        vsum = Vector([5, 7, 9])

        v0 += v1
        self.assertEqual(v0, vsum)

    def test_isub(self):
        v0 = Vector([1, 2, 3])
        v1 = Vector([4, 5, 6])
        vdiff = Vector([-3, -3, -3])

        v0 -= v1
        self.assertEqual(v0, vdiff)

    def test_scalar_mult(self):
        v0 = Vector([1, 2, 3])
        coefficient = 4
        vprod = Vector([4, 8, 12])

        v0 *= coefficient
        self.assertEqual(v0, vprod)

    def test_scalar_div(self):
        v0 = Vector([2, 4, 8])
        coefficient = 2
        vprod = Vector([1, 2, 4])

        v0 /= coefficient
        self.assertEqual(v0, vprod)


class LinearDeducerTestCase(unittest.TestCase):
    pass


class ExampleSolutions(LinearDeducerTestCase):
    def test_example1(self):
        mat = Matrix([
            [1, 3, -2, 5],
            [3, 5, 6, 7],
            [2, 4, 3, 8],
        ])

        deducer = LinearDeducer()
        reduced_mat = deducer.reduce_mat(mat)

        expected_mat = Matrix([
            [1, 0, 0, -15],
            [0, 1, 0, 8],
            [0, 0, 1, 2],
        ])

        self.assertEqual(reduced_mat, expected_mat)
