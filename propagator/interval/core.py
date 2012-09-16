from functools import partial

from propagator import scheduler
from propagator.generic_operator import assign_operation
from propagator.network import Cell, Contradiction

class Interval:
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def __str__(self):
        return 'Interval({low}, {high})'.format(**vars(self))

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if hasattr(other, "low") and hasattr(other, "high"):
            return (self.low == other.low) and (self.high == other.high)
        else:
            return False

    def __mul__(self, other):
        return Interval(self.low * other.low, self.high * other.high)

    def __truediv__(self, other):
        return self * Interval(1.0 / other.high, 1.0 / other.low)

    def __pow__(self, number):
        return Interval(pow(self.low, number), pow(self.high, number))

    def __and__(self, other):
        return Interval(max(self.low, other.low), min(self.high, other.high))

    def is_empty(self):
        return self.low > self.high

    def contains(number):
        return self.high >= number >= self.low


def _merge_intervals(content, increment):
    new_range = content & increment
    if new_range == content:
        return content
    elif new_range == increment:
        return increment
    elif new_range.is_empty():
        return Contradiction + ['Empty merge: {content} & {increment} == {new_range}'.format(**vars())]
    else:
        return new_range

def is_number(thing):
    return isinstance(thing, (int, float, complex))

def is_interval(thing):
    return isinstance(thing, Interval)

assign_operation("merge",
    _merge_intervals,
    (is_interval, is_interval)
)

def _ensure_inside(interval, number):
    if interval.contains(number):
        return number
    else:
        return Contradiction + ['{number} is not inside {interval}'.format(**vars())]

assign_operation("merge",
    lambda content, increment: _ensure_inside(increment, content),
    (is_number, is_interval)
)

assign_operation("merge",
    lambda content, increment: _ensure_inside(content, increment),
    (is_interval, is_number)
)


