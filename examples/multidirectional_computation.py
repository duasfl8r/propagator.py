from propagator import scheduler
from propagator.network import Propagator, Cell
from propagator.primitives import *
from propagator.interval import Interval
from propagator.decorators import compound
from propagator.logging import debug, warn, error, info

"""
A propagator network that calculates the approximated height of a
building from measurements made using a barometer, a stopwatch and a
ruler.

If does this using two new functions, `product` and `quadratic`, which
create various propagators that make data flow not only from some inputs
to a specific output, but in any way of the equations they model.

This makes new data about the building height propagate back and enhance the initial measurements.

This example is present (as Scheme code) in section 4 of The Art of the
Propagator, "Multidirectional Computation".
"""

# What would happen, for instance, if we augmented our arithmetic
# to impose a relation, or a constraint if you will, rather than
# computing a single “output” from the available “inputs”? To do that,
# we just stack appropriate mutual inverses on top of each other
#
# Whichever one has enough inputs will do its computation, and the cells
# will take care to not get too excited about redundant discoveries.

def product(x, y, total):
    multiplier(x, y, total)
    divider(total, x, y)
    divider(total, y, x)

def quadratic(x, x_to_2):
    squarer(x, x_to_2)
    sqrter(x_to_2, x)

# Our building measurement methods become multidirectional just by
# composing multidirectional primitives.

def fall_duration(t, h):
    @compound(neighbors=[t])
    def fall_duration_helper():
        g = Cell('g')
        one_half = Cell('one half')
        t_to_2 = Cell('t^2')
        g_times_t_to_2 = Cell('gt^2')

        (constant(Interval(9.789, 9.832)))(g)
        (constant(Interval(1/2, 1/2)))(one_half)
        quadratic(t, t_to_2)
        product(g, t_to_2, g_times_t_to_2)
        product(one_half, g_times_t_to_2, h)

    return fall_duration_helper

def similar_triangles(s_ba, h_ba, s, h):
    @compound(neighbors=[s_ba, h_ba, s])
    def similar_triangles_helper():
        ratio = Cell('ratio')
        product(s_ba, ratio, h_ba)
        product(s, ratio, h)

    return similar_triangles_helper


if __name__ == '__main__':
    scheduler.initialize()

    # Now the estimation of the building’s height works just fine,

    barometer_height = Cell('barometer height')
    barometer_shadow = Cell('barometer shadow')
    building_height = Cell('building height')
    building_shadow = Cell('building shadow')

    similar_triangles(barometer_shadow, barometer_height, building_shadow, building_height)

    building_shadow.add_content(Interval(54.9, 55.1))
    barometer_height.add_content(Interval(0.3, 0.32))
    barometer_shadow.add_content(Interval(0.36, 0.37))

    scheduler.run()

    print(building_height.content)
    # Interval(44.51351351351351, 48.977777777777774)

    # as does the refinement of that estimate by adding another
    # measurement.

    fall_time = Cell('fall time')

    fall_duration(fall_time, building_height)

    fall_time.add_content(Interval(2.9, 3.1))

    scheduler.run()

    print(building_height.content)
    # Interval(44.51351351351351, 47.24276000000001)

    # But something else interesting happens as well. The better
    # information available about the height of the building propagates
    # backward, and lets us infer refinements of some of our initial
    # measurements!

    print(barometer_height.content)
    # Interval(0.3, 0.3183938287795994)

    print(fall_time.content)
    # Interval(3.0091234174691017, 3.1)

    # Indeed, if we offer (yet another) barometer to the building’s
    # superintendent in return for perfect information about the
    # building’s height, we can use it to refine our understanding of
    # barometers and our experiments even further:

    building_height.add_content(Interval(45, 45))

    scheduler.run()

    print(barometer_height.content)
    # Interval(3.0091234174691017, 3.1)

    print(barometer_shadow.content)
    # Interval(0.366, 0.37)

    print(building_shadow.content)
    # Interval(54.9, 55.1)

    print(fall_time.content)
    # Interval(3.025522031629098, 3.0321598338046556)
