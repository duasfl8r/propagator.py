import math

from propagator.primitives import make_primitive
from propagator.primitives import multiplier, divider
from propagator.interval import Interval

@make_primitive
def squarer(i):
    return Interval(i.low*i.low, i.high*i.high)

@make_primitive
def sqrter(i):
    return Interval(math.sqrt(i.low), math.sqrt(i.high))
