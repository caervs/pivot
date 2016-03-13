"""
Tools for expressing the relation of equation
"""
import inspect

from replicate.replicable import preprocessor

from pivot.lexicon.expression import Variable
from pivot.lexicon.statement import RelationalStatement


class Equation(RelationalStatement):
    """
    A RelationalStatement expressing the equality of two things
    """

    @preprocessor
    def preprocess(subj, obj):
        return dict(subj=subj, obj=obj, relation_name='=')


class EquationSet(set):
    """
    A set of Equations
    """
    equation_class = Equation

    @classmethod
    def from_dict_def(cls, es_def):
        """
        Create an EquationSet from a dict mapping variable names to expressions
        """
        expected_arg_names = list(inspect.signature(es_def).parameters)
        args = {name: Variable(name) for name in expected_arg_names}
        eq_dict = es_def(**args)
        return cls.from_equations(**eq_dict)

    @classmethod
    def from_equations(cls, *equations, **monov_eqs):
        """
        Create an EquationSet from an iterable of equations
        """
        return cls(equations + tuple(cls.equation_class(
            Variable(subj), obj) for subj, obj in monov_eqs.items()))

    # TODO consier adding just "from_def" which will evaluate function
    # body as if it were a set of equations