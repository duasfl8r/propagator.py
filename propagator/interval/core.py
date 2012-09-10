import math

from propagator import scheduler
from propagator.network import Cell

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

class IntervalCell(Cell):
    def merge(self, new_content):
        inf_interval = Interval(float("-inf"), float("inf"))

        def force_interval(n):
            number_types = [float, int, complex]

            if isinstance(n, Interval):
                return n

            if n is None:
                return inf_interval

            if any(isinstance(n, t) for t in number_types):
                return Interval(n, n)

            raise ValueError("{n} is not one of these: Interval, number, None".format(**vars()))

        new_range = force_interval(self.content) & force_interval(new_content)

        if new_range.is_empty():
            raise ContradictionError("Ack! Inconsistency!")

        if new_range == inf_interval:
            return None

        return new_range
