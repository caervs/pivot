import fractions
import functools
import operator

from pivot.props.equation import SymbolicPrimitive, SymbolicCompound


class Vector(list):
    def __add__(self, other):
        return Vector(map(operator.add, self, other))

    def __sub__(self, other):
        return Vector(map(operator.sub, self, other))

    def __mul__(self, other):
        if isinstance(other, Vector):
            return sum(map(operator.mul, self, other))
        return Vector(map(functools.partial(operator.mul, other),
                          self))

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        for index in range(len(self)):
            self[index] /= other
        return self

    def __iadd__(self, other):
        for index in range(len(self)):
            self[index] += other[index]
        return self

    def __isub__(self, other):
        for index in range(len(self)):
            self[index] -= other[index]
        return self


class Matrix(list):
    def __init__(self, rows):
        super().__init__(map(Vector, rows))


class LinearDeducer(object):
    default_cast = fractions.Fraction

    def reduce_mat(self, mat):
        """
        reduce the rows of an augmented matrix to row echelon form
        """
        mat_copy = list(map(Vector, mat))
        all_indices = set(range(len(mat)))

        for index, row in enumerate(mat_copy):
            row /= row[index]

            for other_index in (all_indices - {index}):
                other_row = mat_copy[other_index]
                other_row -= other_row[index] * row
        return mat_copy

    def solve_equation_set(self, eq_set):
        null_expressions = [eq.left_expression - eq.right_expression for eq in eq_set]
        coefficients_of_expressions = list(map(
            self.coefficients_of_expression, null_expressions))

        all_variables = set().union(*(coe.keys() for coe in coefficients_of_expressions))
        order = list(all_variables - {1})

        matrix = Matrix([self.row_from_null_expression_coefficients(coe, order)
                         for coe in coefficients_of_expressions])
        # TODO does this work when there are extra equations
        solutions = [l[-1] for l in self.reduce_mat(matrix)]
        return dict(zip(order, solutions))

    def row_from_null_expression_coefficients(self, expression, order):
        row = Vector()
        for symbolic_primitive in order:
            # TODO makes assumption that add ident is 0
            # TODO also module assumes mult ident is 1 everywhere
            row.append(expression.get(symbolic_primitive, 0))
        row.append(- expression.get(1, 0))
        return row

    def coefficients_of_expression(self, expression):
        # TODO refactor XXX

        if isinstance(expression, SymbolicPrimitive):
            coefficient = -1 if expression.negated else 1
            # TODO will have to update to support symbolic attributes
            if isinstance(expression.symbol, str):
                return {expression: coefficient}
            return {1: coefficient * self.default_cast(expression.symbol)}

        elif expression.operation == operator.add:
            left_coefficients = self.coefficients_of_expression(expression.left_operand)
            right_coefficients = self.coefficients_of_expression(expression.right_operand)

            for variable, coefficient in right_coefficients.items():
                if variable in left_coefficients:
                    left_coefficients[variable] += coefficient
                else:
                    left_coefficients[variable] = coefficient

            return left_coefficients

        elif expression.operation == operator.sub:
            left_coefficients = self.coefficients_of_expression(expression.left_operand)
            right_coefficients = self.coefficients_of_expression(expression.right_operand)

            for variable, coefficient in right_coefficients.items():
                if variable in left_coefficients:
                    left_coefficients[variable] -= coefficient
                else:
                    left_coefficients[variable] = -coefficient

            return left_coefficients

        elif expression.operation == operator.mul:
            left_coefficients = self.coefficients_of_expression(expression.left_operand)
            right_coefficients = self.coefficients_of_expression(expression.right_operand)

            if list(left_coefficients.keys()) == [1]:
                multiplier = left_coefficients[1]

                for variable in right_coefficients:
                    right_coefficients[variable] *= multiplier

                return right_coefficients
            elif list(right_coefficients.keys()) == [1]:
                multiplier = right_coefficients[1]

                for variable in left_coefficients:
                    left_coefficients[variable] *= multiplier

                return left_coefficients
            else:
                # TODO more helpful error message
                raise ValueError("Not a linear expression")

        elif expression.operation == operator.truediv:
            left_coefficients = self.coefficients_of_expression(expression.left_operand)
            right_coefficients = self.coefficients_of_expression(expression.right_operand)

            # TODO more helpful error message
            assert list(right_coefficients.keys()) == [1]

            multiplier = right_coefficients[1]

            for variable in left_coefficients:
                left_coefficients[variable] /= multiplier

            return left_coefficients
        else:
            raise ValueError(expression.operation)
