import unittest

from propagator import scheduler
from propagator import Cell
from propagator.primitives import adder, multiplier
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
