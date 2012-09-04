import unittest

from propagator import scheduler
from propagator.network import Cell, Propagator
from propagator.primitives import *

class TestCaseWithScheduler(unittest.TestCase):
    def setUp(self):
        scheduler.initialize()

class AdderTestCase(TestCaseWithScheduler):
    def test_integer(self):
        a = Cell()
        b = Cell()
        c = Cell()

        adder(a, b, c)

        a.add_content(15)
        b.add_content(13)

        scheduler.run()

        self.assertEqual(c.content, 28)

    def test_float(self):
        a = Cell()
        b = Cell()
        c = Cell()

        adder(a, b, c)

        a.add_content(1.5)
        b.add_content(1.3)

        scheduler.run()

        self.assertEqual(c.content, 2.8)

    def test_str(self):
        a = Cell()
        b = Cell()
        c = Cell()

        adder(a, b, c)

        a.add_content('15')
        b.add_content('13')

        scheduler.run()

        self.assertEqual(c.content, '1513')


class SubtractorTestCase(TestCaseWithScheduler):
    def test_integer(self):
        a = Cell()
        b = Cell()
        c = Cell()

        subtractor(a, b, c)

        a.add_content(15)
        b.add_content(13)

        scheduler.run()

        self.assertEqual(c.content, 2)


class MultiplierTestCase(TestCaseWithScheduler):
    def test_integer(self):
        a = Cell()
        b = Cell()
        c = Cell()

        multiplier(a, b, c)

        a.add_content(5)
        b.add_content(3)

        scheduler.run()

        self.assertEqual(c.content, 15)


class DividerTestCase(TestCaseWithScheduler):
    def test_integer(self):
        a = Cell()
        b = Cell()
        c = Cell()

        divider(a, b, c)

        a.add_content(9)
        b.add_content(3)

        scheduler.run()

        self.assertEqual(c.content, 3)


class AbsoluteValueTestCase(TestCaseWithScheduler):
    def test_integer(self):
        a = Cell()
        b = Cell()

        a_ = Cell()
        b_ = Cell()

        absolute_value(a, b)
        absolute_value(a_, b_)

        a.add_content(-9)
        a_.add_content(9)

        scheduler.run()

        self.assertEqual(b.content, 9)
        self.assertEqual(b_.content, 9)


class LessThanTestCase(TestCaseWithScheduler):
    def test_integer_true(self):
        a = Cell(content=13)
        b = Cell(content=15)
        c = Cell()

        less_than(a, b, c)

        scheduler.run()

        self.assertEqual(c.content, True)

    def test_integer_false(self):
        a = Cell(content=17)
        b = Cell(content=15)
        c = Cell()

        less_than(a, b, c)

        scheduler.run()

        self.assertEqual(c.content, False)


class GreaterThanTestCase(TestCaseWithScheduler):
    def test_integer_true(self):
        a = Cell(content=17)
        b = Cell(content=15)
        c = Cell()

        greater_than(a, b, c)

        scheduler.run()

        self.assertEqual(c.content, True)

    def test_integer_false(self):
        a = Cell(content=13)
        b = Cell(content=15)
        c = Cell()

        greater_than(a, b, c)

        scheduler.run()

        self.assertEqual(c.content, False)


class InverterTestCase(TestCaseWithScheduler):
    def test_true_to_false(self):
        a = Cell(content=True)
        b = Cell()

        inverter(a, b)

        scheduler.run()

        self.assertEqual(b.content, False)

    def test_false_to_true(self):
        a = Cell(content=False)
        b = Cell()

        inverter(a, b)

        scheduler.run()

        self.assertEqual(b.content, True)


class ConstantTestCase(TestCaseWithScheduler):
    def test_integer(self):
        a = Cell()

        constant(5)(a)

        scheduler.run()

        self.assertEqual(a.content, 5)


class SwitchTestCase(TestCaseWithScheduler):
    def test_true(self):
        a = Cell(content=True)
        b = Cell(content='yes')
        c = Cell()

        switch(a, b, c)

        scheduler.run()

        self.assertEqual(c.content, 'yes')

    def test_false(self):
        a = Cell(content=False)
        b = Cell(content='yes')
        c = Cell()

        switch(a, b, c)

        scheduler.run()

        self.assertEqual(c.content, None)


if __name__ == '__main__':
        unittest.main()
