from propagator.network import Propagator

def compound(*, neighbors):
    def compound_(to_build):
        return Propagator.compound(neighbors, to_build)

    return compound_
