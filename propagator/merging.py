from functools import partial
from operator import is_, is_not

from propagator.generic_operator import make_generic_operator, assign_operation
from propagator.logging import debug

class Contradiction:
    def __init__(self, message=None):
        self.message = message

    def __repr__(self):
        if self.message is None:
            return "Contradiction()"
        else:
            return "Contradiction({message})".format(**vars(self))

    def __str__(self):
        return repr(self)

    def __unicode__(self):
        return repr(self)

is_contradictory = make_generic_operator(1, "is_contradictory", lambda x: isinstance(x, Contradiction))
is_none = partial(is_, None)
is_not_none = partial(is_not, None)
is_anything = lambda x: True

def _default_merge(content, increment):
    debug("Merging {content} and {increment}...".format(**vars()))
    if content == increment:
        return content
    else:
        return Contradiction('{content} != {increment}'.format(**vars()))

merge = make_generic_operator(2, "merge", _default_merge)

def implies(v1, v2):
    return v1 == merge(v1, v2)


assign_operation("merge",
    lambda content, increment: content,
    [is_not_none, is_none]
)

assign_operation("merge",
    lambda content, increment: increment,
    [is_none, is_not_none]
)

assign_operation("merge",
    lambda contradiction, _: contradiction,
    [is_contradictory, is_anything]
)

assign_operation("merge",
    lambda _, contradiction: contradiction,
    [is_anything, is_contradictory]
)
