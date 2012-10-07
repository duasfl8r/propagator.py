import unittest

from propagator import scheduler

class TestCaseWithScheduler(unittest.TestCase):
    def setUp(self):
        scheduler.initialize()

class SchedulerTestCase(TestCaseWithScheduler):
    def test_new_scheduler_has_no_alerted_propagators(self):
        self.assertEqual(len(scheduler.alerted_propagators), 0)
        self.assertEqual(len(scheduler.propagators_ever_alerted), 0)


if __name__ == '__main__':
        unittest.main()
