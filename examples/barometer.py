from propagator import scheduler
from propagator.network import Propagator, Cell
from propagator.primitives import *
from propagator.interval import Interval
from propagator.logging import debug, warn, error, info

"""
A propagator network that calculates the approximated height of a
building from measurements made using a barometer, a stopwatch and a
ruler.

This example is present (as Scheme code) in section 3 of The Art of the
Propagator, "Partial Information".
"""

# Let us start with dropping it off the roof and timing its fall. Then the
# height h of the building is given by:
#
#     h =  1 / (2 * g * pow(t, 2))
#
# where g is the acceleration due to gravity and t is the amount of time
# the barometer took to hit the ground. We implement this as a propagator
# network (that includes some uncertainty about the local g):

def fall_duration(t, h):
    def fall_duration_helper():
        g = Cell('g')
        one_half = Cell('one half')
        t_to_2 = Cell('t^2')
        g_times_t_to_2 = Cell('gt^2')

        (constant(Interval(9.789, 9.832)))(g)
        (constant(Interval(1/2, 1/2)))(one_half)
        squarer(t, t_to_2)
        multiplier(g, t_to_2, g_times_t_to_2)
        multiplier(one_half, g_times_t_to_2, h)

    return Propagator.compound([t], fall_duration_helper)

# Trying it out, we get an estimate for the height of the building:

scheduler.initialize()

fall_time = Cell('fall time')
building_height = Cell('building height')

fall_duration(fall_time, building_height)

fall_time.add_content(Interval(2.9, 3.1))

scheduler.run()

print(building_height.content)
# Interval(41.162745, 47.24276000000001)

# Of course, we can also measure the height of a building using a
# barometer by standing the barometer on the ground on a sunny day,
# measuring the height of the barometer as well as the length of its
# shadow, and then measuring the length of the building’s shadow and using
# similar triangles.
#
# The formula is:
#
#     h = s * (h_ba / s_ba)
#
# where h and s are the height and shadow-length of the building,
# respectively, and h_ba and s_ba are the barometer’s.
#
# The network for this is:

def similar_triangles(s_ba, h_ba, s, h):
    def similar_triangles_helper():
        ratio = Cell('ratio')
        divider(h_ba, s_ba, ratio)
        multiplier(s, ratio, h)

    return Propagator.compound([s_ba, h_ba, s], similar_triangles_helper)



# and we can try it out:

scheduler.initialize()

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

# Different measurements lead to different errors, and the computation
# leads to a different estimate of the height of the same building. This
# gets interesting when we combine both means of measurement, by measuring
# shadows first and then climbing the building and dropping the barometer
# off it:

fall_time = Cell('fall time')

fall_duration(fall_time, building_height)

fall_time.add_content(Interval(2.9, 3.1))

scheduler.run()

print(building_height.content)
# Interval(44.51351351351351, 47.24276000000001)

# It turns out that in this case the upper bound for the building’s
# height comes from the drop measurement, whereas the lower bound comes
# from the shadow measurement — we have a nontrivial combination of
# partial information from different sources.
