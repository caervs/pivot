import inspect
import operator

from replicate.replicable import Replicable, preprocessor


class SymbolicExpression(Replicable):
    @staticmethod
    def from_symbol(symbol_or_expression):
        if isinstance(symbol_or_expression, SymbolicExpression):
            return symbol_or_expression
        return SymbolicPrimitive(symbol_or_expression)

    def __add__(self, other):
        return SymbolicCompound(operator.add, self,
                                SymbolicExpression.from_symbol(other))

    def __radd__(self, other):
        return SymbolicExpression.from_symbol(other) + self

    def __mul__(self, other):
        return SymbolicCompound(operator.mul, self,
                                SymbolicExpression.from_symbol(other))

    def __rmul__(self, other):
        return SymbolicExpression.from_symbol(other) * self


class SymbolicPrimitive(SymbolicExpression):
    @preprocessor
    def preprocess(symbol, negated=False):
        pass

    def value_in_scope(self, scope):
        multiplier = -1 if self.negated else 1
        if isinstance(self.symbol, (int, float)):
            return multiplier * self.symbol
        return scope.get(self.symbol) * multiplier

    def __hash__(self):
        return hash((self.symbol, self.negated))

    def __str__(self):
        return str(self.symbol)


class SymbolicCompound(SymbolicExpression):
    @preprocessor
    def preprocess(operation, left_operand, right_operand):
        pass

    def value_in_scope(self, scope):
        return operation(self.left_operand.value_in_scope(scope),
                         self.right_operand.value_in_scope(scope))

    def __hash__(self):
        return hash((self.operation, self.left_operand, self.right_operand))

    def __str__(self):
        if self.operation == operator.add:
            return "%s + %s" % (self.left_operand, self.right_operand)
        elif self.operation == operator.mul:
            return "%s*%s" % (self.left_operand, self.right_operand)
        else:
            raise ValueError(self.operation)


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
        # HACK will have to fix for equation set methods
        indentation = 4
        unindented_body = "".join(line[indentation:] for line in body)
        func_args = inspect.getargspec(f).args
        global_scope = {arg_name: SymbolicExpression.from_symbol(arg_name)
                        for arg_name in func_args}
        exec(unindented_body, global_scope, eval_scope)
        print("eval_scope is", eval_scope.equations)

# initial tests of decorator

@EquationSet
def foobar(x, y, z):
    x = 1
    y = 2*x + 1
    z = 3*y + 4*x + 5
