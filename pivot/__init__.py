import inspect

from replicate.replicable import Replicable, preprocessor


class Equation(Replicable):
    @preprocessor
    def preprocess(left_expression, right_expression):
        pass

    def __hash__(self):
        # TODO this should be in replicate
        return hash((self.left_expression, self.right_expression))

    def __repr__(self):
        # TODO this should be in replicate
        return "<Equation: %s = %s>" % (self.left_expression, self.right_expression)

class EquationAccumulator(dict):
    def __init__(self):
        self.equations = set()

    def __setitem__(self, key, value):
        self.equations.add(Equation(key, value))


class EquationSet(set):
    def __init__(self, equations=()):
        if inspect.isfunction(equations):
            super().__init__()
            self.update_from_function(equations)
        else:
            super().__init__(map(Equation, equations))

    def update_from_function(self, f):
        equations = set()
        source_lines, start_line = inspect.getsourcelines(f)
        def_lines = [index for index, line in enumerate(source_lines)
                     if line.startswith("def ")]
        # TODO there must be a cleaner way to get the function body
        body = source_lines[def_lines[0] + 1:]
        eval_scope = EquationAccumulator()
        # HACK
        indentation = 4
        unindented_body = "".join(line[indentation:] for line in body)
        exec(unindented_body, {}, eval_scope)
        print("eval_scope is", eval_scope.equations)

# initial tests of decorator

@EquationSet
def foobar():
    x = 1
