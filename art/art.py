# -*- encoding: utf-8 -*-
from art import scheduler
from art.logging import debug, warn, error, info

class Cell:
    def __init__(self, content=None):
        debug("New cell: {0}".format(id(self)))
        self.neighbors = []
        self.content = None
        self.add_content(content)

    def __str__(self):
        return "<Cell: {content} ({id})>".format(id=id(self), **vars(self))

    def __unicode__(self):
        return self.__str__()

    def new_neighbor(self, n):
        if n not in self.neighbors:
            debug("{0} gets a new neighbor: {1}".format(self, n))
            self.neighbors.append(n)
            scheduler.alert_propagators(n)

    def add_content(self, c):
        debug("Adding content {1} to {0}".format(self, c))
        if c != None:
            if self.content == None:
                self.content = c
                scheduler.alert_propagators(self.neighbors)
            else:
                if self.content != c:
                    raise ValueError("Ack! Inconsistency!")
        else:
            debug("There's no content!")

class Propagator:
    def __init__(self, neighbors, to_do):
        debug("New propagator: {to_do} ({id})".format(id=id(self), to_do=to_do))
        for n in neighbors:
            n.new_neighbor(to_do)
        scheduler.alert_propagators(to_do)

    def __str__(self):
        return "<Propagator: {to_do} ({id})>".format(id=id(self), **vars(self))

    def __unicode__(self):
        return self.__str__()

    @classmethod
    def compound(cls, neighbors, to_build):
        done = False
        def test():
            nonlocal done
            if not done:
                if filter(lambda x: x is None, [c.content for c in neighbors]):
                    done = True
                    to_build()
        return Propagator(neighbors, test)
