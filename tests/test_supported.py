import unittest

from propagator import scheduler
from propagator import Cell
from propagator.primitives import adder, multiplier
from propagator.content.interval import Interval
from propagator.content.supported import Support, Supported
from propagator.merging import merge, is_contradictory, Contradiction

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

class SupportedMergeTestCase(TestCaseWithScheduler):
    def test_merge_none_and_supported_interval(self):
        nil = None
        sup = Supported(Interval(15, 16), {'this', 'that'})

        self.assertEqual(
            merge(nil, sup),
            merge(sup, nil),
        )

        self.assertEqual(
            merge(sup, nil),
            Supported(Interval(15, 16), {'this', 'that'})
        )

    def test_merge_supported_none_and_supported_interval(self):
        nil = Supported(None, {})
        sup = Supported(Interval(15, 16), {'this', 'that'})

        self.assertEqual(
            merge(nil, sup),
            merge(sup, nil),
        )

        self.assertEqual(
            merge(sup, nil),
            Supported(Interval(15, 16), {'this', 'that'})
        )

    def test_merge_two_supporteds_nones(self):
        nil1 = Supported(None, {})
        nil2 = Supported(None, {})

        self.assertEqual(
            merge(nil1, nil2),
            Supported(None, {})
        )

    def test_merge_flat_interval_and_tighter_supported_interval(self):
        number = Interval(14.5, 16.7)
        sup = Supported(Interval(15, 16), {'this', 'that'})

        self.assertEqual(
            merge(number, sup),
            merge(sup, number),
        )

        self.assertEqual(
            merge(number, sup),
            Supported(Interval(15, 16), {'this', 'that'})
        )

    def test_merge_flat_interval_and_looser_supported_interval(self):
        number = Interval(14.5, 16.7)
        sup = Supported(Interval(3, 18), {'this', 'that'})

        self.assertEqual(
            merge(number, sup),
            merge(sup, number),
        )

        self.assertEqual(
            merge(number, sup),
            Supported(Interval(14.5, 16.7), {})
        )

    def test_merge_contradictory_supported_values(self):
        sup1 = Supported(Interval(3, 6), {})
        sup2 = Supported(Interval(7, 9), {})
        merged = merge(sup1, sup2)

        self.assertTrue(is_contradictory(merged))

class ContradictoryTestCase(TestCaseWithScheduler):
    def test_supported_contradiction_is_contradictory(self):
        sup = Supported(Contradiction('...'), {})
        self.assertTrue(is_contradictory(sup))

    def test_supported_interval_is_not_contradictory(self):
        sup = Supported(Interval(14, 15), {})
        self.assertFalse(is_contradictory(sup))

