"""
Matrix object and related tools
"""

import fractions


def dot_product(v1, v2):
    """
    Return the dot-product of two vectors
    """
    return sum(v1[i] * v2[i] for i in range(len(v1)))


def swap(rows, index0, index1):
    """
    Return an input list with two entries swapped
    """
    indices = list(range(len(rows)))
    indices[index0] = index1
    indices[index1] = index0
    return [rows[index] for index in indices]


def ensure_good_pivot(rows, row_index):
    """
    Return an input list of rows with swapping done to ensure a good
    pivot point for a particular row
    """
    row = rows[row_index]
    pivot_point = row[row_index]
    # more general test for additive identity
    if pivot_point != -pivot_point:
        return rows
    for swap_index in range(row_index + 1, len(rows)):
        new_pivot = rows[swap_index][row_index]
        if new_pivot != -new_pivot:
            return swap(rows, row_index, swap_index)
    raise ValueError("Irredecuble rows")


def divide(x, y):
    """
    Divide two objects by first checking if they are integers and using
    rational division if necessary
    """
    if isinstance(x, int) and isinstance(y, int):
        if not x % y:
            return x // y
        return fractions.Fraction(x, y)
    return x / y


def reduced_rows(rows, start_row_index=0):
    """
    Reduce a matrix to the identity matrix
    """
    if start_row_index >= len(rows):
        return rows

    rows = ensure_good_pivot(rows, start_row_index)
    pivot_point = rows[start_row_index][start_row_index]
    pivot_row = rows[start_row_index] / pivot_point

    new_rows = [(row - (pivot_row * row[start_row_index])) for row in rows]
    new_rows[start_row_index] = pivot_row
    return reduced_rows(new_rows, start_row_index + 1)


def vector_product(v1, v2):
    """
    Return the dot-product of two vectors and the scalar product
    of a vector and a scaler
    """
    if not isinstance(v1, Vector):
        return type(v2)(elem * v1 for elem in v2)
    if not isinstance(v2, Vector):
        return type(v1)(elem * v2 for elem in v1)
    return dot_product(v1, v2)


class Vector(tuple):
    """
    An arrangement of elements which when composed with a mathematical operation
    will do a point-wise application of that operation
    """
    __add__ = lambda self, other: type(self)(self[i] + other[i] for i in range(len(self)))
    __sub__ = lambda self, other: self + (-other)
    __neg__ = lambda self: type(self)(-elem for elem in self)
    __truediv__ = lambda self, divisor: type(self)(divide(elem, divisor) for elem in self)
    __mul__ = vector_product
    __rmul__ = vector_product


class Matrix(Vector):
    """
    A vector of vectors of equal length
    """

    def __new__(cls, rows):
        cls.validate(rows)
        return super().__new__(cls, map(Vector, rows))

    def __mul__(self, other):
        # TODO implement
        pass

    @staticmethod
    def validate(rows):
        """
        Ensure rows of matrix have same length
        """
        if not rows:
            return
        row_length = len(rows[0])
        for row in rows:
            assert len(row) == row_length

    @property
    def reduced_form(self):
        """
        Return the reduced form of the matrix
        """
        return type(self)(reduced_rows(self))


class AugmentedMatrix(Matrix):
    """
    A matrix modeling a system of linear equations
    """

    @property
    def constants(self):
        """
        Return the right-most column of the Matrix as a Vector
        """
        return Vector(row[-1] for row in self)
