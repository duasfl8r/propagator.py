import unittest
from operator import add, sub

from propagator import make_generic_operator, assign_operation

class GenericOperatorTestCase(unittest.TestCase):
    def test_default_operation(self):
        add_op = make_generic_operator(2, "add", add)
        self.assertEqual(add_op(3, 2), 5)

    def test_nondefault_operation(self):
        def is_number(thing):
            return any(isinstance(thing, cls) for cls in [int, float, complex])

        add_op = make_generic_operator(2, "add", sub)
        assign_operation("add", add, (is_number, is_number))
        self.assertEqual(add_op(3, 2), 5)

if __name__ == '__main__':
    unittest.main()
