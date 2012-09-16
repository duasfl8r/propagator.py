import unittest

from propagator import scheduler
from propagator.network import Cell, Propagator, is_contradictory
from propagator.primitives import *


class TestCaseWithScheduler(unittest.TestCase):
    def setUp(self):
        scheduler.initialize()

class CellTestCase(TestCaseWithScheduler):
    def test_new_cell_has_no_content(self):
        a = Cell()
        self.assertEqual(a.content, None)

    def test_new_cell_with_content(self):
        a = Cell(content='hello')
        b = Cell()
        b.add_content('hello')
        self.assertEqual(a.content, 'hello')
        self.assertEqual(b.content, 'hello')

    def test_add_nothing_to_empty_cell(self):
        a = Cell()
        a.add_content(None)
        self.assertEqual(a.content, None)

    def test_add_content_to_empty_cell(self):
        a = Cell()
        a.add_content('hello')
        self.assertEqual(a.content, 'hello')

    def test_add_new_content_to_filled_cell_returns_contradiction(self):
        a = Cell(content='hello')
        a.add_content('world')
        self.assertTrue(is_contradictory(a.content))

    def test_add_same_content_to_filled_cell(self):
        a = Cell(content='hello')
        a.add_content('hello')
        self.assertEqual(a.content, 'hello')

    def test_new_cell_has_no_neighbors(self):
        a = Cell(content='hello')
        self.assertEqual(a.neighbors, [])

    def test_new_cell_with_neighbors(self):
        f = lambda x: x

        a = Cell(content='hello')
        a.new_neighbor(f)
        self.assertEqual(a.neighbors, [f])

    def test_add_existing_neighbor(self):
        f = lambda x: x

        a = Cell(content='hello')
        a.new_neighbor(f)
        a.new_neighbor(f)
        self.assertEqual(len(a.neighbors), 1)



class PropagatorTestCase(TestCaseWithScheduler):
    def new_propagator_appends_function_to_neighbors(self):
        a = Cell()
        b = Cell()
        c = Cell()
        f = lambda x: x

        p = Propagator([a, b, c], f)

        for cell in [a, b, c]:
            self.assertEqual(cell.neighbors, [f])

if __name__ == '__main__':
    unittest.main()
