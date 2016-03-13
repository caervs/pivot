"""
Mathematical Deducer and related classes
"""


class Deducer(object):
    """
    Makes logical deductions by calling out to SolvingEngins
    """
    pass


class Solver(Deducer):
    """
    A type of Deducer that solves equations
    """
    pass


class SolvingEngine(object):
    """
    Abstract base class for a deduction engine within particular domain
    """
    pass
