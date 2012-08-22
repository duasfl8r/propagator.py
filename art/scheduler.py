# -*- encoding: utf-8 -*-
from contextlib import contextmanager
from art.logging import debug, warn, error, info

def listify(value):
    if isinstance(value, list):
        return value
    else:
        return [value]

def order_preserving_insert(thing, set_, list_):
    if thing not in set_:
        set_.add(thing)
        list_.append(thing)

class Scheduler:
    def __init__(self):
        self.initialize()

    def initialize(self):
        debug("Initializing scheduler")

        self.clear_alerted_propagators()

        self.abort_process = False
        self.last_value_of_run = "done"
        self.propagators_ever_alerted = set()
        self.propagators_ever_alerted_list = []

    @property
    def any_propagators_alerted(self):
        return len(self.alerted_propagators) > 0

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

    def alert_propagators(self, propagators):
        debug("Alerting propagators: {0}".format(propagators))
        for p in listify(propagators):
            assert callable(p), "Alerting a non-procedure"
            order_preserving_insert(p, self.propagators_ever_alerted,
                    self.propagators_ever_alerted_list)
            order_preserving_insert(p, self.alerted_propagators,
                    self.alerted_propagators_list)

    def run_alerted(self):
        temp = self.the_alerted_propagators
        debug("Running alerted propagators: {0}".format(temp))
        self.clear_alerted_propagators()
        for propagator in temp:
            propagator()
        if self.any_propagators_alerted:
            debug("More propagators alerted; let's run them")
            self.run_alerted()

    def run(self):
        debug("Running scheduler")
        if self.any_propagators_alerted:
            self.last_value_of_run = self.run_alerted()
        else:
            debug("Scheduler done")
            return self.last_value_of_run
