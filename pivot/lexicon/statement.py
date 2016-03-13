"""
Base vocabulary for making propositional statements
"""

from replicate.replicable import Replicable, preprocessor


class Statement(Replicable):
    """
    A mathematical statements (i.e. anything which is True or False or
    undecideable)
    """
    pass


class RelationalStatement(Statement):
    """
    A statement expressing a relation between a subject and an object
    """

    @preprocessor
    def preprocess(subj, relation_name, obj):
        """
        Preprocess RelationalStatement attributes
        """
        pass

    def __repr__(self):
        return "{} {} {}".format(self.subj, self.relation_name, self.obj)
