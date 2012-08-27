# -*- encoding: utf-8 -*-
"""
A scheduling system that queues propagators and runs them.

Classes defined in this module:

- `Scheduler`
"""

from contextlib import contextmanager
from art.logging import debug, warn, error, info

"""
Returns `value` it it is a list, `[value]` otherwise.
"""
def listify(value):
    if isinstance(value, list):
        return value
    else:
        return [value]

"""
Adds `thing` to `set_` and `list_` if it isn't in `set_` already.
"""
def order_preserving_insert(thing, set_, list_):
    if thing not in set_:
        set_.add(thing)
        list_.append(thing)

"""
A scheduler that stores propagators in a queue ("alerts" them) and runs
them until there are no propagators left.

Each propagator, when ran, may alert other propagators, so this process
will continue until the propagator network stabilizes.

"""
class Scheduler:
    def __init__(self):
        self.initialize()

    """
    Initialize the scheduler, emptying its queues and registers.
    """
    def initialize(self):
        debug("Initializing scheduler")

        self.clear_alerted_propagators()

        self.abort_process = False
        self.last_value_of_run = "done"
        self.propagators_ever_alerted = set()
        self.propagators_ever_alerted_list = []

    """
    Returns `True` if there are any alerted propagators in the queue; `False` otherwise.
    """
    @property
    def any_propagators_alerted(self):
        return len(self.alerted_propagators) > 0

    """
    Empties the queue of alerted propagators.
    """
    def clear_alerted_propagators(self):
        debug("Clearing alerted propagators")
        self.alerted_propagators = set()
        self.alerted_propagators_list = []

    def ordered_key_list(self, set_, list_):
        return list_[::]

    def alert_all_propagators(self):
        self.alert_propagators(
                ordered_key_list(self.propagators_ever_alerted,
                    self.propagators_ever_alerted_list))

    """
    Returns the alerted propagators.
    """
    @property
    def the_alerted_propagators(self):
        return self.ordered_key_list(self.alerted_propagators,
            self.alerted_propagators_list)

    @staticmethod
    @contextmanager
    def process_abortion(k):
        old_abort_process, self.abort_process = self.abort_process, k
        yield
        self.abort_process = old_abort_process

    """
    Alerts all propagators in `propagators`.

    Parameters:

    - `propagators`: a single `Propagator` object or a list of
      `Propagators objects.
    """
    def alert_propagators(self, propagators):
        debug("Alerting propagators: {0}".format(propagators))
        for p in listify(propagators):
            assert callable(p), "Alerting a non-procedure"
            order_preserving_insert(p, self.propagators_ever_alerted,
                    self.propagators_ever_alerted_list)
            order_preserving_insert(p, self.alerted_propagators,
                    self.alerted_propagators_list)

    """
    Pops and runs alerted propagators from the queue them until it is
    empty.
    """
    def run_alerted(self):
        temp = self.the_alerted_propagators
        debug("Running alerted propagators: {0}".format(temp))
        self.clear_alerted_propagators()
        for propagator in temp:
            propagator()
        if self.any_propagators_alerted:
            debug("More propagators alerted; let's run them")
            self.run_alerted()

    """
    Starts running the scheduler's queue.
    """
    def run(self):
        debug("Running scheduler")
        if self.any_propagators_alerted:
            self.last_value_of_run = self.run_alerted()
        else:
            debug("Scheduler done")
            return self.last_value_of_run
