import unittest
import pytest
import tornado.util

def test_doctests_returns_test_suite():
    """The doctests() function should return a unittest.TestSuite instance."""
    suite = tornado.util.doctests()
    assert isinstance(suite, unittest.TestSuite), "Expected a unittest.TestSuite object"

def test_doctests_suite_contains_tests():
    """The returned TestSuite should contain at least one test case."""
    suite = tornado.util.doctests()
    # A TestSuite can contain nested suites; flatten them to count tests
    def count_tests(s):
        count = 0
        for test in s:
            if isinstance(test, unittest.TestSuite):
                count += count_tests(test)
            else:
                count += 1
        return count
    total = count_tests(suite)
    assert total > 0, "Expected at least one doctest in the suite"

def test_doctests_suite_runs_successfully():
    """Running the doctest suite should not produce any failures."""
    suite = tornado.util.doctests()
    runner = unittest.TextTestRunner(stream=open(os.devnull, 'w'), verbosity=0)
    result = runner.run(suite)
    assert result.wasSuccessful(), f"Doctest suite failed with {len(result.failures)} failures and {len(result.errors)} errors"
