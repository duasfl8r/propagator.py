import unittest

from propagator import scheduler
from propagator import Cell
from propagator.primitives import adder, multiplier
from propagator.content.interval import Interval
from propagator.content.supported import Support, Supported

class TestCaseWithScheduler(unittest.TestCase):
    def setUp(self):
        scheduler.initialize()


class SupportTestCase(unittest.TestCase):
    def test_more_informative_than(self):
        s1 = Support(["source1", "source2", "source3"])
        s2 = Support(["source1", "source2"])
        self.assertTrue(s2.more_informative_than(s1))

class SupportedTestCase(TestCaseWithScheduler):
    def test_adder_exact(self):
        c1 = Cell(content=Supported(3))
        c2 = Cell(content=Supported(4))
        c3 = Cell()
        adder(c1, c2, c3)
        scheduler.run()
        self.assertEqual(c3.content, Supported(7))

    def test_multiplier_exact(self):
        c1 = Cell(content=Supported(3))
        c2 = Cell(content=Supported(4))
        c3 = Cell()
        multiplier(c1, c2, c3)
        scheduler.run()
        self.assertEqual(c3.content, Supported(12))

    def test_multiplier_interval(self):
        c1 = Cell(content=Supported(Interval(3, 4)))
        c2 = Cell(content=Supported(Interval(5, 6)))
        c3 = Cell()
        multiplier(c1, c2, c3)
        scheduler.run()
        self.assertEqual(c3.content, Supported(Interval(15, 24)))

    def test_supported_subsumes_one_with_same_value_and_looser_supports(self):
        sup1 = Supported(Interval(5, 10), {'this'})
        sup2 = Supported(Interval(5, 10), {'this', 'that'})
        self.assertTrue(sup1.subsumes(sup2))

    def test_supported_subsumes_one_with_looser_value_and_same_supports(self):
        sup1 = Supported(Interval(6, 9), {'this', 'that'})
        sup2 = Supported(Interval(5, 10), {'this', 'that'})
        self.assertTrue(sup1.subsumes(sup2))

    def test_supported_subsumes_one_with_looser_value_and_looser_supports(self):
        sup1 = Supported(Interval(6, 9), {'this'})
        sup2 = Supported(Interval(5, 10), {'this', 'that'})
        self.assertTrue(sup1.subsumes(sup2))

    def test_supported_doesnt_subsume_one_with_same_value_and_tighter_supports(self):
        sup1 = Supported(Interval(5, 10), {'this', 'that'})
        sup2 = Supported(Interval(5, 10), {'this'})
        self.assertFalse(sup1.subsumes(sup2))

    def test_supported_doesnt_subsume_one_with_tighter_value_and_same_supports(self):
        sup1 = Supported(Interval(5, 10), {'this', 'that'})
        sup2 = Supported(Interval(6, 9), {'this', 'that'})
        self.assertFalse(sup1.subsumes(sup2))

    def test_supported_doesnt_subsume_one_with_tighter_value_and_tighter_supports(self):
        sup1 = Supported(Interval(5, 10), {'this', 'that'})
        sup2 = Supported(Interval(6, 9), {'this'})
        self.assertFalse(sup1.subsumes(sup2))
