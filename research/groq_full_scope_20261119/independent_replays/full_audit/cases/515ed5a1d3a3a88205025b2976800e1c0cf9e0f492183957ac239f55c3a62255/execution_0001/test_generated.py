import unittest
import pytest
import tornado.util as util

def test_doctests_returns_test_suite():
    """The doctests function should return a unittest.TestSuite instance."""
    suite = util.doctests()
    assert isinstance(suite, unittest.TestSuite), "doctests() did not return a TestSuite"

def test_doctests_contains_tests():
    """The returned TestSuite should contain at least one test case."""
    suite = util.doctests()
    # Count the number of test cases in the suite
    test_count = sum(1 for _ in suite)
    assert test_count > 0, "doctests() returned an empty TestSuite"

def test_doctests_run_without_failures(tmp_path):
    """Running the doctest suite should not produce any failures or errors."""
    suite = util.doctests()
    runner = unittest.TextTestRunner(stream=open(tmp_path / "test_output.txt", "w"), verbosity=0)
    result = runner.run(suite)
    assert result.failures == [], f"Doctest failures: {result.failures}"
    assert result.errors == [], f"Doctest errors: {result.errors}"
