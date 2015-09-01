import unittest

from pivot.props.equation import EquationSet, SymbolDict
from pivot.subdeducers.linear import LinearDeducer, Matrix, Vector


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
    def setUp(self):
        self.deducer = LinearDeducer()
        self.sd = SymbolDict()


class ExampleSolutions(LinearDeducerTestCase):
    def test_example1(self):
        mat = Matrix([
            [1, 3, -2, 5],
            [3, 5, 6, 7],
            [2, 4, 3, 8],
        ])

        reduced_mat = self.deducer.reduce_mat(mat)

        expected_mat = Matrix([
            [1, 0, 0, -15],
            [0, 1, 0, 8],
            [0, 0, 1, 2],
        ])

        self.assertEqual(reduced_mat, expected_mat)

    def test_example1_as_equation_set(self):
        @EquationSet
        def example_eqset(x, y, z):
            x = 5 - 3*y + 2*z
            x = (7 - 5*y - 6*z) / 3
            x = (8 - 4*y - 3*z) / 2

        solution = self.deducer.solve_equation_set(example_eqset)
        self.assertEqual(solution, {
            self.sd.x: -15,
            self.sd.y: 8,
            self.sd.z: 2,
        })


class ExtractsCoefficientsFromExpression(LinearDeducerTestCase):
    def test_single_primitive_literal(self):
        @EquationSet
        def eqset(x):
            x = 1

        equation, = eqset
        left_coefficients = self.deducer.coefficients_of_expression(equation.left_expression)
        self.assertEqual(left_coefficients, {self.sd.x: 1})

        right_coefficients = self.deducer.coefficients_of_expression(equation.right_expression)
        self.assertEqual(right_coefficients, {1: 1})

    def test_single_primitive_variable(self):
        @EquationSet
        def eqset(x, y):
            x = y

        equation, = eqset
        right_coefficients = self.deducer.coefficients_of_expression(equation.right_expression)
        self.assertEqual(right_coefficients, {self.sd.y: 1})

    def test_single_sandwiched_variable(self):
        @EquationSet
        def eqset(x, y):
            x = 2*y*3

        equation, = eqset
        right_coefficients = self.deducer.coefficients_of_expression(equation.right_expression)
        self.assertEqual(right_coefficients, {self.sd.y: 6})


    def test_dual_sandwiched_variables(self):
        @EquationSet
        def eqset(x, y, z):
            x = 2*y*3 + 5*z*10*2

        equation, = eqset
        right_coefficients = self.deducer.coefficients_of_expression(equation.right_expression)
        self.assertEqual(right_coefficients, {
            self.sd.y: 6,
            self.sd.z: 100,
        })

    def test_dual_sandwiched_variables_with_multiplier(self):
        @EquationSet
        def eqset(x, y, z):
            x = 4*(2*y*3 + 5*z*10*2)

        equation, = eqset
        right_coefficients = self.deducer.coefficients_of_expression(equation.right_expression)
        self.assertEqual(right_coefficients, {
            self.sd.y: 24,
            self.sd.z: 400,
        })

    def test_dual_sandwiched_variables_with_divider(self):
        @EquationSet
        def eqset(x, y, z):
            x = (2*y*3 + 5*z*10*2) / 2

        equation, = eqset
        right_coefficients = self.deducer.coefficients_of_expression(equation.right_expression)
        self.assertEqual(right_coefficients, {
            self.sd.y: 3,
            self.sd.z: 50,
        })

