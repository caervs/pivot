# pivot: automated mathological deduction in python

## Introduction

pivot is an extensible library that allows you to write mathematical statements with python syntax and have the consequences of those statements automatically derived. To use pivot you will invoke the help of a Deducer object which then defers to "solving engines." The solving engines are domain specific so you can write an engine for deriving statements in any domain. Installation is easy with pip3, just run

```bash
pip3 install -e git+https://github.com/caervs/pivot.git#egg=pivot
```

## What can pivot do now?

So far pivot has a linear algebra solving engine. The implementation allows you to naturally specify systems of linear equations and have the solutions derived for you. The implementation is meant to be field-agnostic allowing you to use alternative definitions of vector addition, scalar multiplication, and the field identity elements. The interface for this feature is not yet battle tested. To create a system of equations you first must initialize your variables.

```python3
from pivot.lexicon.expression import Variable
x = Variable("x")
```

As a shortcut you can define multiple variables at once with

```python3
from pivot.interface.shortcuts import update_with_variables
update_with_variables(globals(), ['x', 'y', 'z'])
```

Now you can define entire systems of equations using the python syntax

```python3
from pivot.lexicon.equation import EquationSet

es0 = EquationSet.from_equations(x=1, y=x, z=y+x)
```

You can also use the `==` operator which lets you get around python syntax restrictions

```python3
es1 = EquationSet.from_equations(
    x == 5 - 3 * y + 2 * z,
    3 * x == 7 - 5 * y - 6 * z,
    2 * x == 8 - 4 * y - 3 * z)
```

Now that you have your equation sets defined pivot can find solutions for you

```python3
from pivot.deduction.linear import LinearEngine
solutions = LinearEngine.solve_equation_set(es1)
```

which will be a dict mapping variables to their solutions in the linear system.

## What will pivot be able to do?

From here it would be great to extend pivot to be able to make deductions in the languages of many different mathematical domains. Contributions are very welcome. Please ensure that your contributions are unit tested and pass lint and format tests. Tests are run with [pysh](https://github.com/caervs/pysh). Once installed you can run pivot tests by simply running

```bash
pysh test
```

from the pivot source directory. Thank you and happy solving.
