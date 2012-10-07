"""
A propagator network that calculates square roots using Heron's method.

Heron's method works by taking a initial guess `g` and making it
progressively near the real square root of a number `x`.

Each step in this process is called a "Heron step"; this step calculates a "better guess" `h`:

    ``h = (g + (x / g)) / 2``
"""

from propagator import scheduler
from propagator import Propagator, Cell
from propagator.primitives import *
from propagator.decorators import compound
from propagator.logging import debug, warn, error, info

"""
Creates a propagator network that calculates a better guess as a
square root of `x`, based on the value of `g`, and stores it in `h`.

Its behavior simulates this equation:

    h = (g + (x / g)) / 2

Parameters:

- `x`: a `Cell` object whose content is a number
- `g`: a `Cell` object whose content is a guess of the sqrt of `x`
- `h`: a `Cell` object that will store a better guess
"""
def heron_step(x, g, h):
    @compound(neighbors=[x, g])
    def helper():
        x_over_g = Cell('x/g')
        g_plus_x_over_g = Cell('g+x/g')
        two = Cell('two')

        divider(x, g, x_over_g)
        adder(g, x_over_g, g_plus_x_over_g)
        (constant(2))(two)
        divider(g_plus_x_over_g, two, h)
    return helper

"""
Creates a propagator network that calculates the square root of `x` and
stores it in `answer`.

Parameters:

- `x`: a `Cell` object whose content is a number
- `answer`: a `Cell` object that will store the approximated square root
  of `x`
"""
def sqrt_network(x, answer):
    @compound(neighbors=[x])
    def sqrt_network_helper():
        one = Cell('one')
        (constant(1))(one)
        sqrt_iter(x, one, answer)
    return sqrt_network_helper

"""
Creates a propagator network that calculates progressively better
guesses of the square root of `x` -- using `heron_step` until it finds
one good enough -- using `good_enuf`.

Parameters:

- `x`: a `Cell` object whose content is a number
- `g`: a `Cell` object whose content is a guess of the sqrt of `x`
- `answer`: a `Cell` object that will store the approximated square root
  of `x`
"""
def sqrt_iter(x, g, answer):
    @compound(neighbors=[x, g])
    def sqrt_iter_helper():
        debug("sqrt_iter_helper: {x}, {g}, {answer}".format(**vars()))
        done = Cell('done')
        not_done = Cell('not(done)')
        x_if_not_done = Cell('x if not(done)')
        g_if_not_done = Cell('g if not(done)')
        new_g = Cell('new g')

        good_enuf(g, x, done)
        switch(done, g, answer)
        inverter(done, not_done)
        switch(not_done, x, x_if_not_done)
        switch(not_done, g, g_if_not_done)
        heron_step(x_if_not_done, g_if_not_done, new_g)

        # Clever recursion: this will call this helper again only if
        # `x_if_not_done` is not None.
        #
        # `x_if_not_done` will not have content if `answer` has content,
        # so it will stop recursing when an answer is found.

        sqrt_iter(x_if_not_done, new_g, answer)

    return sqrt_iter_helper

"""
A `Cell` object containing a very small number.

Used in `good_enuf`.
"""
eps = Cell('eps', content=0.0000000001)

"""
Creates a propagator network that stores `True` in `done` if `g` is good
enough as a guess of the square root of `x`, and stores `False`
otherwise.

To be good enough, `g` and `x` contents have to obey this equation:

    abs(x - pow(g, 2)) <= eps

Where `eps` is a `Cell` object containing a very small number, and is
defined in this module.
"""
def good_enuf(g, x, done):
    @compound(neighbors=[g, x])
    def to_do():
        g_to_2 = Cell('g^2')
        x_minus_g_to_2 = Cell('x-g^2')
        ax_minus_g_to_2 = Cell('abs(x-g^2)')

        multiplier(g, g, g_to_2)
        subtractor(x, g_to_2, x_minus_g_to_2)
        absolute_value(x_minus_g_to_2, ax_minus_g_to_2)
        less_than(ax_minus_g_to_2, eps, done)

    return to_do


if __name__ == '__main__':
    scheduler.initialize()

    x = Cell('x')
    answer = Cell('answer')

    sqrt_network(x, answer)

    x.add_content(2)

    scheduler.run()

    print(answer.content)
