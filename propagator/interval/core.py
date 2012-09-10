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
        new_range = self.content & new_content
        if new_range != self.content:
            if new_range.is_empty():
                raise ValueError("Ack! Inconsistency!")
            else:
                self.content = new_range
                scheduler.alert_propagators(self.neighbors)
