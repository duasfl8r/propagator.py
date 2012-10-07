import unittest

from propagator.merging import merge, Contradiction, is_contradictory
from propagator.interval import Interval
from propagator.supported import Supported

class ContradictionTestCase(unittest.TestCase):
    def test_if_contradiction_is_contradictory(self):
        c = Contradiction("foo")
        self.assertTrue(is_contradictory(c))

    def test_if_merging_contradiction_with_number_is_contradictory(self):
        c = Contradiction("foo")
        n = 10
        m1 = merge(c, n)
        m2 = merge(n, c)
        self.assertTrue(is_contradictory(m1))
        self.assertTrue(is_contradictory(m2))

    def test_if_merging_contradiction_with_interval_is_contradictory(self):
        c = Contradiction("foo")
        n = Interval(5, 10)
        m1 = merge(c, n)
        m2 = merge(n, c)
        self.assertTrue(is_contradictory(m1))
        self.assertTrue(is_contradictory(m2))

    def test_if_merging_contradiction_with_supported_value_is_contradictory(self):
        c = Contradiction("foo")
        n = Supported(Interval(5, 10))
        m1 = merge(c, n)
        m2 = merge(n, c)
        self.assertTrue(is_contradictory(m1))
        self.assertTrue(is_contradictory(m2))
