# -*- encoding: utf-8 -*-
import math
import operator

from propagator.generic_operator import make_generic_operator, assign_operation, generic_operators

add = make_generic_operator(2, "add", operator.add)

sub = make_generic_operator(2, "sub", operator.sub)

mul = make_generic_operator(2, "mul", operator.mul)

truediv = make_generic_operator(2, "truediv", operator.truediv)

lt = make_generic_operator(2, "lt", operator.lt)

gt = make_generic_operator(2, "gt", operator.gt)

le = make_generic_operator(2, "le", operator.le)

ge = make_generic_operator(2, "ge", operator.ge)

not_ = make_generic_operator(1, "not_", operator.not_)

sqrt = make_generic_operator(1, "sqrt", math.sqrt)

abs = make_generic_operator(1, "abs", abs)

square = make_generic_operator(1, "square", lambda x: mul(x, x))
