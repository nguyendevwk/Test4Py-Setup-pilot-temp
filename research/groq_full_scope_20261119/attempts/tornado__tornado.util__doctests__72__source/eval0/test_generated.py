import unittest
import pytest
from tornado.util import doctests

def test_doctests_returns_test_suite():
    """The doctests function should return a unittest.TestSuite instance."""
    suite = doctests()
    assert isinstance(suite, unittest.TestSuite), "Expected a unittest.TestSuite instance"

def test_doctests_contains_tests():
    """The returned TestSuite should contain at least one test case."""
    suite = doctests()
    # countTestCases returns the total number of test cases in the suite
    assert suite.countTestCases() > 0, "Expected at least one test case in the suite"

def test_doctests_runs_without_failures(tmp_path):
    """Running the doctest suite should not produce any failures."""
    suite = doctests()
    runner = unittest.TextTestRunner(stream=open(tmp_path / "test_output.txt", "w"), verbosity=2)
    result = runner.run(suite)
    # Ensure the test run completed and there were no failures or errors
    assert result.wasSuccessful(), f"Doctest suite failed with {len(result.failures)} failures and {len(result.errors)} errors"
