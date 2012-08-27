# -*- encoding: utf-8 -*-
"""
Defines various primitives that establish relationships between `Cell` objects.

They generally take some input cells and return a `Propagator` object
that calculates this relationship when the cells have enough content.
"""

import operator

from art import scheduler
from art.art import Propagator, Cell
from art.logging import debug, warn, error, info

"""
Takes a function `f` and returns a function wrapper that applies `f`
to its arguments if all of them are not `None`; returns `None` otherwise.
"""
def lift_to_cell_contents(f):
    def helper(*args):
        if None in args:
            return None
        return f(*args)
    return helper

"""
Returns a factory of propagators that apply a lifted version of function
`f` to its input cells and store the result on its output cell.

The input cells are defined as the factory's all but last arguments, and
the output cell as the last one.

It "lifts" `f` by wrapping it with `lift_to_cell_contents`, so that it
will return `None` if any of its arguments is `None`.
"""
def make_primitive(f):
    debug("Creating primitive from function {0}".format(f))

    def helper(*cells):
        inputs, output = cells[:-1], cells[-1]
        lifted_f = lift_to_cell_contents(f)

        def to_do():
            debug("Applying lifted {f} to {inputs}".format(f=f, inputs=", ".join(map(str, inputs))))
            debug("")
            output.add_content(lifted_f(*[c.content for c in inputs]))

        return Propagator(inputs, to_do)

    return helper

"""
A factory of propagators that add inputs to an output.
"""
adder = make_primitive(operator.add)

"""
A factory of propagators that subtract inputs to an output.
"""
subtractor = make_primitive(operator.sub)

"""
A factory of propagators that multiply inputs to an output.
"""
multiplier = make_primitive(operator.mul)

"""
A factory of propagators that divide inputs to an output.

Uses true division (as in `/`).
"""
divider = make_primitive(operator.truediv)

"""
A factory of propagators that make its output the absolute value of its input.
"""
absolute_value = make_primitive(operator.abs)

"""
A factory of propagators that make its output `True` if its
inputs `(a, b)` are so that `a < b`, and `False` otherwise.
"""
less_than = make_primitive(operator.lt)

"""
A factory of propagators that make its output `True` if its
inputs `(a, b)` are so that `a > b`, and `False` otherwise.
"""
greater_than = make_primitive(operator.gt)

"""
A factory of propagators that make its output `True` if its
inputs `(a, b)` are so that `a <= b`, and `False` otherwise.
"""
less_or_equal = make_primitive(operator.le)

"""
A factory of propagators that make its output `True` if its
inputs `(a, b)` are so that `a >= b`, and `False` otherwise.
"""
greater_or_equal = make_primitive(operator.ge)

"""
A factory of propagators that make its output the negation of
its input boolean interpretation.
"""
inverter = make_primitive(operator.not_)

"""
Returns a factory of propagators that always stores `value` on its
output.
"""
def constant(value):
    return make_primitive(lambda: value)

"""
A factory of propagators that make its output `predicate` if `if_true`
is true, and `None` otherwise.
"""
def switch(predicate, if_true, output):
    def conditional(p, if_true, if_false, output):
        def helper():
            if p.content is not None:
                if p.content:
                    output.add_content(if_true.content)
                else:
                    output.add_content(if_false.content)

        return Propagator([p, if_true, if_false], helper)

    return conditional(predicate, if_true, Cell(), output)
