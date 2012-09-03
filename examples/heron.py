from art import scheduler
from art.art import Propagator, Cell
from art.primitives import *
from art.logging import debug, warn, error, info


def heron_step(x, g, h):
    def helper():
        x_over_g = Cell('x/g')
        g_plus_x_over_g = Cell('g+x/g')
        two = Cell('two')

        divider(x, g, x_over_g)
        adder(g, x_over_g, g_plus_x_over_g)
        (constant(2))(two)
        divider(g_plus_x_over_g, two, h)
    return Propagator.compound([x, g], helper)

if __name__ == "__main__":
    scheduler.initialize()

    x = Cell()
    g = Cell()
    h = Cell()
    heron_step(x, g, h)

    x.add_content(2)
    g.add_content(1.4)

    scheduler.run() 
    print(h.content)
