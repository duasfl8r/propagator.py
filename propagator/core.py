# -*- encoding: utf-8 -*-
"""
A propagator network.

Classes defined in this module:

- `Cell`
- `Propagator`
- `Scheduler`

This module uses `propagator.scheduler`, a `Scheduler` object
that manages the propagator alerts.
"""

from contextlib import contextmanager

from propagator.generic_operator import make_generic_operator, assign_operation
from propagator.merging import merge, is_contradictory
from propagator.util import SetQueue, listify, all_none
from propagator.logging import debug, warn, error, info


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

scheduler = Scheduler()


"""
The storage unit of the propagator network.

Each cell may have content, stored in the `content` attribute -- that is
`None` if there is no content.

Each cell may have neighbors, stored in the `neighbors` attribute. It is
a list of propagators that are interested in the cell's content.

When the cell receives content, it alerts all neighbor propagators, so
they can update other cells based on this new content.
"""
class Cell:
    """
    Initialize a `Cell` object, with no neighbors.

    Parameters:

    - `content`: is provided, it is added as the cell's content.
    """
    def __init__(self, name=None, content=None):
        self.neighbors = []
        self.name = name
        self.content = None
        self.add_content(content)
        debug("New cell: " + str(self))

    def __repr__(self):
        return "Cell({name}, {content})".format(name=repr(self.name), content=repr(self.content))

    def __str__(self):
        return repr(self)

    def __unicode__(self):
        return str(self)

    """
    Add a propagator to the cell's neighbors, and alert it using the scheduler.

    The propagator is added only if it isn't already a neighbor.
    """
    def new_neighbor(self, n):
        if n not in self.neighbors:
            self.neighbors.append(n)
            scheduler.alert_propagators(n)

    """
    Add content to the cell and alert its neighbors if the cell is empty.

    If the content to be added is `None` or is equal to the cell's
    content, nothing is done.

    If there is content in the cell, and it differs from the parameter's
    content, there is inconsistency in the system; it raises a
    `ValueError`.

    Parameters:

    - `c`: the content to be added.
    """
    def add_content(self, increment):
        answer = merge(self.content, increment)

        if answer != self.content:
            debug("Adding content {1} to {0}".format(self, answer))
            self.content = answer
            scheduler.alert_propagators(self.neighbors)

"""
The machine of the propagator network.  
A `Propagator` is a machine that continously examines its input cells and
produces outputs when possible (i.e. when the inputs have enough information).
"""
class Propagator:
    """
    Initialize a `Propagator` object.

    `to_do` is scheduled to be run once by each of the cells in `neighbors`.

    `to_do` is then added as a neighbor to each of them, so it will run
    again every time one of the cells have its content changed.

    Parameters:

    - `neighbors`: cells that affect this propagator.
    - `to_do`: a function that creates some output based on `neighbors`'
      contents.
    """
    def __init__(self, neighbors, to_do):
        for n in neighbors:
            n.new_neighbor(to_do)
        scheduler.alert_propagators(to_do)

    def __str__(self):
        return "<Propagator: {to_do} ({id})>".format(id=id(self), **vars(self))

    def __unicode__(self):
        return self.__str__()

    """
    Returns a `Propagator` object that constructs its body on demand.

    Parameters:

    - `neighbors`: the propagator's neighbor cells.
    - `to_build`: a function that will be run only if there is at least
      one neighbor with content which is not `None`.
    """
    @classmethod
    def compound(cls, neighbors, to_build):
        done = False

        def compound_helper():
            nonlocal done
            if not done:
                if not all_none(n.content for n in neighbors):
                    done = True
                    to_build()

        return Propagator(neighbors, compound_helper)
