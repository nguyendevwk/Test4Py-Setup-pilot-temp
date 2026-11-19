import pytest
from docstring_parser.common import DocstringDeprecated


def test_deprecated_initialization_with_full_data():
    """DocstringDeprecated should store all provided arguments correctly."""
    args = ["arg1", "arg2"]
    description = "This function is deprecated."
    version = "1.2.3"
    dep = DocstringDeprecated(args, description, version)

    # Assert that the instance holds the exact values passed
    assert dep.args == args
    assert dep.description == description
    assert dep.version == version


def test_deprecated_initialization_with_missing_optional():
    """DocstringDeprecated should handle None for optional fields."""
    args = ["only_arg"]
    dep = DocstringDeprecated(args, None, None)

    # Optional fields should be None, args should be preserved
    assert dep.args == args
    assert dep.description is None
    assert dep.version is None


def test_deprecated_initialization_with_empty_args():
    """DocstringDeprecated should accept an empty list of arguments."""
    dep = DocstringDeprecated([], "No args", "0.0.1")

    # Empty args list should be stored without error
    assert dep.args == []
    assert dep.description == "No args"
    assert dep.version == "0.0.1"
