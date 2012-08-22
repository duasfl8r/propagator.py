import operator

from art import scheduler
from art.art import Propagator, Cell
from art.logging import debug, warn, error, info

def lift_to_cell_contents(f):
    def helper(*args):
        if None in args:
            return None
        return f(*args)
    return helper

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

adder = make_primitive(operator.add)
subtractor = make_primitive(operator.sub)
multiplier = make_primitive(operator.mul)
divider = make_primitive(operator.truediv)
absolute_value = make_primitive(operator.abs)
less_than = make_primitive(operator.lt)
greater_than = make_primitive(operator.gt)
less_or_equal = make_primitive(operator.le)
greater_or_equal = make_primitive(operator.ge)
inverter = make_primitive(operator.not_)

def constant(value):
    return make_primitive(lambda: value)

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
