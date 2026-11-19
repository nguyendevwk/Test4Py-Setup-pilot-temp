import unittest
import pytest
import sys
import types
import importlib

# Import the target module
import tornado.util as util


def test_doctests_returns_test_suite():
    """The doctests() function should return a unittest.TestSuite instance."""
    suite = util.doctests()
    assert isinstance(suite, unittest.TestSuite), "Expected a TestSuite instance"
    # The suite should contain at least one test case
    assert suite.countTestCases() > 0, "Expected at least one doctest in the suite"


def test_doctests_suite_runs_without_failures(tmp_path):
    """Running the doctest suite should not produce any failures."""
    suite = util.doctests()
    # Capture the test runner output
    stream = open(tmp_path / "test_output.txt", "w")
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    stream.close()
    # The test run should be successful
    assert result.wasSuccessful(), f"Doctests failed: {result.failures + result.errors}"


def test_doctests_import_error_handled(monkeypatch):
    """If the doctest module cannot be imported, doctests() should raise ImportError."""
    # Temporarily remove doctest from sys.modules and block its import
    original_import = __import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "doctest":
            raise ImportError("doctest not available")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    with pytest.raises(ImportError, match="doctest not available"):
        util.doctests()
