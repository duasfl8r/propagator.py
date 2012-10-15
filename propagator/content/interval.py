from math import sqrt

from propagator.generic_operator import assign_operation
from propagator.merging import Contradiction
from propagator.operator import mul, truediv

class Interval:
    def __init__(self, low, high=None):
        self.low = low
        self.high = high is None and low or high

    def __str__(self):
        return 'Interval({low}, {high})'.format(**vars(self))

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, Interval) and (self.low == other.low) and (self.high == other.high)

    def __hash__(self):
        return hash(repr(self))

    def __and__(self, other):
        return Interval(max(self.low, other.low), min(self.high, other.high))

    def is_empty(self):
        return self.low > self.high

    def contains(self, number):
        return self.high >= number >= self.low


def _merge_intervals(content, increment):
    new_range = content & increment

    if new_range.is_empty():
        return Contradiction('Empty merge: {content} & {increment} == {new_range}'.format(**vars()))
    elif new_range == content:
        return content
    elif new_range == increment:
        return increment
    else:
        return new_range

def _ensure_inside(interval, number):
    if interval.contains(number):
        return number
    else:
        return Contradiction('{number} is not inside {interval}'.format(**vars()))

def is_number(thing):
    return isinstance(thing, (int, float, complex))

def is_interval(thing):
    return isinstance(thing, Interval)

assign_operation("merge",
    _merge_intervals,
    [is_interval, is_interval]
)

assign_operation("merge",
    lambda content, increment: _ensure_inside(increment, content),
    [is_number, is_interval]
)

assign_operation("merge",
    lambda content, increment: _ensure_inside(content, increment),
    [is_interval, is_number]
)

assign_operation("sqrt",
    lambda i: Interval(sqrt(i.low), sqrt(i.high)),
    [is_interval]
)

def coercing(coercer, f):
    return lambda *args: f(*[coercer(a) for a in args])

def to_interval(thing):
    if isinstance(thing, Interval):
        return thing
    else:
        return Interval(thing)


assign_operation("mul",
    lambda i1, i2: Interval(mul(i1.low, i2.low), mul(i1.high, i2.high)),
    [is_interval, is_interval]
)

assign_operation("mul",
    coercing(to_interval, mul),
    ([is_interval, is_number], [is_number, is_interval])
)

assign_operation("truediv",
    lambda i1, i2: mul(i1, Interval(truediv(1, i2.high), truediv(1, i2.low))),
    [is_interval, is_interval]
)

assign_operation("truediv",
    coercing(to_interval, truediv),
    ([is_interval, is_number], [is_number, is_interval])
)
