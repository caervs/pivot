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

    def __bool__(self):
        return self.reflexive

    @preprocessor
    def preprocess(subj, obj, reflexive=False):
        return dict(subj=subj, obj=obj, relation_name='=', reflexive=reflexive)


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
    def from_set_def(cls, es_def, scope=None):
        """
        Create an EquationSet from a dict mapping variable names to expressions
        """
        expected_arg_names = list(inspect.signature(es_def).parameters)
        if scope is None:
            args = {name: Variable(name) for name in expected_arg_names}
        else:
            args = {name: getattr(scope, name) for name in expected_arg_names}
        eq_set = es_def(**args)
        return cls.from_equations(*eq_set)

    @classmethod
    def from_equations(cls, *equations, **monov_eqs):
        """
        Create an EquationSet from an iterable of equations
        """
        return cls(equations + tuple(
            cls.equation_class(Variable(subj), obj)
            for subj, obj in monov_eqs.items()))

    # TODO consier adding just "from_def" which will evaluate function
    # body as if it were a set of equations
