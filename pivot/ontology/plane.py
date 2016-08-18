"""
Objects in the domain of 2D geometry
"""

from pivot.ontology.matrix import Vector


class PlaneVector(Vector):
    """
    A vector with two coordinates (conveniently named x and y)
    """

    @property
    def x(self):
        """
        The first coordinate of the vector
        """
        return self[0]

    @property
    def y(self):
        """
        The second coordinate of the vector
        """
        return self[1]
