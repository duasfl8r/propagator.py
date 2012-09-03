# -*- encoding: utf-8 -*-
"""
A scheduling system that queues propagators and runs them.

Classes defined in this module:

- `Scheduler`
"""

from contextlib import contextmanager
from art.logging import debug, warn, error, info
from art.util import SetQueue, listify

"""
A scheduler that stores propagators in a queue ("alerts" them) and runs
them until there are no propagators left.

Each propagator, when ran, may alert other propagators, so this process
will continue until the propagator network stabilizes.

"""
class Scheduler:
    def __init__(self):
        self.alerted_propagators = SetQueue()
        self.propagators_ever_alerted = SetQueue()

    """
    Initialize the scheduler, emptying its queues and registers.
    """
    def initialize(self):
        debug("Initializing scheduler")
        self.alerted_propagators.clear()
        self.propagators_ever_alerted.clear()


    """
    Alerts all propagators in `propagators`.

    Parameters:

    - `propagators`: a single `Propagator` object or a list of
      `Propagators objects.
    """
    def alert_propagators(self, propagators):
        for p in listify(propagators):
            assert callable(p), "Alerting a non-procedure"
            self.propagators_ever_alerted.add(p)
            self.alerted_propagators.add(p)

    """
    Pops and runs alerted propagators from the queue them until it is
    empty.
    """
    def run(self):
        debug("Running scheduler")
        while len(self.alerted_propagators):
            propagator = self.alerted_propagators.pop()
            propagator()
        debug("Scheduler done")
