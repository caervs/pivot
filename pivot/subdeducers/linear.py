import functools
import operator


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
