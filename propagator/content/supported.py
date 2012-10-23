import operator
from functools import reduce

from propagator.merging import merge, implies, is_contradictory
from propagator.generic_operator import assign_operation
from propagator.logging import debug
from propagator.content.interval import Interval
import propagator.operator

class Support(set):
    def __str__(self):
        return "{" + ", ".join(repr(i) for i in self) + "}"

    def __unicode__(self):
        return self.__str__()

    def more_informative_than(self, other):
        return self != other and self.issubset(other)


class Supported():
    def __init__(self, value, support=None):
        self.value = value

        if support is None:
            self.support = Support()
        elif not isinstance(support, Support):
            self.support = Support(support)
        else:
            self.support = support

    def __str__(self):
        return 'Supported({value}, {support})'.format(**vars(self))

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, Supported) and \
                self.value == other.value and \
                self.support == other.support

    def __hash__(self):
        return hash(repr(self))

    def subsumes(self, other):
        assert is_supported(other)
        return implies(self.value, other.value) and self.support.issubset(other.support)


def _merge_supporteds(content, increment):
    merged_value = merge(content.value, increment.value)

    if merged_value == content.value:
        if implies(increment.value, merged_value):
            # Confirmation of existing information
            if increment.support.more_informative_than(content.support):
                return increment
            else:
                return content
        else:
            # New information is not interesting
            return content
    elif merged_value == increment.value:
        # New information overrides old information
        return increment
    else:
        # Interesting merge, need both provenances
        return Supported(merged_value, content.support | increment.support)

def is_flat(thing):
    return isinstance(thing, (int, float, complex, Interval))

def is_supported(thing):
    return isinstance(thing, Supported)

assign_operation("merge",
    _merge_supporteds,
    [is_supported, is_supported]
)

assign_operation("merge",
    lambda s, f: _merge_supporteds(s, Supported(f)),
    [is_supported, is_flat]
)

assign_operation("merge",
    lambda f, s: _merge_supporteds(Supported(f), s),
    [is_flat, is_supported]
)

def supported_unpacking(function):
    def merge_supports(*supporteds):
        supports = [supported.support for supported in supporteds]
        merged_sets = reduce(operator.or_, supports, set())
        return Support(merged_sets)

    return lambda *args: Supported( \
        function(*[arg.value for arg in args]),
        merge_supports(*args)
    )

def coercing(coercer, f):
    return lambda *args: f(*map(coercer, args))

def to_supported(thing):
    if isinstance(thing, Supported):
        return thing
    else:
        return Supported(thing)

operator_names = ["add", "sub", "mul", "truediv"]
operator_functions = { name: getattr(propagator.operator, name) for name in operator_names }

for op_name, op_function in operator_functions.items():
    assign_operation(op_name,
        supported_unpacking(op_function),
        [is_supported, is_supported]
    )

        #lambda s, f, func=op_function: func(s.value, f),
    assign_operation(op_name,
        coercing(to_supported, supported_unpacking(op_function)),
        [is_supported, is_flat]
    )

        #lambda f, s, func=op_function: func(f, s.value),
    assign_operation(op_name,
        coercing(to_supported, supported_unpacking(op_function)),
        [is_flat, is_supported]
    )

assign_operation("sqrt", supported_unpacking(propagator.operator.sqrt), [is_supported]) 

assign_operation("is_contradictory",
    lambda s: is_contradictory(s.value),
    [is_supported]
)
