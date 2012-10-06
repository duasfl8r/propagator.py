from propagator import scheduler
from propagator.network import Propagator, Cell
from propagator.primitives import *
from propagator.interval import Interval
from propagator.supported import Supported
from propagator.decorators import compound
from propagator.logging import debug, warn, error, info

"""
A propagator network that calculates the approximated height of a
building from measurements made using a barometer, a stopwatch and a
ruler. Each subsequent measurement enhances the accuracy of the answer,
and also propagates back and enhances the other initial measurements.

It uses the `propagator.supported.Supported` class as content for the
`Cell` objects. The cells then can track the provenance of its data,
based on the supports given when new content is added or merged into
them.

This example is present (as Scheme code) in section 6 of The Art of the
Propagator, "Dependencies".
"""

def product(x, y, total):
    multiplier(x, y, total)
    divider(total, x, y)
    divider(total, y, x)

def quadratic(x, x_to_2):
    squarer(x, x_to_2)
    sqrter(x_to_2, x)

def similar_triangles(s_ba, h_ba, s, h):
    @compound(neighbors=[s_ba, h_ba, s, h])
    def similar_triangles_helper():
        ratio = Cell('ratio')
        product(s_ba, ratio, h_ba)
        product(s, ratio, h)

    return similar_triangles_helper

def fall_duration(t, h):
    @compound(neighbors=[t])
    def fall_duration_helper():
        g = Cell('g')
        one_half = Cell('one half')
        t_to_2 = Cell('t^2')
        g_times_t_to_2 = Cell('gt^2')

        (constant(Interval(9.789, 9.832)))(g)
        (constant(Interval(0.5, 0.5)))(one_half)
        quadratic(t, t_to_2)
        product(g, t_to_2, g_times_t_to_2)
        product(one_half, g_times_t_to_2, h)

    return fall_duration_helper

if __name__ == '__main__':
    scheduler.initialize()

    # We now build a sequence of sample dependency tracking systems of
    # increasing complexity. We start with a relatively simple system
    # that only tracks and reports the provenance of its data.
    #
    # How do we want our provenance system to work? We can make cells
    # and define networks as usual, but if we add supported values as inputs,
    # we get supported values as outputs:

    barometer_height = Cell('barometer height')
    barometer_shadow = Cell('barometer shadow')
    building_height = Cell('building height')
    building_shadow = Cell('building shadow')

    similar_triangles(barometer_shadow, barometer_height, building_shadow, building_height)

    building_shadow.add_content(Supported(Interval(54.9, 55.1), ['shadows']))
    barometer_height.add_content(Supported(Interval(0.3, 0.32), ['shadows']))
    barometer_shadow.add_content(Supported(Interval(0.36, 0.37), ['shadows']))

    scheduler.run()

    print(building_height.content)
    # Supported(Interval(44.51351351351351, 48.977777777777774), {'shadows'})

    # Indeed, our estimate for the height of the building depends on our
    # measurements of the barometer and the shadow. We can try
    # dropping the barometer off the roof, but if we do a bad job of
    # timing its fall, our estimate won’t improve.

    fall_time = Cell('fall time')
    fall_duration(fall_time, building_height)
    fall_time.add_content(Supported(Interval(2.9, 3.3), {'lousy fall time'}))

    scheduler.run()

    print(building_height.content)
    # Supported(Interval(45.51351351351351, 48.977777777777774), {'shadows'})

    # What’s more, the dependency tracker tells us that it was a lousy timing
    # job, because the resulting answer doesn’t actually depend on the fall
    # timing measurement. If we do it better, then we can get a finer estimate,
    # which then will depend on the improved fall timing measurement.

    fall_time.add_content(Supported(Interval(2.9, 3.1), {'better fall time'}))

    scheduler.run()

    print(building_height.content)
    # Supported(Interval(44.51351351351351, 47.24276000000001), {'shadows', 'better fall time'})

    # If we then give a barometer to the superintendent, we can watch the
    # superintendent’s information supercede and obsolesce the results of our
    # measurements...

    building_height.add_content(Supported(45, {'superintendent'}))

    scheduler.run()

    print(building_height.content)
    # Supported(45, {'superintendent'})

    # ...and see which of the measurements themselves we can infer more about
    # based on the now known height of the building.

    print(barometer_height.content)
    #Supported(Interval(0.3, 0.30327868852459017), {'shadows', 'better fall time', 'superintendent'})

    print(barometer_shadow.content)
    #Supported(Interval(0.366, 0.37), {'shadows', 'better fall time', 'superintendent'})

    print(building_shadow.content)
    #Supported(Interval(54.9, 55.1), {'shadows'})

    print(fall_time.content)
    #Supported(Interval(3.025522031629098, 3.0321598338046556), {'superintendent'})
